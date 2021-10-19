import json
import sqlite3

# Creates "countries" database
with open("countries.json") as f:
    countries = json.load(f)

con = sqlite3.connect("countries.db")
db = con.cursor()

# Creates table "countries" in countries.db
db.execute("DROP TABLE IF EXISTS countries")
db.execute("CREATE TABLE countries (name TEXT, code TEXT UNIQUE, capital TEXT, region TEXT, subregion TEXT, population NUMERIC, area NUMERIC, flag TEXT)")
    
for country in countries:
    db.execute("INSERT INTO countries (name, code, capital, region, subregion, population, area, flag) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [country["name"], country["alpha3Code"], country["capital"], country["region"], country["subregion"], country["population"], country["area"], country["flag"]])

con.commit()

# Creates table "borders" in countries.db
db.execute("DROP TABLE IF EXISTS borders")
db.execute("CREATE TABLE borders (code TEXT, border_code TEXT)")

for country in countries:
    for border in country["borders"]:
        db.execute("INSERT INTO borders (code, border_code) VALUES (?, ?)", [country["alpha3Code"], border])

con.commit()
        
# Creates table "currencies" in countries.db
db.execute("DROP TABLE IF EXISTS currencies")
db.execute("CREATE TABLE currencies (code TEXT, currency TEXT, symbol TEXT)")

for country in countries:
    for currency in country["currencies"]:
        db.execute("INSERT INTO currencies (code, currency, symbol) VALUES (?, ?, ?)", [country["alpha3Code"], currency["name"], "({})".format(currency["symbol"])])

con.commit()

# Creates table "languages" in countries.db
db.execute("DROP TABLE IF EXISTS languages")
db.execute("CREATE TABLE languages (code TEXT, language TEXT)")

for country in countries:
    for language in country["languages"]:
        db.execute("INSERT INTO languages (code, language) VALUES (?, ?)", [country["alpha3Code"], language["name"]])

con.commit()

# Creates table "blocs" in countries.db
db.execute("DROP TABLE IF EXISTS blocs")
db.execute("CREATE TABLE blocs (code TEXT, name TEXT, acronym TEXT)")

for country in countries:
    for bloc in country["regionalBlocs"]:
        db.execute("INSERT INTO blocs (code, name, acronym) VALUES (?, ?, ?)", [country["alpha3Code"], bloc["name"], "({})".format(bloc["acronym"])])

con.commit()