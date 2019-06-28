#!/usr/bin/env python3

from rssbot2 import rssbot2

rssbot = rssbot2()

print("Title: {}". format(rssbot.title))
print("Agent: {}". format(rssbot.user_agent))
print("Max Feeds: {}". format(rssbot.max_feeds))

rssbot.db_connect()
feeds = rssbot.get_feeds()
