# Pyblr
Pyblr is a simple Tumblr API v2 library written in python

# Example
    #!/usr/bin/env python
    #-*- coding: utf-8 -*-

    import pyblr
    import oauth2 as oauth
    import urllib
    consumer = oauth.Consumer(
            '*** consumer key ***',
            '*** consumer secret ***',
            )
    access_token = oauth.Token(
            '*** oauth token ***',
            '*** oauth token secret ***'
            )

    client = pyblr.Pyblr(oauth.Client(consumer, access_token))
    info = client.info("toqoz.tumblr.com")
    print info["blog"]["title"] #=> Toqoz notes

# Requirements
oauth2
urllib
