#!/usr/bin/env python3

import feedparser
import datetime

d = feedparser.parse('http://www.gamekult.com/feeds/actu.html')

#print(d['feed']['title'])

#print(d['feed']['link'])

#print(d.feed.subtitle)

#print(len(d['entries']))

#print(d['entries'][0]['title'])

#print(d.entries[0]['link'])

now = datetime.datetime.now()

for post in d.entries:
    print(post.published + " --> " + post.title + ": " + post.link + "")
