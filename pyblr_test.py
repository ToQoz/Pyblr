from nose.tools import *
import oauth2 as oauth
import pyblr

class PyblrTest:
    def __init__(self):
        self.api_key = 'consumer key'
        self.consumer = oauth.Consumer(self.api_key, 'consumer secret')
        self.access_token = oauth.Token('oauth token', 'oauth token secret')
        self.client = pyblr.Pyblr(oauth.Client(self.consumer, self.access_token))
    def info_test(self):
#self.client.
        pass
    def followers_test(self):
        pass
    def posts_test(self):
        pass
    def queue_test(self):
        pass
    def draft_test(self):
        pass
    def submission_test(self):
        pass
    def create_post_test(self):
        pass
    def edit_post_test(self):
        pass
    def reblog_post_test(self):
        pass
    def delete_post_test(self):
        pass
    def dashboard(self):
        pass
    def likes(self):
        pass
    def following_test(self):
        pass
    def follow_test(self):
        pass
    def unfollow(self):
        pass
    def info_user_test(self):
        pass
