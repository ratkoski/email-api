import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import os
from dotenv import load_dotenv
import re

load_dotenv()
# Importing from file .env needed values
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
weather_api = os.getenv("WEATHER_API")


def fetch_bitcoin_rate():
    # Making a request to the CoinDesk API to fetch the current bitcoin rate
    btc = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(btc)
    if response.status_code == 200:
        btc_rate_str = response.json()["bpi"]["USD"]["rate"]
        btc_rate = float(btc_rate_str.replace(",", ""))
        return btc_rate
    else:
        raise Exception(
            "Something went wrong with fetching Bitcoin rate from CoinDesk API"
        )


def fetch_weather():
    # Making a request to the weather API to fetch weather information
    weather_url = "https://api.openweathermap.org/data/2.5/weather?"
    city = "Białystok"
    weather = weather_url + "appid=" + weather_api + "&q=" + city
    response = requests.get(weather)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            "Something went wrong with fetching weather information from the API"
        )


def create_btc_msg(btc_rate, mail_receiver):
    # Create the message for btc information
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = mail_receiver
    msg["Subject"] = "Bitcoin rate"
    body = f"Current bitcoin rate: {btc_rate}$"
    msg.attach(MIMEText(body, "plain"))
    return msg


def create_weather_msg(weather_info, mail_receiver):
    # Create the message for weather information
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = mail_receiver
    msg["Subject"] = "Weather Update"
    # Getting informations about the weather
    temp_celsius = weather_info["main"]["temp"] - 273.15
    wind_speed = weather_info["wind"]["speed"]
    humidity = weather_info["main"]["humidity"]
    body = f"Today's weather is: \nTemperature:{temp_celsius:.2f} °C\nWind speed: {wind_speed} m/s\nHumidity: {humidity}%"
    msg.attach(MIMEText(body, "plain"))
    return msg


def is_valid_email(email):
    # Regex for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)


def main(option, mail_receiver):
    if option not in ["bitcoin", "weather"]:
        print("Invalid option. Please choose either 'bitcoin' or 'weather'.")
        sys.exit(1)

    if not is_valid_email(mail_receiver):
        print("Invalid email address.")
        sys.exit(1)

    # Fetch the information based on the option
    if option == "bitcoin":
        btc_rate = fetch_bitcoin_rate()
        message = create_btc_msg(btc_rate, mail_receiver)
    else:
        weather_info = fetch_weather()
        message = create_weather_msg(weather_info, mail_receiver)

    # Establishing a secure connection and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, mail_receiver, message.as_string())
        print("Email sent successfully!")
    except Exception:
        print("Error sending email")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("You need to place two arguments bitcion or weather and a mail receiver")
        sys.exit(1)
    option = sys.argv[1]
    mail_receiver = sys.argv[2]
    main(option, mail_receiver)


# keybinds that i'm currently using:
# alt + up or down - moves selected lines up or down
# ctrl + shift + k - deletes the whole line instead of deleting it line by line
# ctrl + l - selecting whole line (then you can easly copy it and paste it wherever you want)
# ctrl + shift + p - to open a command palette
# ctrl + alt + up or down - i'm using this for indentation if i need to move more than one line
# shift + tab - to remove the indentation
