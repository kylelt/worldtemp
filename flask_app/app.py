from flask import Flask
from get_country import CountryMapper
import json

app = Flask(__name__)
countryMapping = CountryMapper()

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/country/<city>')
def get_country_of_city(city):
    return countryMapping.get_latlon(city)

