import requests
from datetime import datetime
import os

APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
EXERCISE_API = 'https://trackapi.nutritionix.com/v2/natural/exercise'
SHEETY_API = "https://api.sheety.co/d974b632fa5a6289f283e9742d5f3f5d/workoutTracking/workouts"
BEARER = os.environ.get("BEARER")

headers = {
    'x-app-id': APP_ID,
    'x-app-key': APP_KEY,
    'x-remote-user-id': '0'
}

body = {
    "query" : input("Tell me which exercise you did: "),
    "gender": "male",
    "weight_kg": 74,
    "height_cm": 183,
    "age": 28
}

response = requests.post(EXERCISE_API, headers=headers, json=body)
response.raise_for_status()

data = response.json()

date = datetime.now()

formatted_date = date.strftime("%d/%m/%Y")
formatted_time = date.strftime("%H:%M:%S")

header_sheety = {
    "Authorization": BEARER
}

for exercise in data["exercises"]:
    body = {
        "workout": {
            "date": formatted_date,
            "time": formatted_time,
            "exercise": exercise["name"].title(),
            "duration": str(exercise["duration_min"]),
            "calories": exercise["nf_calories"]
        }
    }

    response_sheety = requests.post(url=SHEETY_API, json=body, headers=header_sheety)
    print(response_sheety.text)
