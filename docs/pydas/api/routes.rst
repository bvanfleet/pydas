sDAS REST API Routes
====================

The routes for the sDAS REST API are defined using :class:`flask.blueprints.Blueprint` objects.
These objects then become decorators over functions that define logic for handling specific
operations performed against the API, e.g. ``GET /acquire/aapl``.

These routes are not dynamically configurable and should not be modified without an
understanding of flask server development.

API documentation is provided via a Swagger endpoint on the sDAS server. This endpoint is
``/api/docs``. This site also supports interacting with the sDAS server without having to
integrate into a front-end client.
