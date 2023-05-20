import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        loc = tracker.get_slot("location")
        api_key = "9a38206167d8d178536e85d9830b2c9b"  # Replace with your OpenWeatherMap API key

        url = f"http://api.openweathermap.org/data/2.5/weather?q={loc}&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        country = data['sys']['country']
        city = data['name']
        condition = data['weather'][0]['main']
        temperature = data['main']['temp']
        temperature = round(temperature - 273.15, 2)  # Convert temperature from Kelvin to Celsius
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        response = f"It is currently {condition} in {city} at the moment." \
                   f"The temperature is {temperature}°C, the humidity is {humidity}% and the wind speed is {wind} mph."
        dispatcher.utter_message(response)
        return [SlotSet('location', city)]
