CHANGELOG
=========

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
