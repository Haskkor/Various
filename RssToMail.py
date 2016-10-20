#!/usr/bin/env python3

import feedparser
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("RSS TO MAIL " + str(datetime.datetime.now()) + " ...")

# Variables
feedparser.registerDateHandler("W3CDTF")
today_articles = list()
year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day

# Websites to check
#feed_list = ['http://www.gamekult.com/feeds/actu.html',
#             'http://http://www.journaldugeek.com/feed/',
#             'https://www.geeksaresexy.net/feed/',
#             'http://korben.info/feed',
#             'http://www.elbakin.net/rss.php',
#             'http://www.penofchaos.com/naheulbeukrss.xml']

# Gathering feeds
#for feed in feed_list:
#    d = feedparser.parse(feed)
#    for post in d.entries:
#        if post.published_parsed[0] == year and \
#           post.published_parsed[1] == month and \
#           post.published_parsed[2] == day:
#            today_articles.append("<li><a href={}>{} - {}</a></li>".format(post.link, d['feed']['title'], post.title))


##### TESTER TOUS LES SITES EN HTTPS

d = feedparser.parse('https://www.gamekult.com/feeds/actu.html')
for post in d.entries:
    if post.published_parsed[0] == year and \
       post.published_parsed[1] == month and \
       post.published_parsed[2] == day:
       today_articles.append("<li><a href={}>{} - {}</a></li>".format(post.link, d['feed']['title'], post.title))







# Send a mail
msg = MIMEMultipart()
msg['From'] = "haskkor@gmail.com"
msg['To'] = "haskkor@gmail.com"
msg['Subject'] = "[RSS FEEDS] News - {}".format(datetime.datetime.now())
html = """\
<html>
    <head>
        NEWS LIST
    </head>
    <body>
        <ul>
            {}
        </ul>
    </body>
</html>
""".format(''.join(today_articles))
msg.attach(MIMEText(html, 'html'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("haskkor@gmail.com", "gkpkqtmaxlonnrry")
text = msg.as_string()
server.sendmail("haskkor@gmail.com", "haskkor@gmail.com", text)
server.quit()

print("OK\n")

#print(d['feed']['title'])
#print(d['feed']['link'])
#print(d.feed.subtitle)
#print(len(d['entries']))
#print(d['entries'][0]['title'])
#print(d.entries[0]['link'])




