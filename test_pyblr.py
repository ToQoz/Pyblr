#!/usr/bin/env python
#-*- coding: utf-8 -*-
from nose.tools import *
from minimock import mock, Mock, restore, TraceTracker, assert_same_trace 
import pyblr
import oauth2 as oauth
import json



class TestPyblr:
    def setUp(self):
        self.api_key = "consumer key"
        self.consumer = oauth.Consumer(self.api_key, "consumer secret")
        self.access_token = oauth.Token("oauth token", "oauth token secret")
        self.client = pyblr.Pyblr(oauth.Client(self.consumer, self.access_token))
        self.params = {
            "name": "toqoz",
            "sex": "male"
        }
        self.parsed_params = "name=toqoz&sex=male"
        self.trackar = TraceTracker()
        mock("pyblr.Pyblr.get", tracker=self.trackar)
        mock("pyblr.Pyblr.post", tracker=self.trackar)

    def assert_not_raise(self, excClass, callable_, *args, **kwargs):
        try:
            callable_(*args, **kwargs)
        except excClass:
            if hasattr(excClass,"__name__"): excName = excClass.__name__
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

    # when assert_same_trace
    #  required space between colon(:) and value in dict
    #  [use this two times or more in same method] required call trackar.clear()
    def info_test(self):
        self.client.info("toqoz.tumblr.com")
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/blog/toqoz.tumblr.com/info', %s)
        """ % ({'api_key': self.api_key}))

    def followers_test(self):
        self.client.followers("toqoz.tumblr.com")
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/blog/toqoz.tumblr.com/followers', %s)
        """ % ({}))

        self.trackar.clear()
        self.client.followers("toqoz.tumblr.com", {"limit": 10})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/blog/toqoz.tumblr.com/followers', %s)
        """ % ({'limit': 10}))

    def posts_test(self):
        self.client.posts("toqoz.tumblr.com")
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/blog/toqoz.tumblr.com/posts', %s)
        """ % ({'api_key': self.api_key}))

        self.trackar.clear()
        self.client.posts("toqoz.tumblr.com", {"type": "photo"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/blog/toqoz.tumblr.com/posts', %s)
        """ % ({'api_key': self.api_key, 'type': 'photo'}))

    def queue_test(self):
        self.client.queue("toqoz.tumblr.com")
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/blog/toqoz.tumblr.com/posts/queue', %s)
        """ % ({}))

    def draft_test(self):
        self.client.draft("toqoz.tumblr.com")
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/blog/toqoz.tumblr.com/posts/draft', %s)
        """ % ({}))

    def submission_test(self):
        self.client.submission("toqoz.tumblr.com")
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/blog/toqoz.tumblr.com/posts/submission', %s)
        """ %({}))

    def create_post_test(self):
        self.client.create_post("toqoz.tumblr.com", {'type': 'text', 'body': 'text'})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post', %s)
        """ % ({"type": "text", "body": "text"}))

        self.trackar.clear()
        self.client.create_post("toqoz.tumblr.com", {"type": "photo", "source": "http://example.com/photo.png"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post', %s)
        """ % ({'type': 'photo', 'source': 'http://example.com/photo.png'}))

        self.trackar.clear()
        self.client.create_post("toqoz.tumblr.com", {"type": "quote", "quote": "quote"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post', %s)
        """ % ({'type': 'quote', 'quote': 'quote'}))

        self.trackar.clear()
        self.client.create_post("toqoz.tumblr.com", {'type': 'like', 'url': 'http://example.com/'})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post', %s)
        """ % ({'type': 'like', 'url': 'http://example.com/'}))

        self.trackar.clear()
        self.client.create_post("toqoz.tumblr.com", {"type": "chat", "conversation": "conversation"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post', %s)
        """ % ({'type': 'chat', 'conversation': 'conversation'}))

        self.trackar.clear()
        self.client.create_post("toqoz.tumblr.com", {"type": "audio", "external_url": "http://example.com/audio.mp3"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post', %s)
        """ % ({'type': 'audio', 'external_url': 'http://example.com/audio.mp3'}))

        self.trackar.clear()
        self.client.create_post("toqoz.tumblr.com", {"type": "video", "embed": "<embed>code</embed>"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post', %s)
        """ % ({"type": "video", "embed": "<embed>code</embed>"}))


    def edit_post_test(self):
        self.client.edit_post("toqoz.tumblr.com", {"id": 123456789, "type": "text", "body": "new text"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post/edit', %s)
        """ % ({"id": 123456789, "type": "text", "body": "new text"}))

    def reblog_post_test(self):
        self.client.reblog_post("toqoz.tumblr.com", {"id": 123456789, "reblog_key": "adcdefg"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post/reblog', %s)
        """ % ({"id": 123456789, "reblog_key": "adcdefg"}))

        self.trackar.clear()
        self.client.reblog_post("toqoz.tumblr.com", {"id": 123456789, "reblog_key": "adcdefg", "comment": "comment"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post/reblog', %s)
        """ % ({"id": 123456789, "reblog_key": "adcdefg", "comment": "comment"}))

    def delete_post_test(self):
        self.client.delete_post("toqoz.tumblr.com", {"id": 123456789})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/blog/toqoz.tumblr.com/post/delete', %s)
        """ % ({"id": 123456789}))

    def dashboard_test(self):
        self.client.dashboard()
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/user/dashboard', %s)
        """ % ({}))

        self.trackar.clear()
        self.client.dashboard({"type": "photo"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/user/dashboard', %s)
        """ % ({"type": "photo"}))

    def likes_test(self):
        self.client.likes()
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/user/likes', %s)
        """ % ({}))

        self.trackar.clear()
        self.client.likes({"limit": 10})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/user/likes', %s)
        """ % ({"limit": 10}))

    def following_test(self):
        self.client.following()
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/user/following', %s)
        """ % ({}))

        self.trackar.clear()
        self.client.following({"limit": 10})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/user/following', %s)
        """ % ({"limit": 10}))

    def follow_test(self):
        self.client.follow({"url": "toqoz.tumblr.com"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/user/follow', %s)
        """ % ({"url": "toqoz.tumblr.com"}))

    def unfollow_test(self):
        self.client.unfollow({"url": "toqoz.tumblr.com"})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.post('/v2/user/unfollow', %s)
        """ % ({"url": "toqoz.tumblr.com"}))

    def info_user_test(self):
        self.client.info_user({})
        assert_same_trace(self.trackar, """\
            Called pyblr.Pyblr.get('/v2/user/info', %s)
        """ % ({}))

    def parse_params_test(self):
        assert_equals(self.client.parse_params(self.params), self.parsed_params)

    def APIError_test(self):
        self.assert_not_raise(pyblr.APIError, lambda: self.client.parse_response(self.create_response("200", "OK")))
        self.assert_not_raise(pyblr.APIError, lambda: self.client.parse_response(self.create_response("300", "Found")))
        assert_raises(pyblr.APIError, lambda: self.client.parse_response(self.create_response("401", "Not Authorized")))
        assert_raises(pyblr.APIError, lambda: self.client.parse_response(self.create_response("404", "Not Found")))
