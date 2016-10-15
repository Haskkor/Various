import requests
import smtplib
import json
import datetime
import sched
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# API
url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyBDi8VT0DWJOiK8b3ditTZUfzHF1_4MELY"
headers = {'content-type': 'application/json'}
google_app_pwd = "gkpkqtmaxlonnrry"

# VARIABLES
FROM = "PAR"
TO = "AKL"
DATE = "2017-06-05"
PASSENGERS = 1
SOLUTIONS = 2
MY_MAIL = "haskkor@gmail.com"
TO_MAIL = "haskkor@gmail.com"
f_name = "results_flight_price_tracking.txt"
AlERT_PRICE = 750

# MAIL
def send_mail():
    """
    Sends a mail with the output file
    """
    fromaddr = MY_MAIL
    toaddr = TO_MAIL
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "[BILLETS D'AVION] Alertes prix"
    body = "Liste des dernieres recherches de billets.\n\nDepart : {}\nArrivee : {}\nDate : {}".format(FROM, TO, DATE)
    msg.attach(MIMEText(body, 'plain'))
    filename = f_name
    attachment = open(f_name, "r")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, google_app_pwd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# REQUEST
def look_for_prices():
    """
    Execute the request and write the result in the output file
    """
    params = {
      "request": {
        "slice": [
          {
            "origin": FROM,
            "destination": TO,
            "date": DATE,
            "maxStops": 5,
            "maxConnectionDuration": 1000
          }
        ],
        "passengers": {
          "adultCount": PASSENGERS
        },
        "solutions": SOLUTIONS+1,
        "refundable": False
      }
    }
    response = requests.post(url, data=json.dumps(params), headers=headers)
    data = response.json()
    
    # RESPONSE IN FILE
    out_file = open(f_name, 'w')
    send_alert = False
    for i in range(SOLUTIONS):
        out_file.write("VOL : {}\n".format(i+1))
        out_file.write("Date de la recherche : {}\n".format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))
        out_file.write("Compagnie principale : {}\n".format(data["trips"]["data"]["carrier"][i]["name"]))
        out_file.write("Prix total : {}e\n".format(data["trips"]["tripOption"][i]["saleTotal"][3:]))
        out_file.write("Duree totale du vol : {}h {}m\n".format((data["trips"]["tripOption"][i]["slice"][0]
                                                                 ["duration"] // 60),
                                                                (data["trips"]["tripOption"][i]["slice"][0]
                                                                 ["duration"] % 60)))
        out_file.write("Aeroport de depart : {}\n".format(data["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"][0]
                                                          ["origin"]))
        out_file.write("Heure de depart : {} {} {}\n".format(data["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"]
                                                             [0]["departureTime"][:10],
                                                             data["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"]
                                                             [0]["departureTime"][11:16],
                                                             data["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"]
                                                             [0]["departureTime"][17:21]))
        out_file.write("Aeroport d'arrivee : {}\n".format(data["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"][0]
                                                          ["destination"]))
        out_file.write("Heure d'arrivee : {} {} {}\n".format(data["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"]
                                                             [0]["arrivalTime"][:10],
                                                             data["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"]
                                                             [0]["arrivalTime"][11:16],
                                                             data["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"]
                                                             [0]["arrivalTime"][17:21]))
        out_file.write("Duree du vol : {}h {}m\n".format((data["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"][0]
                                                          ["duration"] // 60),
                                                         (data["trips"]["tripOption"][i]["slice"][0]["segment"][0]["leg"][0]
                                                          ["duration"] % 60)))
        out_file.write("Duree de la correspondance : {}h {}m\n".format((data["trips"]["tripOption"][i]["slice"][0]
                                                                        ["segment"][0]["connectionDuration"] // 60),
                                                                       (data["trips"]["tripOption"][i]["slice"][0]
                                                                        ["segment"][0]["connectionDuration"] % 60)))
        out_file.write("Heure de depart : {} {} {}\n".format(data["trips"]["tripOption"][i]["slice"][0]["segment"][1]["leg"]
                                                             [0]["departureTime"][:10],
                                                             data["trips"]["tripOption"][i]["slice"][0]["segment"][1]["leg"]
                                                             [0]["departureTime"][11:16],
                                                             data["trips"]["tripOption"][i]["slice"][0]["segment"][1]["leg"]
                                                             [0]["departureTime"][17:21]))
        out_file.write("Aeroport d'arrivee : {}\n".format(data["trips"]["tripOption"][i]["slice"][0]["segment"][1]["leg"][0]
                                                          ["destination"]))
        out_file.write("Heure d'arrivee : {} {} {}\n".format(data["trips"]["tripOption"][i]["slice"][0]["segment"][1]["leg"]
                                                             [0]["arrivalTime"][:10],
                                                             data["trips"]["tripOption"][i]["slice"][0]["segment"][1]["leg"]
                                                             [0]["arrivalTime"][11:16],
                                                             data["trips"]["tripOption"][i]["slice"][0]["segment"][1]["leg"]
                                                             [0]["arrivalTime"][17:21]))
        out_file.write("Duree du vol : {}h {}m\n\n".format((data["trips"]["tripOption"][i]["slice"][0]["segment"][1]["leg"][0]
                                                          ["duration"] // 60),
                                                         (data["trips"]["tripOption"][i]["slice"][0]["segment"][1]["leg"][0]
                                                          ["duration"] % 60)))
        if float(data["trips"]["tripOption"][i]["saleTotal"][3:]) <= AlERT_PRICE:
            send_alert = True
    out_file.close()
    if send_alert:
        send_mail()
    reschedule()

# SCHEDULER
scheduler = sched.scheduler(time.time, time.sleep)
def reschedule():
    new_target = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    new_target += datetime.timedelta(hours=1)
    scheduler.enterabs(new_target.timestamp(), priority=0, action=look_for_prices)

reschedule()
try:
    scheduler.run(blocking=True)
except KeyboardInterrupt:
    print('Stopped.')

# https://developers.google.com/qpx-express/v1/trips/search
