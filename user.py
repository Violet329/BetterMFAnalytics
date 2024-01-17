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

# Sort the data by the 'totalLogins' key in descending order
sorted_data = sorted(data, key=lambda x: x["totalLogins"], reverse=True)

# Create a separate list of users with less than 5 logins
less_than_5_logins = [entry for entry in data if entry['totalLogins'] < 5]

# Calculate the sum of logins for all emails
total_logins = sum(entry['totalLogins'] for entry in data)

# Output the sorted data to a text file
with open('output.txt', 'w') as file:
    file.write("Most active to least active users:\n")
    for entry in sorted_data:
        file.write(f"{entry['email']}: {entry['totalLogins']}\n")

    # Output the list of users with less than 5 logins to a text file
    file.write("\nUsers with Less Than 5 Logins:\n")
    for entry in less_than_5_logins:
        file.write(f"{entry['email']}: {entry['totalLogins']}\n")

    # Output the sum of logins for all emails to a text file
    file.write(f"\nTotal Account Logins: {total_logins}\n")

print("File Generated")