CHANGELOG
=========

4.3.20-bugfix-4 (2020-12-04)
----------------------------

- python-oembed 0.2.4.imio1

  - Quickfix: Always try to parse JSON (as default) from response
    Youtube stopped sending correct Content-Type header: text/html instead of JSON
    [laulaz]


4.3.20-bugfix-3 (2020-12-04)
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
