#!/usr/bin/env python3
import feedparser
from rssbot2 import rssbot2

rssbot = rssbot2()

banner = """
     ____  __________ ____        __ 
    / __ \/ ___/ ___// __ )____  / /_
   / /_/ /\__ \\__ \/ __  / __ \/ __/
  / _, _/___/ /__/ / /_/ / /_/ / /_  
 /_/ |_|/____/____/_____/\____/\__/ v2.0

 A simple RSS Crawler written in python.

"""
print(banner)
print("--------------------------")
print("Title: {}". format(rssbot.title))
print("Agent: {}". format(rssbot.user_agent))
print("Max Feeds: {}". format(rssbot.max_feeds))

rssbot.db_connect()
rssbot.get_feeds()

# iteration cursors
i=0
j=0
k=0

if rssbot.feeds_count > 0:
    print("Aggregating {} Feeds". format(rssbot.feeds_count))

    for feed in rssbot.feeds:
        rss = feedparser.parse(feed[1],referrer=rssbot.root_url)
        http_status = "HTTP Response Status Code: %d" % (rss.status)
        print(http_status)
        if rss.feed.has_key('title'):
            if rssbot.debug:
                print("--------------------------")
                print("RSS Feed Title: {}". format(rss.feed.title))
    
            if len(rss.entries) > 0:
                for entry in rss.entries:
                    if entry.has_key('title') and entry.has_key('link'):
    
                        id = rssbot.add_link(feed[2],entry.title,entry.link)

                        try:
                            if id > 0:
                                if rssbot.debug:
                                    print("\nAdded Record {}". format(id))
                                    print(str(entry.title))
                                    print(str(entry.link))
                                k=k+1
                        except:
                            print("Exception thrown while processing item.")

                        j=j+1
        else:
            rssbot.deactivate_feed(feed[2])
            
        i=i+1

rssbot.conn.close()

print("--------------------------")
print("Processed feeds: {}". format(i))
print("Processed items: {}". format(j))
print("Added new links: {}". format(k))