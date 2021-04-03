from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri = 'mongodb://localhost:27017/mars_app')

# Index Route
@app.route('/')
def index():
    
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)


