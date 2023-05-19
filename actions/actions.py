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
        location = tracker.get_slot("location")
        api_key = "9a38206167d8d178536e85d9830b2c9b"  # Replace with your OpenWeatherMap API key

        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and "weather" in data and "main" in data["weather"][0]:
            weather = data["weather"][0]["main"]
            temperature = data["main"]["temp"]
            temperature = round(temperature - 273.15, 2)  # Convert temperature from Kelvin to Celsius

            weather_info = f"The current weather in {location} is {weather} with a temperature of {temperature}°C."
        else:
            weather_info = f"Sorry, I couldn't retrieve the weather information for {location}."

        dispatcher.utter_message(text=weather_info)

        return []
