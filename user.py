import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

print("##################################################################\n############## Welcome To Violet's Shitty Analytics ##############\n##################################################################\n############## If something breaks, no it didn't <3 ##############\n##################################################################\n")
email = input("Enter email: ")
token = input("Enter api key: ")
region = input("Enter region (us or eu): ")
print("--------")

requestString = "https://api-{}.mouseflow.com/account/users/stats".format(region)
req1 = requests.get(requestString, auth=HTTPBasicAuth(email, token))
data = req1.json()

sorted_data = sorted(data, key=lambda x: x["totalLogins"], reverse=True)

less_than_5_logins = [entry for entry in data if entry['totalLogins'] < 5]


total_logins = sum(entry['totalLogins'] for entry in data)

with open('output.txt', 'w') as file:
    file.write("Most active to least active users:\n")
    for entry in sorted_data:
        file.write(f"{entry['email']}: {entry['totalLogins']}\n")

    file.write("\nUsers with Less Than 5 Logins:\n")
    for entry in less_than_5_logins:
        file.write(f"{entry['email']}: {entry['totalLogins']}\n")

    file.write(f"\nTotal Account Logins: {total_logins}\n")

print("File Generated")