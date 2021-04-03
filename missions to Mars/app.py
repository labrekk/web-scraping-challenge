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

# Scrape Route
@app.route('/scrape')
def scrape():
    mars_scrape = scrape_mars.scrape_info()
    print(mars_scrape)
    mongo.db.mars.update({}, mars_scrape, upsert=True)


    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)