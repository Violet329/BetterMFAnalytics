import json
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import quote
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
    all_referrers = [recording["referrer"] for recording in data["recordings"] if recording.get("referrer")]

    top_ref = Counter(all_referrers).most_common(100)
    total_recordings = len(data["recordings"])

    if top_ref:
        print("\nTop 100 referrers:\n")
        print("----|URL|----|Count|----|Percentage|\n")
        for referrer, count in top_ref:
            percent = (count / total_recordings) * 100
            print(f"= {referrer}| {count} | {percent}%")
else:
    print("No recordings found in the response.")