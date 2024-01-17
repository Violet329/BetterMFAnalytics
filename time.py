import json
import requests
from requests.auth import HTTPBasicAuth
from collections import defaultdict
from datetime import datetime, timedelta

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


requestString = "https://api-{}.mouseflow.com/websites/{}/recordings?limit=10000&expand=true&fromdate={}&todate={}".format(region,
    website_id, from_date, to_date)
req1 = requests.get(requestString, auth=HTTPBasicAuth(email, token))
data = req1.json()


page_views = []
for recording in data["recordings"]:
    page_views.extend(recording["pageViews"])


daily_counts = defaultdict(int)
hourly_counts = defaultdict(int)

#if you don't understand this then learn to code
for page in page_views:
    start_time = datetime.fromisoformat(page["startTime"])
    
    
    hour_key = start_time.replace(minute=0, second=0, microsecond=0)
    hourly_counts[hour_key] += 1


    day_key = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    daily_counts[day_key] += 1


peak_day = max(daily_counts, key=daily_counts.get)
lowest_day = min(daily_counts, key=daily_counts.get)

peak_hour = max(hourly_counts, key=hourly_counts.get)
lowest_hour = min(hourly_counts, key=hourly_counts.get)

# output as yyyy-mm-dd here for consistency
print("Peak Visitors:", peak_day.strftime("%A, %Y/%m/%d"), "at", peak_hour.time())
print("Lowest Visitors:", lowest_day.strftime("%A, %Y/%m/%d"), "at", lowest_hour.time())

print("Note: These are calculated by average number of pageviews and rounded to closest hour")
input() #so program doesn't close immediately 