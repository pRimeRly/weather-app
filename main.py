import requests
from twilio.rest import Client
import os

try:
    api_key = os.environ["OMW_API_KEY"]
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
except KeyError as message:
    print(f"Invalid environment variable.\n{message} does not exist.")
else:
    # TWILIO API VARIABLES
    FROM_NUM = '+18583304296'
    TO_NUM = '+31639298381'

    # OMW API VARIABLES
    OMW_Endpoint = "https://api.openweathermap.org/data/3.0/onecall?"
    MY_LAT = 52.37403
    MY_LONG = 4.88969

    weather_params = {
        "lat": MY_LAT,
        "lon": MY_LONG,
        "appid": api_key,
        "exclude": "current,minutely,daily"
    }
    response = requests.get(url=OMW_Endpoint, params=weather_params)
    response.raise_for_status()
    weather_data = response.json()

    hourly_data = weather_data["hourly"]

    # list of weather id's for the next 12 hour's
    weather_at_hour_id = [hourly_data[i]["weather"][0]["id"] for i in range(12)]

    # ID's less than 700 represents bad weather
    will_rain = bool([True for item in weather_at_hour_id if item < 700])

    if will_rain:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="It's going to rain today, Remember to bring an ☔",
            from_=FROM_NUM,
            to=TO_NUM
        )
        print(message.status)
