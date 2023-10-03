Endpoint Blueprints
===================

.. _Flask Blueprints: https://flask.palletsprojects.com/en/latest/blueprints/

The API endpoints and page endpoints are implemented and served using `Flask Blueprints`_, since the core of the application
revolves around Flask.

Presently, there are five groups of endpoints either planned or currently implemented in the application:

* ``index`` - The landing/home page of the application.

* ``about`` - The about page(s) of the applications. These pages contain everything from description of the application and its functionalities to its design and implementation details.

* ``data`` - The data API endpoint. This provides data services that are needed e.g. for creating the plane icons on the maps. This endpoint loads and serves the data directly and provides wrappers for other APIs where necessary.

* ``map`` - The map pages and API endpoints.

* ``models`` - The ASR and NLP model endpoints.

The root of each of these endpoints serves either a home page (e.g. the templates rendered and returned from ``index`` and ``about``) or an API and/or endpoint status when a homepage is not necessary or has not been created.

For more information about the endpoints grouped under the above blueprints, see the :ref:`endpoints-api-reference`.