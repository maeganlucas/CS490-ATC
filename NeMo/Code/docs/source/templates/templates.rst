HTML Template Documentation
===========================

.. _Jinja2 Template Engine: https://jinja.palletsprojects.com/en/latest/

Since this application is built with Flask, it makes use of the `Jinja2 Template Engine`_. If you are unfamiliar with the syntax
of the templates, you should (re-)familiarize yourself with it before continuing. Although the templates and rendered and technically
written in HTML, the raw templates often look nothing like HTML at first glance.

Base Template
-------------

File: ``template.html``

This file serves - perhaps confusingly - as the base template for the rest of the HTML pages in this project, with the exception
of the map pages.

For clarity, this is the base template from which all the other pages are built. From an inheritance point-of-view, this is the parent
template from which all the other templates inherit.

There are two blocks defined in this template:

* ``title`` - This is reserved for the title of the page (that shows up in the web browser tab)

* ``content`` - This is where the entirety of the page content is contained

A style sheet is also automatically linked (``static/stylesheets/stylesheet.css``), so styles defined in that sheet will apply to all
pages that inherit from ``template.html``.

There is also a navigation bar with the title/name of the application and links to the "Home" and "About" pages.

Index Template
--------------

File: ``index.html``

The two blocks from the base template are defined with the following data:

* ``title``: ``"Home"``

* ``content``: At the moment this is just two buttons for the geographic and aeronautical (or sectional chart) maps

About Template
--------------

File: ``about.html``

The two blocks from the base template are defined with the following data:

* ``title``: ``"About"``

* ``content``: TODO (nothing at the moment)

Map Templates
-------------

Directory: ``map``

This is where the templates for the geographic and aeronautical maps are stored.

**These templates do not extend from ``template.html``, so styles and block definitions will differ between them.**

Geographic Map
^^^^^^^^^^^^^^

File: ``geographic_map.html``

Since this template is completely independent from the other pages, there are no blocks or base templates defined or used.

There is a stylesheet specifically for this map that is linked (``static/stylesheets/map.css``) along with the stylesheet for
Leaflet.

There are three scripts linked in the head:

1. Leaflet library (Leaflet.js)

2. JQuery library (``static/vendor/jquery-3.7.0.min.js``)

3. Leaflet Rotated Marker Extension (``static/vendor/leaflet.rotatedMarker.js``)

There are two more scripts linked in the body of the document:

1. Static asset for map initialization and icon rendering and overall app functionalities (``static/js/map.js``)

2. An inline script to initialize selectors, icons, HTTP requests, and start the main loop of the app

Aeronautical Map
^^^^^^^^^^^^^^^^

File: ``sectional_map.html``

TODO; this is unimplemented at the moment.
