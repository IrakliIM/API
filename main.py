import requests
import json
import sqlite3

get_countries_request = requests.get(url = "https://restcountries.com/v3.1/all",
                                     headers = {"Content-Type": "application/json"})
status_code = get_countries_request.status_code
response = get_countries_request.json()

with open("saveResponse.json", "w", encoding = "UTF-8") as j:
    json.dump(response, j, ensure_ascii=False, indent=4)

# it will print all the countrys with USD currency
for country in response:
    if country.get("currencies") != None and country.get("currencies").get("USD") != None:
        print(country.get("name").get("common"))

#  it will save all the countrys -> name; independence status true/false; capital and region if that counry is from Europe

connection = sqlite3.connect("countrys.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS EuropeCountrys(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(250),
    independence_status BOOL,
    capital VARCHAR(250),
    region VARCHAR(250)
);""")

for country in response:
    if country.get("region") == "Europe":
        country_name = country.get("name").get("common")
        independence_status = country.get("independent")
        capital = country.get("capital")[0]
        region = country.get("region")
        cursor.execute("INSERT INTO EuropeCountrys(name, independence_status, capital, region) VALUES (?, ?, ?, ?) ",
        (country_name, independence_status, capital, region))
        connection.commit()

cursor.close()
connection.close()