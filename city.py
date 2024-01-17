import json
import requests
from requests.auth import HTTPBasicAuth
from collections import Counter

print("##################################################################\n############## Welcome To Violet's Shitty Analytics ##############\n##################################################################\n############## If something breaks, no it didn't <3 ##############\n##################################################################\n")
email = input("Email: ")
token = input("Api key: ")
region = input("Region (us or eu): ")
website_id = input("Website id: ")

print("--------\n")
print("!IMPORTANT -- Only 10k records can be pulled from a defined date range, use a smaller range if site contains a lot of data --!\n")
from_date = input("Input start date (yyyy-mm-dd): ")
to_date = input("Input end date (yyyy-mm-dd): ")
print("--------")

requestString = "https://api-{}.mouseflow.com/websites/{}/recordings?limit=10000&fromdate={}&todate={}".format(region,
    website_id, from_date, to_date)
req = requests.get(requestString, auth=HTTPBasicAuth(email, token))
data = req.json()

if "recordings" in data:
    all_cities = [recording["city"] for recording in data["recordings"] if recording.get("city")]
    top_cities = Counter(all_cities).most_common(150)

    all_country = [recording["country"] for recording in data["recordings"] if recording.get("country")]
    top_country = Counter(all_country).most_common(150)
    total_recordings = len(data["recordings"])
    

    if all_cities:
        print("Top 150 cities")
        print("----City | Recording Count | Percentage----")
        for city, count in top_cities:
            percent = (count / total_recordings) * 100
            print(f"= {city} | {count} | {percent}%")
        print("--------\n")
        print("Top Countries")
        print("----Country | Recording Count | Percentage----")
        for country, count in top_country:
            percent = (count / total_recordings) * 100
            print(f"= {country} | {count} | {percent}%")
        print("--------")
else:
    print("No recordings found in the response.")



