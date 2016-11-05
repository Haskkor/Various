#!/usr/bin/env python3

import requests
import smtplib
import sys
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("DRIVING TRAVEL TIME START " + str(datetime.datetime.now()) + " ...")

# VARIABLES
my_mail = "MAIL"
to_mail = "MAIL"
api_id = "YOUR_ID"
google_app_pwd = "YOUR_PWD"
origin_lat = sys.argv[1]
origin_lon = sys.argv[2]
destination_lat = sys.argv[3]
destination_lon = sys.argv[4]

# MAIL
def send_mail(content):
    """
    Sends a mail with the travel details
    """
    msg = MIMEMultipart()
    msg['From'] = my_mail
    msg['To'] = to_mail
    msg['Subject'] = "[ALERTES TRAJET] Temps de trajet et étapes"
    body = "<b>Nouvelle alerte de trajet :</b><br><br>"
    body += content
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_mail, google_app_pwd)
    text = msg.as_string()
    server.sendmail(my_mail, to_mail, text)
    server.quit()

# REQUEST
url = \
    "https://maps.googleapis.com/maps/api/directions/json?origin={},{}&destination={},{}&departure_time={}&" \
    "traffic_model=best_guess&key={}&language=fr&units=metric".format(origin_lat, origin_lon, destination_lat,
                                                                      destination_lon, "now", api_id)
response = requests.post(url)
data = response.json()

content = "Adresse de départ : {}<br>".format(data["routes"][0]["legs"][0]["start_address"])
content += "Adresse d'arrivée : {}<br>".format(data["routes"][0]["legs"][0]["end_address"])
content += "Durée du trajet : <font color=\"red\">{}</font><br>".format(data["routes"][0]["legs"][0]["duration"]
                                                                        ["text"])
content += "Durée estimée du trajet : <font color=\"red\">{}</font><br>".format(data["routes"][0]["legs"][0]
                                                                                ["duration_in_traffic"]["text"])
content += "Distance : {}<br><br>".format(data["routes"][0]["legs"][0]["distance"]["text"])
content += "Trajet : <br><br>"
for i in range(len(data["routes"][0]["legs"][0]["steps"])):
    content += "Etape {} :<br>".format(i+1)
    content += "Distance : {}<br>".format(data["routes"][0]["legs"][0]["steps"][i]["distance"]["text"])
    content += "Durée : {}<br>".format(data["routes"][0]["legs"][0]["steps"][i]["duration"]["text"])
    content += "{}<br><br>".format(data["routes"][0]["legs"][0]["steps"][i]["html_instructions"])

send_mail(content)

print("OK\n")
