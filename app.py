from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#name of the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_datalists = mongo.db.mars_datalists.find_one()
    return render_template("index.html", mars_datalists=mars_datalists)


@app.route("/scrape")
def scraper():
    mars_datatalists = mongo.db.mars_datalists
    list_data = scrape_mars.scrape()
    mars_datatalists.update({}, list_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
