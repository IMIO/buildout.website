# -*- coding: utf-8 -*-
"""
Delete bot users created by cpskin.citizen.

cpskin.citizen does not create users itself: its ``afterMemberAdd`` monkeypatch
(``cpskin/citizen/monkeypatches.py``) adds *every self-registered* user to the
``Citizens`` group (admin-created users are not added). So membership in the
``Citizens`` group == "account created through this package".

Self-registration has no CAPTCHA / email verification / rate limiting, so the
``Citizens`` group fills up with bot accounts. This script deletes them, while
protecting any citizen who has actually interacted with content.

A user is PROTECTED (never deleted) if their id appears in either of the two
catalog metadata columns the package maintains
(``cpskin/citizen/profiles/default/catalog.xml``):

  * ``citizens``      -> approved claimants (copied into ``obj.citizens``)
  * ``citizen_claim`` -> pending claimants (``utils.get_claim_users``)

Working-copy drafts need no separate check: a draft only exists after a
checkout, which requires an approved claim, so its owner is already in
``obj.citizens`` -> already protected.

Deletion target = Citizens group members - protected set. Those accounts have
no claims, no approved content and no drafts, so deleting them leaves no
dangling references.

Usage (run in-process via the Zope/Plone instance, NOT as a plain script)::

    bin/instance run scripts/citizen_cleanup.py                 # dry-run (report only)
    bin/instance run scripts/citizen_cleanup.py --confirm       # delete + commit
    bin/instance run scripts/citizen_cleanup.py --confirm Plone # pick a site id

Dry-run is the default: it reports counts, writes a CSV of the candidate ids and
aborts the transaction. Nothing is deleted unless ``--confirm`` is passed.
"""

from __future__ import print_function

import csv
import sys

import transaction
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Testing.makerequest import makerequest
from datetime import datetime
from plone import api
from zope.component.hooks import setSite


# Commit every COMMIT_BATCH deletions to bound memory and conflict-error risk
# against an instance still serving live traffic.
COMMIT_BATCH = 500


def real_args(argv):
    """Return the user args passed after the script path.

    Under ``bin/instance run`` sys.argv looks like
    ``[<runner>, '-c', 'scripts/citizen_cleanup.py', <real args...>]`` -- the
    runner's own flags and the script path both precede the real arguments, so
    plain ``sys.argv[1:]`` would mistake ``-c`` / the script path for a site id.
    Slice to whatever comes after the token ending in this script's filename.
    """
    for index, arg in enumerate(argv):
        if arg.replace("\\", "/").endswith("citizen_cleanup.py"):
            return argv[index + 1:]
    return argv[1:]


def parse_args(argv):
    """Return (confirm, site_id) from the user args passed after the script."""
    args = real_args(argv)
    confirm = "--confirm" in args
    positional = [a for a in args if not a.startswith("-")]
    site_id = positional[0] if positional else None
    return confirm, site_id


def find_plone_sites(app):
    """Return all Plone sites directly under the Zope root."""
    return [
        obj
        for obj in app.objectValues()
        if IPloneSiteRoot.providedBy(obj)
    ]


def resolve_site(app, site_id):
    """Return the Plone site to operate on, or exit with a helpful message."""
    sites = find_plone_sites(app)
    if site_id:
        for site in sites:
            if site.getId() == site_id:
                return site
        sys.exit(
            "No Plone site with id '{0}'. Available: {1}".format(
                site_id, ", ".join(s.getId() for s in sites) or "(none)"
            )
        )
    if len(sites) == 1:
        return sites[0]
    if not sites:
        sys.exit("No Plone site found under the Zope root.")
    sys.exit(
        "Multiple Plone sites found ({0}); pass a site id as an argument.".format(
            ", ".join(s.getId() for s in sites)
        )
    )


def setup_security(app):
    """Install an admin/Manager security manager so deletions are permitted."""
    acl_users = app.acl_users
    user = acl_users.getUserById("admin")
    if user is None:
        # Fall back to any root user holding the Manager role.
        for candidate in acl_users.getUsers():
            if "Manager" in candidate.getRoles():
                user = candidate
                break
    if user is None:
        sys.exit(
            "No Manager user found on the Zope root acl_users; cannot delete users."
        )
    newSecurityManager(None, user.__of__(acl_users))


