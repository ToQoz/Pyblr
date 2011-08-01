#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re, urllib, json
import oauth2 as oauth
class APIError(StandardError):
    def __init__(self, msg, response=None):
        StandardError.__init__(self, msg)

class Pyblr:
    def __init__(self, client):
        self.site = "http://api.tumblr.com"
        self.client = client
        self.set_methods()

    def api_key(self):
        return {"api_key": self.client.consumer.key}

    def api_setting(self):
        api_str = """
          info         /v2/blog/%s/info             api_key get
          followers    /v2/blog/%s/followers        oauth   get
          posts        /v2/blog/%s/posts            api_key get
          queue        /v2/blog/%s/posts/queue      oauth   get
          draft        /v2/blog/%s/posts/draft      oauth   get
          submission   /v2/blog/%s/posts/submission oauth   get
          create_post  /v2/blog/%s/post             oauth   post
          edit_post    /v2/blog/%s/post/edit        oauth   post
          reblog_post  /v2/blog/%s/post/reblog      oauth   post
          delete_post  /v2/blog/%s/post/delete      oauth   post
          dashboard    /v2/user/dashboard           oauth   get
          likes        /v2/user/likes               oauth   get
          following    /v2/user/following           oauth   get
          follow       /v2/user/follow              oauth   post
          unfollow     /v2/user/unfollow            oauth   post
          info_user    /v2/user/info                oauth   get
        """
        return map(lambda x: re.split("\s+", x.strip()),
                             re.split("\n", api_str.strip()))

    def set_methods(self):
        for api_list in self.api_setting():
            api = {}
            api["method_name"], api["path"], api["auth"], api["http_method"] = api_list
            def _method(base_hostname="", params={}, api=api):
                if isinstance(base_hostname, dict):
                    params = base_hostname
                if re.compile("%s").search(api["path"]):
                    api["path"] = api["path"] % base_hostname
                if api["auth"] == "api_key":
                    params = dict(params.items() + self.api_key().items())
                return getattr(self, api['http_method'])(api["path"], params)
            setattr(self, api["method_name"], _method)

    def get(self, path, params = {}):
        return self.parse_response(self.client.request(
                   self.site + path + "?" + self.parse_params(params),
                   "GET",
                   ))

    def post(self, path, params = {}):
        return self.parse_response(self.client.request(
                   self.site + path,
                   "POST",
                   self.parse_params(params)
                   ))

    def parse_params(self, params = {}):
        return  urllib.urlencode(params)

    def parse_response(self, result):
        resp, content = result
        content = json.loads(content)
        if 400 <= int(content["meta"]["status"]) <= 600:
            raise APIError(content["meta"]["msg"], result)
        return content["response"]
