#!/usr/bin/env python3
#
# rssbot2.py
#
# Github Repo:
# https://github.com/sodonnell/rssbot2/
#
# Install Requirements:
# $ sudo pip install feedparser mysql-connector-python
#
__version__ = "2.0"
__author__ = "Sean O'Donnell <sean@seanodonnell.com>"

__license__ = "GPL"
__copyright__ = "Copyright 2019, Sean O'Donnell"

import mysql.connector, feedparser, config

class rssbot2:
    def __init__(self):
        # SET DEFAULT OBJECT PARAMS
        self.title = "rssbot2"
        self.set_root_url("https://github.com/sodonnell/rssbot2/")
        self.set_useragent("rssbot/2.0 +%s" % self.root_url)
        self.set_max_feeds(250)
        self.debug = 1

    def set_root_url(self,url):
        # define the root URL for the rssbot.org webUI
        self.root_url = url

    def set_max_feeds(self,int):
        # Maximum number of RSS Feeds to scour per-session (250 max suggested)
        self.max_feeds = int

    def set_useragent(self,agent):
        # define a custom user agent for this application
        self.user_agent = agent
        feedparser.USER_AGENT = agent

    def db_connect(self):
        self.conn = mysql.connector.connect(host=config.db['host'],user=config.db['user'],password=config.db['password'],database=config.db['database'])
        return self.conn

    def get_feeds(self):
        sql = "SELECT title, link, id FROM rssbot2_feeds WHERE active = 'Y' ORDER BY RAND() LIMIT 0, {}".format(self.max_feeds)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.feeds = cursor.fetchall()
        self.feeds_count = cursor.rowcount
        cursor.close()

    def deactivate_feed(self,id):
        sql = "UPDATE rssbot2_feeds SET active = 'N' WHERE id = '{}'". format(id)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()
        print("Feed %d de-activated.", id)

    def activate_feed(self,id):
        sql = "UPDATE rssbot2_feeds SET active = 'Y' WHERE id = '{}'". format(id)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()
        print("Feed %d activated.", id)

    def add_feed(self,link,active='N'):
        # get rss feed data via link
        sql = "select id from rssbot2_feeds where id = '{}'". format(link)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.feed = cursor.fetchone()
        self.feed_count = cursor.rowcount

        if self.feed_count == 0:
            rss = feedparser.parse(link,referrer=self.root_url)
            try: rss.status
            except: 
                print 'HTTP Status not found.'
            else: 
                http_status = "HTTP Response Status Code: %d" % (rss.status)
                print(http_status)
            if rss.feed.has_key('title'):
                rss.feed.title = rss.feed.title.replace("'",r"\'")
                cursor = self.conn.cursor()
                sql = "INSERT IGNORE INTO rssbot2_feeds ( title, link, active) VALUES ('%s','%s','%s')" % (rss.feed.title,link,active)
                cursor.execute(sql)
                self.conn.commit()
                id = cursor.lastrowid
                cursor.close()
                return id
            else:
                return 0
        else:
            return self.feed.id

    def add_link(self,feed_id,title,link):
        cursor = self.conn.cursor()
        title = title.replace("'",r"\'")
        sql = "INSERT IGNORE INTO rssbot2_archive ( title, link, feed_id) VALUES ('%s','%s','%s')" % (title,link,feed_id)
        cursor.execute(sql)
        self.conn.commit()
        id = cursor.lastrowid
        cursor.close()
        return id
