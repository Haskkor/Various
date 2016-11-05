import newspaper
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Variables
now = datetime.now().date()
today_articles = list()

# Websites list multithreading
gas_paper = newspaper.build('https://www.geeksaresexy.net/')
jdg_paper = newspaper.build('http://www.journaldugeek.com/')
kb_paper = newspaper.build('http://korben.info/')
gk_paper = newspaper.build('http://www.gamekult.com/actu/jeux-video.html?date=' + str(now))
ebk_paper = newspaper.build('http://www.elbakin.net/')
bm_paper = newspaper.build('http://dites.bonjourmadame.fr/')
papers = [gas_paper, jdg_paper, kb_paper, gk_paper, ebk_paper, bm_paper]
newspaper.news_pool.set(papers, threads_per_source=2)
newspaper.news_pool.join()

# Gathering articles
for paper in papers:
    for article in paper.articles:
        print(article.url)
        if article.publish_date is not None and article.url[-5:] != "feed/" and article.url[-12:] != "#dsq-content":
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
        
# RSS Reader with Bottle : https://github.com/MickaelG/simple_rss_reader
