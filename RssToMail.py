#!/usr/bin/env python3

import feedparser
import datetime
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("RSS TO MAIL " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " ...")

# Variables
today_articles = list()
year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day
hour = sys.argv[1]
mail = "YOUR_MAIL"
pwd = "YOUR_PWD"

# Websites to check
feed_list = ['http://feeds2.feedburner.com/LeJournalduGeek',
             'https://www.geeksaresexy.net/feed/',
             'http://korben.info/feed',
             'http://www.laboiteverte.fr/feed/',
             'https://www.wired.com/feed/',
             'http://www.infoworld.com/index.rss',
             'http://planetpython.org/rss20.xml',
             'https://www.reddit.com/r/Python/.rss',
             'https://www.reddit.com/r/coding/.rss',
             'https://www.reddit.com/r/programming/.rss',
             'http://www.penofchaos.com/naheulbeukrss.xml',
             'http://www.futura-sciences.com/rss/actualites.xml',
             'http://www.futura-sciences.com/rss/dossiers.xml',
             'http://www.futura-sciences.com/rss/definitions.xml',
             'http://www.futura-sciences.com/rss/questions-reponses.xml',
             'http://www.futura-sciences.com/rss/photos.xml',
             'http://www.futura-sciences.com/rss/services/fonds-ecran.xml',
             'http://www.futura-sciences.com/rss/services/cartes-virtuelles.xml',
             'http://www.gamekult.com/feeds/actu.html',
             'http://www.tabletopgamingnews.com/feed/',
             'http://www.dicetowernews.com/feed',
             'http://www.boardgamequest.com/feed/',
             'https://www.smashingmagazine.com/feed/']

colors = ['#FFA405', '#C19659', '#F3951B', '#E5C39F', '#BE9B7C',
          '#6495ED', '#B3DDED', '#6D8DBE', '#2676AD', '#C9DEE9', '#D185B7',
          '#648637', '#50C878', '#90ee90', '#77DD99', '#AADD77', '#9AFF9A', '#9BCD9B',
          '#FDFDAF', '#FCFC64', '#FDFD96', '#FDE396', '#ECFD96']

# Gathering feeds
for j in range(len(feed_list)):
    d = feedparser.parse(feed_list[j])
    for i in range(len(d.entries)):
        post = d.entries[i]
        if "published_parsed" in post:
            if (post.published_parsed.tm_year == year and
                post.published_parsed.tm_mon == month and
                post.published_parsed.tm_mday == day and
                post.published_parsed.tm_hour > int(hour)):
                tr = "<tr style=\"background-color:" + colors[j] + ";\">"
                today_articles.append(tr + "<td>{}</td><td>{}</td><td>{}</td><td><a href={}>Go</a></td></tr>".format(d['feed']['title'], post.published[0:-5], post.title, post.link))
        else:
            if ("updated_parsed" in post and
                post.updated_parsed.tm_year == year and
                post.updated_parsed.tm_mon == month and
                post.updated_parsed.tm_mday == day and
                post.updated_parsed.tm_hour > int(hour)):
                tr = "<tr style=\"background-color:" + colors[j] + ";\">"
                today_articles.append(tr + "<td>{}</td><td>{}</td><td>{}</td><td><a href={}>Go</a></td></tr>".format(d['feed']['title'], post.updated[0:-5], post.title, post.link))

                
# Send a mail
msg = MIMEMultipart()
msg['From'] = mail
msg['To'] = mail
msg['Subject'] = "[RSS FEEDS] News - {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
html = "<html><head><p>NEWS LIST</p><style>table{width:100%;max-width:100%;margin-bottom:20px;"
html += "border-collapse:collapse;}th{padding:8px;line-height:1.42857143;color:#337ab7;"
html += "text-align:left;vertical-align:bottom;}td{font-size:0.8em;padding:8px;line-height:1.42857143;"
html += "vertical-align:top;border-top:1px solid #ddd;}tr{padding:8px;line-height:1.42857143;"
html += "vertical-align:top;border-top:1px solid #ddd;}</style></head><body><table>"
html += "<tr style=\"background-color:antiquewhite;\"><th>Website</th><th>Date</th><th>Title</th>"
html += "<th>Link</th></tr>{}</table></body></html>".format(''.join(today_articles))
msg.attach(MIMEText(html, 'html'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(mail, pwd)
text = msg.as_string()
server.sendmail(mail, mail, text)
server.quit()

print("OK\n")

# http://www.elbakin.net/rss.php



