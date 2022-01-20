CHANGELOG
=========

4.3.20-19 (unreleased)
----------------------

- cpskin.locales 0.5.40

    - Add a missing translation for cookies preferences in colophon
      [boulch]

- cpskin.theme 0.6.56

    - Revert last release to handle cookies viewlet in cpskin.core directly
      [laulaz]

- cpskin.diazotheme.vicinity 0.6

    - Revert last release to handle cookies viewlet in cpskin.core directly
      [laulaz]

- cpskin.diazotheme.smart 0.6.29

    - Revert last release to handle cookies viewlet in cpskin.core directly
      [laulaz]

- cpskin.diazotheme.newDream 0.1.18

    - Revert 0.1.16 release to handle cookies viewlet in cpskin.core directly
      [laulaz]

- cpskin.diazotheme.memory 0.2.18

    - Revert last release to handle cookies viewlet in cpskin.core directly
      [laulaz]

- cpskin.diazotheme.dreambasic 0.3.13

    - Revert last release to handle cookies viewlet in cpskin.core directly
      [laulaz]

- cpskin.diazotheme.dream 0.2.15

    - Revert last release to handle cookies viewlet in cpskin.core directly
      [laulaz]

- cpskin.diazotheme.spirit 0.1.47

    - Revert last release to handle cookies consent viewlet in cpskin.core directly
      [laulaz]

- cpskin.core 0.14.7

    - Fix styles for cookies viewlets
      [thomlamb]

    - Put cookies viewlet in plone.portaltop (to avoid Diazo manipulations in themes)
      [laulaz]

    - Add link to cookies preferences in colophon
      [boulch]

- cpskin.core 0.14.6

    - Hide cookies viewlets by default (JS will show it if needed)
      [laulaz]

    - Fix styles for cookies viewlets
      [thomlamb]

- cpskin.theme 0.6.55

    - Add cookies consent viewlet in minisite mode (in Diazo rules)
      [laulaz]

- cpskin.diazotheme.newDream 0.1.17

    - WEB-3210: Revert 0.1.15 changes (that were never put in production)
      [laulaz, thomlamb]


- cpskin.diazotheme.newDream 0.1.16

    - Add cookies consent viewlet in minisite mode (in Diazo rules)
      [laulaz]

- cpskin.diazotheme.newDream 0.1.15

    - WEB-3210: Addition of a div container for the banner image. 
      This allows the live search to be able to go beyond the banner
      [thomlamb]

    - WEB-3210: Modification of the JS parrallax to work with the modifications of the banner.
      [thomlamb]

    - WEB-3210: Small improvements to the themes
      [thomlamb]

- cpskin.diazotheme.dream 0.2.14

    - Add cookies consent viewlet in minisite mode (in Diazo rules)
      [laulaz]

- cpskin.diazotheme.dreambasic 0.3.12

    - Add cookies consent viewlet in minisite mode (in Diazo rules)
      [laulaz]

- cpskin.diazotheme.memory 0.2.17

    - Add cookies consent viewlet in minisite mode (in Diazo rules)
      [laulaz]

- cpskin.diazotheme.smart 0.6.28

    - Add cookies consent viewlet in minisite mode (in Diazo rules)
      [laulaz]

- cpskin.diazotheme.vicinity 0.5

    - Add cookies consent viewlet in minisite mode (in Diazo rules)
      [laulaz]

- cpskin.diazotheme.spirit 0.1.46

    - Add cookies consent viewlet in minisite mode (in Diazo rules)
      [laulaz]

- cpskin.core 0.14.5

    - Fix styles for cookies viewlets
      [thomlamb]

- cpskin.core 0.14.4

    - WEB-3260: Styles for cookies viewlets.
      [thomlamb]

    - SUP-21625: Fix iframe class removal if specified manually
      [laulaz]

    - SUP-21477: Change cookies viewlet / overlay logic.
      We now show overlay only to see detailed options about cookies because viewlet
      allows to Accept / Refuse all cookies directly.
      [laulaz]

    - Fix iframe (un)blocking on faceted pages
      [laulaz]

    - Fix iframe blocked message when there are many iframes on the same page
      [laulaz]

