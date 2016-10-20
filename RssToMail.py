#!/usr/bin/env python3

import feedparser
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("RSS TO MAIL " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " ...")

# Variables
today_articles = list()
year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day

# Websites to check
feed_list = ['http://feeds2.feedburner.com/LeJournalduGeek',
             'http://www.gamekult.com/feeds/actu.html',
             'https://www.geeksaresexy.net/feed/',
             'http://korben.info/feed',
             'http://www.penofchaos.com/naheulbeukrss.xml']

# Gathering feeds
for feed in feed_list:
    d = feedparser.parse(feed)
    for post in d.entries:
        if (post.published_parsed.tm_year == year and
            post.published_parsed.tm_mon == month and
            post.published_parsed.tm_mday == day):
            today_articles.append("<tr><td>{}</td><td>{}</td><td>{}</td><td><a href={}>Go</a></td></tr>".format(d['feed']['title'], post.published[0:-5], post.title, post.link))
            
# Send a mail
msg = MIMEMultipart()
msg['From'] = "haskkor@gmail.com"
msg['To'] = "haskkor@gmail.com"
msg['Subject'] = "[RSS FEEDS] News - {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
html = """\
<html>
    <head>
        NEWS LIST
    </head>
    <body>
        <table>
            <tr>
                <th>Website</th>
                <th>Date</th>
                <th>Title</th>
                <th>Link</th>                
            </tr>
            {}
        </table
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

# http://www.elbakin.net/rss.php



