#!/usr/bin/env python3

from rssbot2 import rssbot

rssbot = rssbot()

print("Title: {}". format(rssbot.title))
print("Agent: {}". format(rssbot.user_agent))