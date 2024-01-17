import json
import requests
import sys
from requests.auth import HTTPBasicAuth
from urllib.parse import quote
from collections import Counter

print("##################################################################\n############## Welcome To Violet's Shitty Analytics ##############\n##################################################################\n############## If something breaks, no it didn't <3 ##############\n##################################################################\n")
email = input("Email: ")
token = input("Api key: ")
region = input("Region (us or eu): ")
website_id = input("Website id: ")
print("--------")

requestString = "https://api-{}.mouseflow.com/websites/{}/stats".format(region,
    website_id)
req1 = requests.get(requestString, auth=HTTPBasicAuth(email, token))
data = req1.json()
full_session_count = data["sessionCount"]

requestString2 = "https://api-{}.mouseflow.com/websites/{}/recordings?limit=10000".format(region,
    website_id)
reqr = requests.get(requestString2, auth=HTTPBasicAuth(email, token))
datar = reqr.json()

# Extract tags and variables from recordings
all_tags = [tags for recording in datar["recordings"] for tags in recording["tags"]]
all_variables = [variables for recording in datar["recordings"] for variables in recording["variables"]]

# Find the top 5 most common tags and variables
top_tags = Counter(all_tags).most_common(5)
top_variables = Counter(all_variables).most_common(5)

# Extract engagement time from recordings
engagement_times = [recording["engagementTime"] for recording in datar["recordings"]]

# Calculate the average engagement time
average_engagement_time = sum(engagement_times) / len(engagement_times) if engagement_times else 0

print(f"Average Engagement Time: {average_engagement_time:.2f} ms (10k most recent recordings)\n")

if top_tags:
    print("Top 5 Tags (10k most recent recordings):")
    for tag, count in top_tags:
        print(f"- {tag}: {count}")
        

if top_variables: 
    print("\nTop 5 Variables (10k most recent recordings):")
    for variable, count in top_variables:
        print(f"- {variable}: {count}")
       
print("--------")

end = input("Type 1 to search more data, or type 2 to exit: ")
if(end ==  '2'):
    sys.exit()

tv_input = input("Choose which to search by (tag/var): ").lower()

if tv_input == 'tag':
    type_input = input("Enter tag name:").lower()
    requestString2 = "https://api-{}.mouseflow.com/websites/{}/stats?tags={}".format(region,
    website_id, type_input)
    req2 = requests.get(requestString2, auth=HTTPBasicAuth(email, token))
    data2 = req2.json()
    tag_session_count = data2["sessionCount"]
    percentage = (tag_session_count / full_session_count) * 100
    friction = data2["averageFrictionScore"]
    print("--------")
    print("Total sessions with this tag in the past 30 days:", tag_session_count)
    print("Percentage of sessions that contain this tag:", percentage, "%")
    print("Average friction score of recordings with this tag:", friction)

    requestStringTag = "https://api-{}.mouseflow.com/websites/{}/pagelist?tags={}".format(region,
    website_id, type_input)
    reqTag = requests.get(requestStringTag, auth=HTTPBasicAuth(email, token))
    dataTag = reqTag.json()
    sorted_pages = sorted(dataTag['pages'], key=lambda x: x['views'], reverse=True)

    # Get the top 5 viewed pages
    top_5_pages = sorted_pages[:5]

    # Extract and print the displayURL of the top 3 viewed pages
    top_5_display_urls = [page['displayUrl'] for page in top_5_pages]
    print("\nTop 5 Pages with this tag:")
    for url in top_5_display_urls:
        print(f"- {url}")
    print("--------")
    

if tv_input == 'var':
    key_input = input("Enter variable key:").lower()
    val_input = input("Enter variable value:").lower()
    requestString3 = "https://api-{}.mouseflow.com/websites/{}/stats?vars={}%3D{}".format(region,
    website_id, key_input, val_input)
    req3 = requests.get(requestString3, auth=HTTPBasicAuth(email, token))
    data3 = req3.json()
    var_session_count = data3["sessionCount"]
    friction2 = data3["averageFrictionScore"]
    percentage2 = (var_session_count / full_session_count) * 100
    print("--------")
    print("Total sessions with this variable in the past 30 days: ", var_session_count)
    print("Percentage of sessions that contain this variable: ", percentage2, "%")
    print("Average friction score of recordings with this variable: ", friction2)


    requestString3 = "https://api-{}.mouseflow.com/websites/{}/pagelist?vars={}%3D{}".format(region,
    website_id, key_input, val_input)
    reqVar = requests.get(requestString3, auth=HTTPBasicAuth(email, token))
    dataVar = reqVar.json()
    sorted_pages = sorted(dataVar['pages'], key=lambda x: x['views'], reverse=True)

    # Get the top 5 viewed pages
    top_5_pages = sorted_pages[:5]

    # Extract and print the displayURL of the top 3 viewed pages
    top_5_display_urls = [page['displayUrl'] for page in top_5_pages]
    print("\nTop 5 Pages with this variable:")
    for url in top_5_display_urls:
        print(f"- {url}")
    print("--------")

input()
