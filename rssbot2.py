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
        self.set_root_url("http://www.rssbot.org/")
        self.set_useragent("rssbot/2.0 +%s" % self.root_url)
        self.set_max_feeds(250)
        #self.db_connect()
        #self.get_feeds()
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
        sql = "SELECT title, link, id FROM rssbot2_feeds WHERE active = 'Y' ORDER BY RAND() LIMIT 0, {} "
        cursor = self.conn.cursor()
        cursor.execute(sql, format(self.max_feeds))
        self.feeds = cursor.fetchall()
        self.feeds_count = cursor.rowcount
        cursor.close()

    def deactivate_feed(self,id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE rssbot2_feeds SET active = 'N' WHERE id = %s",id)
        cursor.close()
        print("Feed %d de-activated.", id)
        
    def add_link(self,feed_id,title,link):
        title = title.replace(';','')
        link = link.replace(';','')
        cursor = self.conn.cursor()

        sql = "INSERT IGNORE INTO rssbot2_archive ( title, link, feed_id) VALUES (%s,%s,%s)"
        cursor.execute(sql, (title,link,feed_id))

        self.conn.commit()
        id = cursor.lastrowid
        cursor.close()
        return id

    def add_link_if_not_exists(self,feed_id,title,link,pubdate=''):
        title = title.replace(';','')
        link = link.replace(';','')
        cursor = self.conn.cursor()
        sql = "SELECT count(id) AS existing_id FROM rssbot2_archive WHERE link = '%s'"
        cursor.execute(sql,link)
        self.existing_link = cursor.fetchall()
        cursor.close()

        if self.existing_link.existing_id < 1:
            cursor = self.conn.cursor()

            sql = "INSERT IGNORE INTO rssbot2_archive ( title, link, feed_id) VALUES (%s,%s,%s,)"
            cursor.execute(sql, (title,link,feed_id))

            self.conn.commit()
            id = cursor.lastrowid
            cursor.close()
            return id
        else:
            return 0