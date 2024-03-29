#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import ast
import getpass
import json
import os
import subprocess
import urllib
import requests


class Environment:
    def __init__(self):
        self.env_filename = ".env"
        self.get_env_from_file()
        self.manage_args()
        if self.start_rsync:
            self.rsync()
        if self.start_server_infos:
            self.get_server_infos()
        if self.start_minisites_files:
            self.set_minisites_files()

    def get_env_from_file(self):
        f = open("{0}/{1}".format(os.getcwd(), self.env_filename), "r")
        self.env = {}
        for line in f.readlines():
            key, value = line.rstrip().split("=")
            self.env[key] = value

    def set_env_to_file(self, key, value):
        if key not in self.env.keys():
            f = open("{0}/{1}".format(os.getcwd(), self.env_filename), "a")
            f.write("{0}={1}\n".format(key, value))
            f.close()
            self.env[key] = value

    def manage_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-p",
            "--projectid",
            dest="projectid",
            type=str,
            help="Id of project you are working on (liege, namur, ..)",
        )
        parser.add_argument(
            "-r",
            "--rsync",
            dest="rsync",
            type=str,
            help="You can rsync only blobstorage or Data.fs, options are b or d",
        )
        parser.add_argument("--serverinfos", action="store_true")
        parser.add_argument("--minisitesfiles", action="store_true")
        parse_args = parser.parse_args()
        if "projectid" not in self.env.keys():
            projectid = parse_args.projectid
            if not projectid:
                projectid = os.path.basename(os.getcwd())
                if "." in projectid:
                    projectid = projectid.split(".")[-1]
            self.set_env_to_file("projectid", projectid)
        if not parse_args.rsync:
            self.start_rsync = False
        else:
            self.start_rsync = True
            self.rsync_option = parse_args.rsync
        self.start_server_infos = parse_args.serverinfos
        self.start_minisites_files = parse_args.minisitesfiles

    def get_server_infos(self):
        if "servername" not in self.env.keys() or "minisites" not in self.env.keys():
            url = "http://infra-api.imio.be/application/{0}/website/production".format(
                self.env["projectid"]
            )
            url = "http://infra-api.imio.be/application/website"
            json_result = requests.get(url).json()
            result = [site for site in json_result if site.get("application_name") == "{0}_website".format(self.env["projectid"]) and site.get("environment") == "production"]
            # result = json.load(urllib.urlopen(url))
            if len(result) < 0 or isinstance(result, dict):
                print("Error in {0}".format(url))
                return 0
            num = 0
            if len(result) != 1:
                # choose good one
                pass
            if "servername" not in self.env.keys():
                server = result[num].get("host")
            #    if "lan" not in server:
            #        server = server.replace("imio.be", "lan.imio.be")
                self.set_env_to_file("servername", server)
            if "serverip" not in self.env.keys():
                try:
                    ip = result[num]["instance_port_urls"][-1].split(":")[1].replace("//", "")
                    self.set_env_to_file("serverip", ip)
                except:
                    pass
            if "minisites" not in self.env.keys():
                ms = result[num].get("minisites")
                minisites = [val["path"] for val in ms.values()]
                self.set_env_to_file("minisites", minisites)

    def rsync(self):
        if "servername" not in self.env.keys():
            self.get_server_infos()
        if "username" not in self.env.keys():
            user = "imio"
            # user = getpass.getuser()
            # answer = raw_input(
            #     "Which user script could use to make rsync command? If you leave empty, script will use {0} ".format(
            #         user
            #     )
            # )
            # if answer:
            #     user = answer
            self.set_env_to_file("username", user)
        else:
            user = self.env["username"]
        test_cmd = [
            "ssh",
            "-oBatchMode=yes",
            "-oStrictHostKeyChecking=no",
            "{0}@{1}".format(user, self.env["serverip"]),
            "ls -l",
        ]
        try:
            subprocess.check_output(test_cmd)
        except subprocess.CalledProcessError:
            print(" ".join(test_cmd))
            print ("You have no right to rsync on {0}, ask sysadmin to add your user to imio group.".format(
                self.env["serverip"]
            ))  # noqa
            return 0
        rsync_server_path = "{0}@{1}:/srv/instances/{2}".format(
            user, self.env["serverip"], self.env["projectid"]
        )
        if self.rsync_option in ["a", "d"]:
            os.system(
                "rsync -avP {0}/filestorage/Data.fs var/filestorage/Data.fs".format(
                    rsync_server_path
                )
            )
        if self.rsync_option in ["a", "b"]:
            os.system(
                "rsync -r --info=progress2 {0}/blobstorage/ var/blobstorage/".format(
                    rsync_server_path
                )
            )

    def set_minisites_files(self):
        if "minisites" not in self.env.keys():
            self.get_server_infos()
            if "minisites" not in self.env.keys():
                return
        # var/instance/minisites files
        i = 1
        minisites = ast.literal_eval(self.env["minisites"])
        for minisite in minisites:
            fname = "{0}/var/instance/minisites/ms_{1}.ini".format(os.getcwd(), i)
            if os.path.isfile(fname):
                f = open(fname, "w")
            else:
                f = open(fname, "w+")
            f.write("[/{0}{1}]\r\n".format(self.env["projectid"], minisite))
            f.write("minisite_url = http://minisite{0}.localhost\r\n".format(i))
            f.write("portal_url = http://portal.localhost\r\n")
            f.close()
            i += 1
        fname = "{0}/traefik.toml".format(os.getcwd())
        if os.path.isfile(fname):
            f = open(fname, "w")
        else:
            f = open(fname, "w+")

        f.write("[file]\r\n")
        f.write("[backends]\r\n")
        f.write("  [backends.backend]\r\n")
        f.write("    [backends.backend.servers.server1]\r\n")
        f.write('    url = "http://instance:8081"\r\n')
        f.write("[frontends]\r\n")
        f.write("  [frontends.frontend1]\r\n")
        f.write('    backend = "backend"\r\n')
        f.write("    passHostHeader = true\r\n")
        f.write("    [frontends.frontend1.routes.portal]\r\n")
        f.write(
            '      rule = "Host:portal.localhost; AddPrefix: /VirtualHostBase/http/portal.localhost/{0}/VirtualHostRoot"\r\n'.format(
                self.env["projectid"]
            )
        )
        i = 2
        for minisite in minisites:
            f.write("  [frontends.frontend{0}]\r\n".format(i))
            f.write('    backend = "backend"\r\n')
            f.write("    passHostHeader = true\r\n")
            f.write("    [frontends.frontend{0}.routes.minisite]\r\n".format(i))
            f.write(
                '      rule = "Host:minisite{0}.localhost; AddPrefix: /VirtualHostBase/http/minisite{0}.localhost/{1}{2}/VirtualHostRoot"\r\n'.format(
                    i - 1, self.env["projectid"], minisite
                )
            )
            i += 1
        f.close()


if __name__ == "__main__":
    env = Environment()
