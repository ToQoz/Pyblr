#!/usr/bin/env python
#-*- coding: utf-8 -*-
import unittest
import pyblr
import oauth2 as oauth
import json

class TestPyblr(unittest.TestCase):
    def assertNotRaise(self, excClass, callable_, *args, **kwargs):
        try:
            callable_(*args, **kwargs)
        except excClass:
            if hasattr(excClass,'__name__'): excName = excClass.__name__
            else: excName = str(excClass)
            self.fail("unexpected exception raised: %s" % excName)

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

    def test_parse_params(self):
        self.assertEqual(
            self.client.parse_params(self.params),
            self.parsed_params
        )

    def test_APIError(self):
        self.assertNotRaise(pyblr.APIError, lambda: self.client.parse_response(self.create_response('200', 'OK')))
        self.assertNotRaise(pyblr.APIError, lambda: self.client.parse_response(self.create_response('300', 'Found')))
        self.assertRaises(pyblr.APIError, lambda: self.client.parse_response(self.create_response('401', 'Not Authorized')))
        self.assertRaises(pyblr.APIError, lambda: self.client.parse_response(self.create_response('404', 'Not Found')))

if __name__ == '__main__':
    unittest.main()
