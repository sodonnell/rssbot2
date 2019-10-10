#!/usr/bin/env python3
import sys, getopt, banner
from rssbot2 import rssbot2

url = None
active = None

# let user define the feed url and active-state via args
opts, args = getopt.getopt(sys.argv[1:],"adu:",["url=","help"])

for opt, arg in opts:
    if opt == '--help':
        print('Add an active feed:\n')
        print('\tpython3 add_feed.py -u https://somefeed.com/rss/ -a\n')
        print('Add a de-activated feed:\n')
        print('\tpython3 add_feed.py -u https://somefeed.com/rss/ -d\n')
        sys.exit()
    elif opt in ("-u", "--url"):
        url = arg
    elif opt in ("-a"):
        active = "Y"
    elif opt in ("-d"):
        active = "N"

print(banner.rssbot_logo)

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

#
# @todo fix this algorithm. 
#
# - Python needs a default switch/case procedure. 
# - feedparser and rssbot need better exception handling.
#
if feed_id == -1:
    print("HTTP request error. Process halted.")
elif feed_id == -2:
    print("Feed already exists. Process halted.")
elif feed_id == -3:
    print("Feed status updated.")
elif feed_id == 0:
    print("Feed could not be parsed properly.")
else:
    print("Feed successfully added to the database. ID: {}". format(feed_id))
