# run with:
# flask --app main run --debug

from flask import Flask, request, Response
from dotenv import load_dotenv
import requests
import os
import json
from jinja2 import Environment, PackageLoader, select_autoescape


load_dotenv()
API_KEY = os.environ["API_KEY"]
ENDPOINT = "https://api.weatherapi.com/v1/forecast.json"

app = Flask(__name__)
env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)


def get_data(location):
    url = f"{ENDPOINT}?key={API_KEY}&q={location}&aqi=no&days=3"
    r = requests.get(url)
    return r.json()

@app.route("/")
def root():
    file = open("pages/index.html", "r")
    contents = file.read()
    file.close()
    return contents

@app.route("/main.css")
def main_css():
    file = open("css/main.css")
    contents = file.read()
    file.close()
    return Response(contents, mimetype="text/css")

@app.route("/w")
def route_location():
    location = request.args.get("location")
    data = get_data(location)
    template = env.get_template("forecast.html")
    

    return template.render(
        location = data["location"]["name"],
        forecast_today=data["current"]["temp_f"],
        forecast_min=[
            data["forecast"]["forecastday"][i]["day"]["mintemp_f"]
            for i in range(3)
        ],
        forecast_max=[
            data["forecast"]["forecastday"][i]["day"]["maxtemp_f"]
            for i in range(3)
        ],
        forecast_condition=[
            data["forecast"]["forecastday"][i]["day"]["condition"]["icon"]
            for i in range(3)
        ],
        forecast_cor=[
            data["forecast"]["forecastday"][i]["day"]["daily_chance_of_rain"]
            for i in range(3)
        ],
        date=[
            data["forecast"]["forecastday"][i]["date"]
            for i in range(3)
        ],
        region=data["location"]["region"],
        all_data=json.dumps(data, indent=4)
    )
