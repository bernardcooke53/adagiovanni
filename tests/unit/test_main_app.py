# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

from tests.util import HTTPMethods, http_method_round_robin, not_found_all_methods


def test_app_get_home(test_app):
    test_map = {HTTPMethods.GET: (200, {"message": "Welcome to Giovanni's!"})}
    return http_method_round_robin(test_app, "/", test_map)


def test_app_ping(test_app):
    test_map = {HTTPMethods.GET: (200, {"ping": "pong"})}
    return http_method_round_robin(test_app, "/ping", test_map)


def test_app_docs_disabled(test_app):
    return not_found_all_methods(test_app, "/docs")


def test_app_get_non_existent(test_app):
    return not_found_all_methods(
        test_app, "/this/route/definitely/should/not/exist/andthisisjusttomakesure"
    )
