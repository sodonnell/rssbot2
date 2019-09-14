#!/usr/bin/env python3
import sys, getopt
from rssbot2 import rssbot2

url = None
active = None

# let user define db credentials via input
opts, args = getopt.getopt(sys.argv[1:],"adu:",["url=","--help"])

for opt, arg in opts:
    if opt == '--help':
        print('add_feed.py -u https://somefeed.com/rss/ -a Y')
        sys.exit()
    elif opt in ("-u", "--url"):
        url = arg
    elif opt in ("-a"):
        active = "Y"
    elif opt in ("-d"):
        active = "N"

if url is None:
    url = input("Enter an RSS Feed URL: ")

if active is None:
    active = input("Activate Feed for Scraping? (Y/N): ")

# force active to by N, if not Y. Lazy, I know.
if active != "Y":
    active = "N"

rssbot = rssbot2()
rssbot.db_connect()

feed_id = rssbot.add_feed(url,active)

if feed_id == -1:
    print("HTTP Request Error. Process halted.")
elif feed_id == 0:
    print("Feed could not be parsed properly.")
else:
    print("Feed successfully added to the database. ID: {}". format(feed_id))
