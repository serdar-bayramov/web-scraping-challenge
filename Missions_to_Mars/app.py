from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# connect to mongo db
client = pymongo.MongoClient('mongodb://localhost:27017')

# create db
db = client.mars_db

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    data = db.collection.find_one()
    return render_template("index.html", mar=data)

# Route that will trigger the scrape function   
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dtb = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    db.collection.update({}, mars_dtb, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)