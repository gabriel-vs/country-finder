import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///countries.db")

# Define useful lists
regions = []
for region in db.execute("SELECT region FROM countries"):
    if region["region"] != None and region["region"] != "" and region["region"] not in regions:
        regions.append(region["region"])

subRegions = []
for subRegion in db.execute("SELECT subregion FROM countries"):
    if subRegion["subregion"] != None and subRegion["subregion"] != "" and subRegion["subregion"] not in subRegions:
        subRegions.append(subRegion["subregion"])

currencies = []
for currency in db.execute("SELECT currency FROM currencies"):
    if currency["currency"] != None and currency["currency"] not in currencies:
        currencies.append(currency["currency"])

languages = []
for language in db.execute("SELECT language FROM languages"):
    if language["language"] not in languages:
        languages.append(language["language"])

blocs = []
for bloc in db.execute("SELECT name FROM blocs"):
    if bloc["name"] not in blocs:
        blocs.append(bloc["name"])

countries_names = []
for country in db.execute("SELECT name FROM countries"):
    if country["name"] != None and country["name"] not in countries_names:
        countries_names.append(country["name"])
        
# Sort the lists alphabetically
currencies.sort()
languages.sort()
blocs.sort()
regions.sort()
subRegions.sort()
countries_names.sort()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("name").lower().capitalize() not in countries_names:
            return render_template("indexError.html")
            
        user_country = db.execute(
            "SELECT * FROM countries WHERE name == ?", request.form.get("name").lower().capitalize())[0]

        country_borders = db.execute(
            "SELECT name FROM countries WHERE code IN (SELECT border_code FROM borders WHERE code IN (SELECT code FROM countries WHERE name = ?))", user_country["name"])

        country_currencies = db.execute(
            "SELECT currency, symbol FROM currencies WHERE code IN (SELECT code FROM countries WHERE name = ?)", user_country["name"])

        country_languages = db.execute(
            "SELECT language FROM languages WHERE code IN (SELECT code FROM countries WHERE name = ?)", user_country["name"])

        country_blocs = db.execute(
            "SELECT name, acronym FROM blocs WHERE code IN (SELECT code FROM countries WHERE name = ?)", user_country["name"])

        return render_template("info.html", country=user_country, borders=country_borders, currencies=country_currencies, languages=country_languages, blocs=country_blocs)

    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        selections = db.execute("SELECT name, flag FROM countries WHERE region IN (coalesce(?, region)) AND subregion IN (coalesce(?, subregion)) AND code IN (SELECT code FROM currencies WHERE currency IN (coalesce(?, currency))) AND code IN (SELECT code FROM languages WHERE language IN (coalesce(?, language))) AND code IN (SELECT code FROM blocs WHERE name IN (coalesce(?, name))) AND code IN (SELECT code FROM borders WHERE border_code IN (SELECT code FROM countries WHERE name IN (coalesce(?,name))))",
        request.form.get("region"), request.form.get("subRegion"), request.form.get("currency"), request.form.get("language"), request.form.get("bloc"), request.form.get("border"))
        
        if len(selections) == 0:
            return render_template("searchNoMatch.html", countries=countries_names, regions=regions, subRegions=subRegions, currencies=currencies, languages=languages, blocs=blocs)
            
        return render_template("searched.html", countries=selections)

    else:
        return render_template("search.html", countries=countries_names, regions=regions, subRegions=subRegions, currencies=currencies, languages=languages, blocs=blocs)