- cpskin.locales 0.5.39

    - SUP-21477: Override some collective.privacy translations
      [laulaz]

- iaweb.privacy 1.0a2

    - SUP-21477: Change default cookies texts
      [laulaz]

- cpskin.core 0.14.3

    - Fix JS transformations on consent form: collective.privacy JS is not included
      on this form, so we need to move that code in a everywhere-included resource
      [laulaz]

    - SUP-21477: Use Allow as default value on cookies consent form
      [laulaz]


4.3.20-quick-18 (2022-01-12)
----------------------------

- Empty release to force a quick promote after a failed build
  [laulaz]


4.3.20-quick-17 (2022-01-11)
----------------------------

- cpskin.core 0.14.2

    - SUP-21477: Fix consent form override
      [laulaz]


4.3.20-quick-16 (2022-01-11)
----------------------------

- cpskin.core 0.14.1

    - SUP-21477: Allow consent form display on minisite (they are not INavigationRoot)
      [laulaz]

    - WEB-3595: Fix traceback when iframes have no width / height attributes
      [laulaz]


4.3.20-15 (2022-01-10)
----------------------

- cpskin.theme 0.6.54

    - WEB-3524: Change views permissions that are used in diazo manifest.
      Fix some recurring unauthorized access to these views.
      [boulch]

- cpskin.theme 0.6.53

    - Hide the export button for anonymous users
      [thomlamb]

- cpskin.locales 0.5.38

    - WEB-3260: Add translations for privacy overlay
      [laulaz]

- cpskin.core 0.14

    - WEB-3260: Add new cookies overlay based on collective privcay & iaweb.privacy
      iframes & language selectors are handled through JS code to avoid caching problems
      [laulaz]

- imio.gdpr 1.2

    - Add cookies policy default text & logic (same as legal mentions)
      [laulaz]


4.3.20-14 (2021-11-15)
----------------------

- cpskin.policy 4.3.56
  
  - Add subscriber (and upgrade step) to remove (duplicated) contact behavior from organization 
    Behavior may come back with collective.contact.core TypeInfo 
    [boulch]


4.3.20-13 (2021-10-28)
----------------------

- cpskin.core 0.13.51
  
  - Fix : Avoid event_listing can be play on any objects. 
    [boulch]

- Use environment variables for ZODB_CACHE_SIZE and ZEO_CLIENT_CACHE_SIZE. So we can override it on docker.
  [bsuttor]

- imio.behavior.teleservices 1.0.5

  - Fix query and authentication to get procedures from ia.teleservices.
    [boulch]

- cpskin.core 0.13.50

  - Fix : Avoid bug when collection return other brains than events
    [boulch]

- collective.contact.core 1.37

  - Add image path when exporting
    [boulch]


4.3.20-12 (2021-05-18)
----------------------

- cpskin.core 0.13.49

  - Removal of the underline style on the internal page menu and comma removal for contact addresses
    [thomlamb]

- imio.behavior.teleservices 1.0.4

  - Remove useless browser view
    [boulch]

- cpskin.contenttypes 1.0.13

  - Build more specific procedure interface
    [boulch]

  - Remove useless index because template si specifying in zcml file
    [boulch]

  - Add add_view Procedure expression
    [boulch]

- cpskin.contenttypes 1.0.12

  - e_guichet field is printing like a link in template
    [boulch]

  - Add new procedure validator
    [boulch]

  - e_guichet field always available (even if imio.behavior.teleservice is installed)
    [boulch]

  - Fix / update buildout & dependencies
    [laulaz]

- imio.prettylink 1.18

  - Improve check for file when adding @@download in url.
    [laz, boulch]


4.3.20-11 (2021-02-17)
----------------------

- cpskin.locales 0.5.37

  - Update translation files
    [boulch]

- cpskin.core 0.13.48

  - Fix upgrade step that was reinstalling whole cpskin.correct
    [laulaz]


