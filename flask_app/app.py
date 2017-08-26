from flask import Flask
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/country')
def get_country_of_city():
    return json.dumps({'country': 'Australia'})
