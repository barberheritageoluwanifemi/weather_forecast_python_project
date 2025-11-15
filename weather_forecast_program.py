import requests
from flet import *
from dotenv import load_dotenv
import os
import pprint

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

BASE_URL = "http://api.weatherapi.com/v1/current.json"
city = "lagos"

data = {
    "key": API_KEY,
    "q": city
}

response = requests.get(BASE_URL, params=data)
json_data = response.json()
city_stat = f"Last update time: {json_data['current']['last_updated']}"
temp = f"{json_data['current']['temp_c']}°C"
condition = f"Condition: {json_data['current']['condition']['text']}"
condition_code = f"Code: {json_data['current']['condition']['code']}"

def main(page: Page):
    page.bgcolor = "blue"
    page.title = "Weather App"
    page.scroll = "auto"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
#-------------------------UI CARD------------------------------------------
    weather_card = Container(
        width= 700,
        padding= 30,
        border_radius= 20,
        bgcolor= "white",
        shadow= BoxShadow(
            blur_radius= 20,
            color= "black12",
            offset= Offset(0, 4)
        ),
            content= Column(
            horizontal_alignment= "center",
            controls=[
                Text(f"Location: {city.title()}", size= 25),
                Text(city_stat, size = 12, weight="bold"),
                Text(condition, size=20, color= "blue",weight= "w600"),
                Text(temp, size= 50, weight = "bold"),
                Divider(height= 20, color= "transparent"),
                Text(condition_code, size= 14, color= "black54")
            ]
        )
    )

    page.add(weather_card)
    page.update()

app(target= main, view= AppView.FLET_APP_WEB)

FORECAST_URL = "http://api.weatherapi.com/v1/forecast.json"
longitude = "6.4983° N"
latitude = "3.3486° E"
params = {
    "key": API_KEY,
    "q" : "6.4983° N, 3.3486° E",
    "days" : 1
}

forecast_response = requests.get(FORECAST_URL, params= params)
response_data = forecast_response.json()

forecast_days = response_data["forecast"]["forecastday"]
# pprint.pprint(response_data["forecast"]["forecastday"][0])

print(f"Forecast for {response_data['location']['name']}, {response_data['location']['country']}")
print(f"Local time: {response_data['location']['localtime']}")
# pprint.pprint(response_data["location"])
for day in forecast_days:
    print(f"Date: {day['date']}")
    print(f"Condition: {day['day']['condition']['text']}")
    print(f"Chances of rain: {day['day']['daily_chance_of_rain']}%")
    print(f"Chances of snow: {day['day']['daily_chance_of_snow']}%")
    print("-"*40)

for hour in day["hour"]:
    time = hour["time"]
    temp = hour["temp_c"]
    cond = hour["condition"]["text"]
    print(f"   {time} -> {temp}°C | {cond}")

# import requests

# lat = 6.4983
# lon = 3.3486

# url = "https://nominatim.openstreetmap.org/reverse"
# params = {
#     "lat": lat,
#     "lon": lon,
#     "format": "json"
# }

# headers = {
#     "User-Agent": "MyWeatherApp/1.0 tageb109@gmail.com"
# }

# r = requests.get(url, params=params, headers= headers)
# data = r.json()

# print(data["display_name"])
