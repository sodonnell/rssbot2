#!/usr/bin/env python3

from rssbot2 import rssbot2

url = input("Enter an RSS Feed URL: ")
active = input("Activate Feed for Scraping? (Y/N): ")

if active != "Y":
    active = "N"

rssbot = rssbot2()
rssbot.db_connect()
feed_id = rssbot.add_feed(url,active)

if feed_id == 0:
    print("Feed already exists in database. Command ignored.")
else:
    print("Feed successfully added to the database. ID: {}". format(feed_id))