4.3.20-10 (2021-02-16)
----------------------

- cpskin.core 0.13.47

  - Change of a css property for a better display of the mini-site navigation
    [thomlamb]


4.3.20-9 (2021-02-04)
---------------------
- collective.pivot 1.0a5

  - Improved UI
  - Modification react to display the popup from the map to the hover items.
  - Improved accessibility.
    [thomlamb]

- collective.pivot 1.0a4

  - Fix offer codeCgt.
    [boulch]

- cpskin.policy 4.3.55

  - Small changes in accessibility text.
    [boulch]

- cpskin.core 0.13.46

  - WEB-3423 : Add an option to view/hide a link to accessbility text in footer.
    [boulch]

- cpskin.policy 4.3.54

  - WEB-3487 : Install or update new collective.anysurfer accessibility text.
    [boulch]


4.3.20-8 (2021-01-11)
---------------------

- collective.anysurfer 1.4.2

  - Breadcrumb is already in a "div" in Plone4, so, we override plone.app.layout.viewlets.path_bar.pt. only for Plone5.
    [boulch]

- cpskin.contenttypes 1.0.11

  - WEBLIE-81 : Remove lead-image out of procedure template
    [boulch]

- collective.pivot 1.0a2

  - improvement of the development environment to react (less, svg), addition of styles.
    [thomlamb]


4.3.20-quick-7 (2020-12-15)
---------------------------

- imio.media 0.2.13

  - Use https to call oembed on youtube.
    [bsuttor]

- collective.pivot 1.0a2

  - Change style of pivot view / Split css and js on webpack build


4.3.20-6 (2020-12-14)
---------------------

- cpskin.minisite 1.1.8

    - WEB-3377: Fix traversing redirection where there are views / attributes in URL
      [laulaz]


4.3.20-5 (2020-12-09)
---------------------

- cpskin.diazotheme.newDream 0.1.14

    - WEB-3476: Move minisite logo outside banner
      We want to keep original behavior for all themes except newdream
      [laulaz]

- cpskin.theme 0.6.52

    - WEB-3476: Revert Keep old minisite-logo behavior intact when there is no banner
      We want to keep original behavior for all themes except newdream
      [laulaz]

- cpskin.core 0.13.45

    - WEB-3476: Revert Move minisite logo outside banner
      We want to keep original behavior for all themes except newdream
      [laulaz]

- cpskin.policy 4.3.52

    - Fix setup.py parsing.
      [bsuttor]

- cpskin.policy 4.3.51

    - WEB-3480: Fix strange error during upgrade step on some of our instance.
      [bsuttor]

    - WEB-3449: Handle prevent actions in folderish migration
      [laulaz]

    - WEB-3449: Make folderish migration more robust
      [laulaz]

- collective.pivot 1.0a1

  - initial release  +  added a react and webpack project for the pivot frontend
    [thomlamb, boulch]



4.3.20-quick-4 (2020-12-04)
----------------------------

- python-oembed 0.2.4.imio1

  - Quickfix: Always try to parse JSON (as default) from response
    Youtube stopped sending correct Content-Type header: text/html instead of JSON
    [laulaz]


4.3.20-quick-3 (2020-12-04)
----------------------------

- imio.media 0.2.12

  - Return empty string if no data from provider.
    [bsuttor]


4.3.20-2 (2020-11-26)
---------------------

- cpskin.slider 1.2.11

  - slick_slider : Print short date : Print short date format when only one day is select but from an hour to another.
    [boulch]

- cpskin.theme 0.6.51

  - Keep old minisite-logo behavior intact when there is no banner + avoid error in pypi renderer
    [laulaz]


4.3.20-1 (2020-11-23)
---------------------

- cpskin.core 0.13.44

    - WEB-3476 : Move minisite logo outside banner
      [laulaz]

- cpskin.slider 1.2.10

    - [WEB-3478] slick_slider : Print short date format if show_day_and_month is true.
      [boulch]

- Update to Plone 4.3.20.
  [cboulanger]


0.1 (2014-07-22)
----------------

- Initial release
