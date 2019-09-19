#!/usr/bin/env python3
import feedparser, banner
from rssbot2 import rssbot2

rssbot = rssbot2()

print(banner.rssbot_logo)
print("--------------------------")
print("Title: {}". format(rssbot.title))
print("Agent: {}". format(rssbot.user_agent))
print("Max Feeds: {}". format(rssbot.max_feeds))

rssbot.db_connect()
rssbot.get_feeds()

# iteration cursors (yuck)
i=0 # iterations
p=0 # links processed
a=0 # links added

if rssbot.feeds_count > 0:
    print("Aggregating {} Feeds". format(rssbot.feeds_count))

    for feed in rssbot.feeds:
        rss = feedparser.parse(feed[1],referrer=rssbot.root_url)
        if rssbot.debug:
            print("--------------------------")
            print("RSS Feed Title: {}". format(rss.feed.title))
            if (rss.feed.has_key('link')):
                print("RSS Feed URL: {}". format(rss.feed.link))
        try: rss.status
        except: 
            print('HTTP Status not found.')
        else: 
            http_status = "HTTP Response Status Code: %d" % (rss.status)
            print(http_status)
            if rss.feed.has_key('title'):
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
                                    a=a+1
                            except:
                                print("Exception thrown while processing item.")

                            p=p+1
            else:
                rssbot.deactivate_feed(feed[2])
            
        i=i+1

rssbot.conn.close()

print("--------------------------")
print("Processed feeds: {}". format(i))
print("Processed items: {}". format(p))
print("Added new links: {}". format(a))
