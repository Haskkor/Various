#!/usr/bin/env python3

import feedparser
import datetime

d = feedparser.parse('http://www.gamekult.com/feeds/actu.html')
feedparser.registerDateHandler("W3CDTF")

#print(d['feed']['title'])

#print(d['feed']['link'])

#print(d.feed.subtitle)

#print(len(d['entries']))

#print(d['entries'][0]['title'])

#print(d.entries[0]['link'])

year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day

for post in d.entries:
    if post.published_parsed[0] == year and post.published_parsed[1] == month and post.published_parsed[2] == 18:
        print(post.published + " --> " + post.title + ": " + post.link + "")
