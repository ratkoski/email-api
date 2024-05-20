import pytest
import smtplib
from email.mime.multipart import MIMEMultipart
from mail import fetch_bitcoin_rate, fetch_weather, create_btc_msg, create_weather_msg, main


def test_fetch_bitcoin_rate():
    # Test that fetch_bitcoin_rate() returns a float
    btc_rate = fetch_bitcoin_rate()
    assert isinstance(btc_rate, float)

def test_fetch_weather():
    # Test that fetch_weather() returns a dictionary
    weather_info = fetch_weather()
    assert isinstance(weather_info, dict)

def test_create_btc_msg():
    # Test that create_btc_msg() returns a MIMEMultipart object
    btc_rate = 45000.00  # Assuming Bitcoin rate
    mail_receiver = "radek.gryciukk@gmail.com"
    btc_msg = create_btc_msg(btc_rate, mail_receiver)
    assert isinstance(btc_msg, MIMEMultipart)
    assert btc_msg["To"] == mail_receiver
def test_create_weather_msg():
    # Test that create_weather_msg() returns a MIMEMultipart object
    weather_info = {"main": {"temp": 280.15, "humidity": 50}, "wind": {"speed": 3.5}}
    mail_receiver = "radek.gryciukk@gmail.com"
    weather_msg = create_weather_msg(weather_info, mail_receiver)
    assert isinstance(weather_msg, MIMEMultipart)
    assert weather_msg["To"] == mail_receiver

@pytest.mark.parametrize("option, mail_receiver", [("bitcoin", "radek.gryciukk@gmail.com"), ("weather", "radek.gryciukk@gmail.com")])
def test_main(option, mail_receiver):
    main(option, mail_receiver)
