#!/usr/bin/env python3

import newspaper
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("SITES CHECKING " + str(datetime.now()) + " ...")

# Variables
now = datetime.now().date()
today_articles = list()

# Websites list multithreading
gas_paper = newspaper.build('https://www.geeksaresexy.net/', memoize_articles=True)
jdg_paper = newspaper.build('http://www.journaldugeek.com/', memoize_articles=True)
kb_paper = newspaper.build('http://korben.info/', memoize_articles=True)
gk_paper = newspaper.build('http://www.gamekult.com/actu/jeux-video.html?date=' + str(now), memoize_articles=True)
ebk_paper = newspaper.build('http://www.elbakin.net/', memoize_articles=True)
bm_paper = newspaper.build('http://dites.bonjourmadame.fr/', memoize_articles=True)
papers = [gas_paper, jdg_paper, kb_paper, gk_paper, ebk_paper, bm_paper]
newspaper.news_pool.set(papers, threads_per_source=2)
newspaper.news_pool.join()

# Gathering articles
for paper in papers:
    for article in paper.articles:
        if article.publish_date is not None and article.url[-5:] != "feed/" and article.url[-12:] != "#dsq-content":
            if article.title == None or article.title != "" :
                today_articles.append("<li><a href={}>{} - {}</a></li>".format(article.url, paper.brand, article.url))
            else:
                today_articles.append("<li><a href={}>{} - {}</a></li>".format(article.url, paper.brand, article.title))


today_articles.sort()

# Send a mail
msg = MIMEMultipart()
msg['From'] = "MAIL"
msg['To'] = "MAIL"
msg['Subject'] = "[WEBSITES] News - {}".format(now)
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
server.login("MAIL", "PWD")
text = msg.as_string()
server.sendmail("MAIL", "MAIL", text)
server.quit()

print("OK\n")

# RSS Reader with Bottle : https://github.com/MickaelG/simple_rss_reader
