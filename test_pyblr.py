#!/usr/bin/env python
#-*- coding: utf-8 -*-
from nose.tools import *
import pyblr
import oauth2 as oauth
import json



class TestPyblr:
    def setUp(self):
        self.api_key = 'consumer key'
        self.consumer = oauth.Consumer(self.api_key, 'consumer secret')
        self.access_token = oauth.Token('oauth token', 'oauth token secret')
        self.client = pyblr.Pyblr(oauth.Client(self.consumer, self.access_token))
        self.params = {
            "name": "toqoz",
            "sex": "male"
        }
        self.parsed_params = "name=toqoz&sex=male"

    def assert_not_raise(self, excClass, callable_, *args, **kwargs):
        try:
            callable_(*args, **kwargs)
        except excClass:
            if hasattr(excClass,'__name__'): excName = excClass.__name__
            else: excName = str(excClass)
            message = "Against the expectationm Raised %s" % (excClass)
            raise AssertionError(message)

    def create_response(self, status, msg):
        result = (
            {},
            json.dumps({
                "meta": {
                    "status": status,
                    "msg": msg
                },
                "response": {}
            })
        )
        return result

    def parse_params_test(self):
        assert_equals(
            self.client.parse_params(self.params),
            self.parsed_params
        )

    def APIError_test(self):
        self.assert_not_raise(pyblr.APIError, lambda: self.client.parse_response(self.create_response('200', 'OK')))
        self.assert_not_raise(pyblr.APIError, lambda: self.client.parse_response(self.create_response('300', 'Found')))
        assert_raises(pyblr.APIError, lambda: self.client.parse_response(self.create_response('401', 'Not Authorized')))
        assert_raises(pyblr.APIError, lambda: self.client.parse_response(self.create_response('404', 'Not Found')))
