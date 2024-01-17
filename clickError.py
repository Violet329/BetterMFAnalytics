import json
import requests
from requests.auth import HTTPBasicAuth

print("##################################################################\n############## Welcome To Violet's Shitty Analytics ##############\n##################################################################\n############## If something breaks, no it didn't <3 ##############\n##################################################################\n")
email = input("Email: ")
token = input("Api key: ")
region = input("Region (us or eu): ")
website_id = input("Website id: ")
print("--------")

requestString = "https://api-{}.mouseflow.com/websites/{}/recordings?tags=click-error".format(region, website_id)
req = requests.get(requestString, auth=HTTPBasicAuth(email, token))
data = req.json()

click_error_id = [recording["id"] for recording in data["recordings"] if "click-error" in recording.get("tags", [])]

pageviewList = []
print("Analyzing data...this may take a while...")
for id in click_error_id:
    requestString2 = "https://api-{}.mouseflow.com/websites/{}/recordings/{}".format(region, website_id, id)
    req2 = requests.get(requestString2, auth=HTTPBasicAuth(email, token))
    data2 = req2.json()
    click_error_page_views = [page_view['id'] for page_view in data2['pageViews'] if 'click-error' in page_view.get('tags', [])]
    pageviewList.extend(click_error_page_views)
    for pvID in pageviewList:
        requestString3 = "https://api-{}.mouseflow.com/websites/{}/recordings/{}/pageviews/{}/data".format(region, website_id, id, pvID)
        req3 = requests.get(requestString3, auth=HTTPBasicAuth(email, token))
        try:
            data3 = req3.json()
        except json.decoder.JSONDecodeError:
            continue  # Skip to the next iteration

        for item in data3.get("javascriptErrors", []):
            with open('errors.txt', 'a') as file:
                    file.write(f"{item}\n")
                    file.write(f"----------------------------\n")

print("Data has been output to errors.txt")
input()
