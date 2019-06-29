#!/usr/bin/env python3

from rssbot2 import rssbot2

url = input("Enter an RSS Feed URL: ")
active = input("Activate Feed for Scraping? (Y/N): ")

if active != "Y":
    active = "N"

rssbot = rssbot2()
rssbot.db_connect()
print(rssbot.add_feed(url,active))
