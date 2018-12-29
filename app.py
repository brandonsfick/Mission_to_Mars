from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from flask import send_from_directory

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_News_db")

@app.route("/")
def home():

    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", Mars=mars_data) 

@app.route("/music/<path:filename>")
def music(filename):
    return send_from_directory('../Homework/templates', filename)

@app.route("/scrape")
def scrape():
    # Run the scrape function
    Mars_news = scrape_mars.Scrap_Mars_data()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, Mars_news, upsert=True)

    # Redirect back to home page
    return redirect("/")
  

if __name__ == "__main__":
    app.run(debug=True)