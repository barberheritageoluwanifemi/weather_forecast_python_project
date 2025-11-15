# import flet as ft
from flet import *
import requests
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

# response = requests.get(BASE_URL, params=data)
# json_data = response.json()
# city_stat = f"Last update time: {json_data['current']['last_updated']}"
# temp = f"{json_data['current']['temp_c']}°C"
# condition = f"Condition: {json_data['current']['condition']['text']}"
# condition_code = f"Code: {json_data['current']['condition']['code']}"

def main(page: Page):
    #---------------------------------------------Giving the page its basic layout-----------------------------------------------
    page.title = "FLET WEATHER APP"
    page.bgcolor = "#f5f5f5"
    page.scroll = "auto"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.add(Text("I am here"))
    city_input = TextField(
        label= "Input City name, placeholder or even longitude and latitude for more precise forecasts",
        width= 400,
        autofocus= True,
        bgcolor= "white",
        border_radius= 20,
    )
    weather_title = Text(" ", size= 20, weight= "bold")
    city_name = Text(" ", size= 15, weight= "bold")
    temp_text = Text("", size= 40, weight= "bold")
    condition_text = Text("", size= 18)
    updated_text = Text("", size= 16)
    weather_card = Container(
        width = 350,
        padding = 20,
        bgcolor= "white",
        border_radius= 17,
        shadow = BoxShadow(
            blur_radius= 20,
            color= "black12",
            offset= (0, 4)
        ),
        content = Column(
                horizontal_alignment= "center",
                controls=[
                    weather_title,
                    city_name,
                    temp_text,
                    condition_text,
                    updated_text
                ]
            ),
        visible= False
    )
    
    def fetch_weather(e):
        city = city_input.value.strip()
        if city == "" or " ":
            page.snack_bar = SnackBar(Text("Page cannot be empty"), bgcolor= "red")
            page.snack_bar.open = True
            page.update()

        params = {
            "key": API_KEY,
            "q" : city
        }
        try:
            response = requests.get(BASE_URL, params= params)
            data = response.json()
            if "error" in data:
                page.snack_bar = SnackBar(Text(data["error"]["message"]), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
            #Extract Data 
            last_updated = data["current"]["last_updated"]
            condition = data["current"]["condition"]["text"]
            temp = data["current"]["temp_c"]
            city_location = data["location"]["name"]
            
            weather_title.value = f"Weather in {city_location.title()}"
            updated_text.value = f"Updated: {last_updated}"
            temp_text.value = f"{temp}°C"
            condition_text.value = condition
            city_name.value = city

            weather_card.visible = True
            page.update()

        except Exception as err:
            page.snack_bar = SnackBar(Text("Network Error!"), bgcolor= "red")
            page.snack_bar.open = True
            page.update()

    search_btn = ElevatedButton(
        "Search", icon= Icon(icons.SEARCH),
        width= 150,
        on_click= fetch_weather,
        style = ButtonStyle(
            shape=RoundedRectangleBorder(radius=12),
            padding= 20
        )
    )

    page.add(
        Column(
            spacing= 25,
            controls= [
                Text("Weather App", size=30, weight="bold"),
                city_input,
                search_btn,
                weather_card
            ]
        )
    )


    page.update()


app(target= main, view= AppView.FLET_APP_WEB)