def build_protected_set(portal):
    """Return the set of user ids that have claimed / been granted content."""
    catalog = api.portal.get_tool("portal_catalog")
    protected = set()
    for brain in catalog(is_citizen_content=True):
        protected.update(brain.citizens or [])
        protected.update(brain.citizen_claim or [])
    return protected


def get_citizen_members(portal):
    """Return the set of user ids in the Citizens group (package-created users)."""
    group = api.group.get(groupname="Citizens")
    if group is None:
        return set()
    return set(group.getGroupMemberIds())


def get_total_user_count(portal):
    """Return the total number of users on the site (all accounts)."""
    return len(api.user.get_users())


def write_csv(site_id, candidates, protected_count, member_count, total_users):
    """Write a timestamped report of the candidate user ids."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "citizen_cleanup_{0}_{1}.csv".format(site_id, stamp)
    with open(filename, "w") as fh:
        writer = csv.writer(fh)
        writer.writerow(["site", site_id])
        writer.writerow(["total_users", total_users])
        writer.writerow(["citizens_group_members", member_count])
        writer.writerow(["protected", protected_count])
        writer.writerow(["to_delete", len(candidates)])
        writer.writerow([])
        writer.writerow(["userid_to_delete"])
        for uid in candidates:
            writer.writerow([uid])
    return filename


def delete_users(candidates):
    """Delete the given user ids in batches, committing per batch.

    Passes ``delete_localroles=0``: these candidates provably have no local
    roles (no claims, no content, no drafts -> otherwise protected), so the
    default recursive site-wide local-role + security reindex done by
    ``deleteMembers`` is pure wasted work -- and is the ~10s/user bottleneck.
    ``delete_memberareas`` is left at its default (cheap when member-area
    creation is off; avoids orphan /Members/<id> folders when it is on).

    Returns (ok, failed).
    """
    mtool = api.portal.get_tool("portal_membership")
    ok, failed = 0, 0
    with api.env.adopt_roles(["Manager"]):
        for start in range(0, len(candidates), COMMIT_BATCH):
            batch = candidates[start:start + COMMIT_BATCH]
            try:
                deleted = mtool.deleteMembers(batch, delete_localroles=0)
                ok += len(deleted)
                transaction.commit()
                print("  ... deleted {0}/{1}".format(
                    start + len(batch), len(candidates)))
            except Exception as exc:  # noqa - isolate the bad account
                transaction.abort()
                print("  ! batch failed ({0}); retrying individually".format(exc))
                for uid in batch:
                    try:
                        mtool.deleteMembers([uid], delete_localroles=0)
                        transaction.commit()
                        ok += 1
                    except Exception as exc2:  # noqa - report and continue
                        transaction.abort()
                        failed += 1
                        print("    ! failed to delete {0}: {1}".format(uid, exc2))
    return ok, failed


def main(app):
    confirm, site_id = parse_args(sys.argv)

    app = makerequest(app)
    setup_security(app)
    portal = resolve_site(app, site_id)
    setSite(portal)
    site_id = portal.getId()

    print("=== cpskin.citizen bot-user cleanup ===")
    print("Site: {0}   Mode: {1}".format(
        site_id, "DELETE (--confirm)" if confirm else "DRY-RUN"))

    members = get_citizen_members(portal)
    protected = build_protected_set(portal)
    candidates = sorted(members - protected)
    total_users = get_total_user_count(portal)

    print("Total users (all)       : {0}".format(total_users))
    print("Citizens group members  : {0}".format(len(members)))
    print("Protected (have content): {0}".format(len(protected & members)))
    print("Candidates to delete    : {0}".format(len(candidates)))

    csv_file = write_csv(
        site_id, candidates, len(protected & members), len(members), total_users)
    print("Candidate list written to: {0}".format(csv_file))

    if not confirm:
        transaction.abort()
        print("DRY-RUN: no users deleted, transaction aborted.")
        print("Re-run with --confirm to delete the listed users.")
        return

    if not candidates:
        transaction.abort()
        print("Nothing to delete.")
        return

    print("Deleting {0} users...".format(len(candidates)))
    ok, failed = delete_users(candidates)
    print("Done. Deleted: {0}   Failed: {1}".format(ok, failed))


# `bin/instance run` executes this module with the Zope root bound to `app`.
if "app" in globals():
    main(app)  # noqa: F821 - provided by bin/instance run
