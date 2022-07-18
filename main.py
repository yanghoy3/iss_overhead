import requests
from datetime import datetime
import time
import smtplib

sender_email = "yanghoy3@gmail.com"
password = "yaztaldzooylncrk"
receiver_email = "yanghoy3@gmail.com"

MY_LAT = 43.905870  # Your latitude
MY_LONG = -79.478271  # Your longitude


def iss_above_me():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 < iss_latitude < MY_LAT + 5 and MY_LONG - 5 < iss_longitude < MY_LONG + 5:
        return True
    else:
        return False


def is_dark():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    time_now = datetime.now()

    sunrise = (int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 24 - 4) % 24
    sunset = (int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 24 - 4) % 24

    if sunset < time_now.hour or sunrise > time_now.hour:
        return True
    else:
        return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


while True:

    if iss_above_me() and is_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()  # encrypts message
            connection.login(user=sender_email, password=password)
            connection.sendmail(from_addr=sender_email,
                                to_addrs=receiver_email,
                                msg="Subject:Quote of the Week\n\nISS currently flying over your head"
                                )
    time.sleep(60)


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



