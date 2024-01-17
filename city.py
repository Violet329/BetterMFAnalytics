import json
import requests
import sys
from requests.auth import HTTPBasicAuth
from collections import Counter
from datetime import datetime, timedelta

print("##################################################################\n############## Welcome To Violet's Shitty Analytics ##############\n##################################################################\n############## If something breaks, no it didn't <3 ##############\n##################################################################\n")
email = input("Email: ")
token = input("Api key: ")
region = input("Region (us or eu): ")
website_id = input("Website id: ")
print("--------")


requestString = "https://api-{}.mouseflow.com/websites/{}/recordings?limit=10000".format(region,
    website_id)
req = requests.get(requestString, auth=HTTPBasicAuth(email, token))
data = req.json()

if "recordings" in data:
    all_cities = [recording["city"] for recording in data["recordings"] if recording.get("city")]
    top_cities = Counter(all_cities).most_common(150)

    all_country = [recording["country"] for recording in data["recordings"] if recording.get("country")]
    top_country = Counter(all_country).most_common(150)

    

    if all_cities:
        print("Top 150 cities (10k most recent recordings)")
        print("----City | Count | Percentage----")
        for city, count in top_cities:
            percent = (count / 10000) * 100
            print(f"= {city} | {count} | {percent}%")
        print("--------\n")
        print("Top Countries (10k most recent recordings)")
        print("----Country | Count | Percentage----")
        for country, count in top_country:
            percent = (count / 10000) * 100
            print(f"= {country} | {count} | {percent}%")
        print("--------")
else:
    print("No recordings found in the response.")



