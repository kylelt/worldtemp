from get_country import CountryMapper
import json
from tweetscanner import dataIO
from flask import Flask, render_template

app = Flask(__name__)
countryMapping = CountryMapper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/country/<city>')
def get_country_of_city(city):
    return countryMapping.get_latlon(city)

@app.route('/countries')
def get_countries():
    return dataIO.getAllCountryObjectsJSON()
