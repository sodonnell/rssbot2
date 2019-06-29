#!/usr/bin/env python3

from rssbot2 import rssbot2

rssbot = rssbot2()

print("Title: {}". format(rssbot.title))
print("Agent: {}". format(rssbot.user_agent))
print("Max Feeds: {}". format(rssbot.max_feeds))

rssbot.db_connect()
rssbot.get_feeds()

if rssbot.feeds_count > 0:
    print "Aggregating %d Feeds\n" % rssbot.feeds_count

    for feed in rssbot.feeds:
        rss = feedparser.parse(feed[1],referrer=rssbot.root_url)
        if rss.feed.has_key('title'):
            if rssbot.debug:
                print "RSS Feed Title: %s" % rss.feed.title.encode('utf-8')
    
            if len(rss.entries) > 0:
                for entry in rss.entries:
                    if entry.has_key('title') and entry.has_key('link'):
    
                        if 'pubDate' in entry:
                            id = rssbot.add_link_if_not_exists(feed[2],entry.title,entry.link,entry.pubDate)
                        else:
                            id = rssbot.add_link_if_not_exists(feed[2],entry.link)

                        try:
                            if id > 0:
                                if rssbot.debug:
                                    print("\nAdded Record (ID): %d") % id
                                    print("\t"+ str(entry.title))
                                    print("\t"+ str(entry.link))
                                k=k+1
                        except:
                            print("Exception thrown while processing item.")

                        j=j+1
        else:
            rssbot.deactivate_feed(feed[2])
            
        i=i+1

rssbot.conn.close()