# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

import logging
from enum import Enum

from fastapi import status

log = logging.getLogger(__name__)

# Single point to modify tests if a
# default not found handler is implemented
# NOT_FOUND_JSON_RESPONSE = {"detail": "Not Found"}
NOT_FOUND_JSON_RESPONSE = None


class HTTPMethods(str, Enum):
    """
    Methods per:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
    """

    def __format__(self, __format_spec):
        return str.__format__(self, __format_spec)

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    # FastAPI doesn't implement "CONNECT" like
    # the other verbs here and "TRACE" isn't on
    # the TestClient either.
    TRACE = "TRACE"
    CONNECT = "CONNECT"


def http_method_round_robin(client, endpoint, test_map):
    """
    Given a client, and map of HTTPMethod members
    to 2-tuples (status_code, response), perform
    a round robin assertion that the status codes
    and responses are correct for each supplied method.
    For methods not supplied, assert that the response
    is a 405 METHOD_NOT_ALLOWED.
    """
    for method in HTTPMethods:
        try:
            client_route = getattr(client, method.lower())
        except AttributeError:
            # We'll get some warnings in the test logs for methods
            # that aren't implemented on the TestClient - better to
            # be explicit and actively silence later on than to
            # exclude them upfront and forget later.
            log.warning(
                f"client {client!r} doesn't implement a {method.lower()!r} method",
                exc_info=True,
            )
            continue
        else:
            log.info("Testing %s %r", method.upper(), endpoint)
            response = client_route(endpoint)
            (status_code, response_json) = test_map.get(
                method, (status.HTTP_405_METHOD_NOT_ALLOWED, None)
            )
            log.info("Expecting %d from %s %r", status_code, method.upper(), endpoint)
            assert response.status_code == status_code
            if response_json:
                assert response_json == response.json()


def not_found_all_methods(client, endpoint):
    test_map = {
        method: (status.HTTP_404_NOT_FOUND, NOT_FOUND_JSON_RESPONSE)
        for method in HTTPMethods
    }
    http_method_round_robin(client, endpoint, test_map)
