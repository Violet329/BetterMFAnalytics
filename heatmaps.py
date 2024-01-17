import json
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import quote

print("##################################################################\n############## Welcome To Violet's Shitty Analytics ##############\n##################################################################\n############## If something breaks, no it didn't <3 ##############\n##################################################################\n")
email = input("Enter email: ")
token = input("Enter api key: ")
region = input("Enter region (us or eu): ")
website_id = input("Enter a website id: ")
page_name = input("Enter a page name: ")
encoded_page_name = quote(page_name)
device_input = input("Enter the device (desktop, tablet, or phone): ").lower()

if device_input in ['desktop', 'tablet', 'phone']:
    chosen_device = device_input

requestString = "https://api-{}.mouseflow.com/websites/{}/link-analytics?url={}&device={}".format(region,
    website_id, encoded_page_name, chosen_device
)
r = requests.get(requestString, auth=HTTPBasicAuth(email, token))

data = r.json()

targets = data['data'][0]['targets']
total_visit_count = data["data"][0]["visitCount"]
# Sorting targets by hoverTime
sorted_targets = sorted(targets, key=lambda x: x['hoverTime'])

# Extracting the IDs with the longest and shortest hoverTime
longest_hover_target = sorted_targets[-1]
shortest_hover_target = sorted_targets[0]

longest_hover_id = longest_hover_target['id']
shortest_hover_id = shortest_hover_target['id']

# Extracting additional metrics for the longest hover
longest_hover_time_before_hover = longest_hover_target['timeBeforeHover']
longest_hover_hovering_visitors = longest_hover_target['hoveringVisitors']

# Extracting additional metrics for the shortest hover
shortest_hover_time_before_hover = shortest_hover_target['timeBeforeHover']
shortest_hover_hovering_visitors = shortest_hover_target['hoveringVisitors']

longest_hover_total_hover_time = sum(target['hoverTime'] for target in targets if target['id'] == longest_hover_id)
shortest_hover_total_hover_time = sum(target['hoverTime'] for target in targets if target['id'] == shortest_hover_id)
with open('heatmap.txt', 'w') as file:

    file.write("\n-----\n\n")
    file.write(f"Element with the longest hoverTime: {longest_hover_id}\n")
    file.write(f"Average hoverTime for the above element: {longest_hover_total_hover_time} ms\n", )
    file.write(f"Average time before hover for the above element: {longest_hover_time_before_hover} ms\n")
    file.write(f"Number of hovering visitors for the above element: {longest_hover_hovering_visitors}\n" )
    file.write("\n-----\n\n")
    file.write(f"Element ID with the shortest hoverTime: {shortest_hover_id}\n")
    file.write(f"Average timeBeforeHover for the above element: {shortest_hover_time_before_hover} ms\n")
    file.write(f"Number of hoveringVisitors for the above element: {shortest_hover_hovering_visitors}\n")
    file.write(f"Average hoverTime for the above element: {shortest_hover_total_hover_time} ms\n")
    file.write("\n-----\n\n")

    # Calculating total hoverTime, timeBeforeHover, click errors, click rages, and the count of targets
    total_hover_time = sum(target['hoverTime'] for target in targets)
    total_time_before_hover = sum(target['timeBeforeHover'] for target in targets)
    total_click_errors = sum(target['clickErrors'] for target in targets)
    total_click_rages = sum(target['clickRages'] for target in targets)
    total_targets = len(targets)

    # Calculating the average hoverTime, timeBeforeHover, click errors, and click rages
    average_hover_time = total_hover_time / total_targets
    average_time_before_hover = total_time_before_hover / total_targets
    average_click_errors = total_click_errors / total_targets
    average_click_rages = total_click_rages / total_targets

    # Finding the target with the most clicks
    most_clicks_target = max(targets, key=lambda x: x['clicks'])
    most_clicks_clicking_visitors = most_clicks_target['clickingVisitors']

    # Extracting metrics for the target with the most clicks
    most_clicks_id = most_clicks_target['id']
    most_clicks_time_before_click = most_clicks_target['timeBeforeClick']
    most_clicks_count = most_clicks_target['clicks']

    # Calculating the average number of clicks and average total timeBeforeClick
    average_clicks = sum(target['clicks'] for target in targets) / total_targets
    average_total_time_before_click = sum(target['timeBeforeClick'] for target in targets) / total_targets

    most_click_rages_target = max(targets, key=lambda x: x['clickRages'])
    most_click_errors_target = max(targets, key=lambda x: x['clickErrors'])
    most_click_errors_id = most_click_errors_target['id']
    most_click_errors_count = most_click_errors_target['clickErrors']

    # Extracting metrics for the target with the most click rages
    most_click_rages_id = most_click_rages_target['id']
    most_click_rages_count = most_click_rages_target['clickRages']
    most_click_errors_count = most_click_errors_target['clickErrors']
    total_clicks = sum(target['clicks'] for target in targets)
    most_click_errors_click_total = most_click_errors_target['clicks']
    most_rages_click_count = most_click_rages_target['clicks']
    # Printing additional metrics
    file.write(f"Total number of click errors for all elements:{total_click_errors}\n")

    if total_click_errors != 0:
        calc = (total_click_errors / total_visit_count) * 100
        file.write(f"Percent of total visitors that encounter a click-error: {calc} %\n")
        calc2 = most_clicks_target['id']
        file.write(f"Element with the most click errors: {calc2}\n")
        file.write(f"Number of click errors for the above element: {most_click_errors_count}\n")
        calc3 = (most_click_errors_count / most_click_errors_click_total) * 100
        file.write(f"Percent of clicks on this element that result in a click-error: {calc3}\n")
        file.write("\n-----\n\n")

    file.write(f"Total number of click rages for all elements: {total_click_rages}\n")
    if total_click_rages != 0:
        calc4 = (total_click_rages / total_visit_count) * 100
        file.write(f"Percent of total visitors that click-rage: {calc4}\n")
        file.write(f"Element with the most click rages: {most_click_rages_id}\n")
        file.write(f"Number of click rages for above element: {most_click_rages_count}\n")
        calc5 = (most_click_rages_count / most_rages_click_count) * 100
        file.write(f"Percent of clicks on this element that result in a click-rage: {calc5}\n")
        file.write("\n-----\n\n")

    file.write(f"Total number of clicks for all elements: {total_clicks}\n")
    file.write(f"Average number of clicks an element receives: {average_clicks}\n")
    file.write(f"Average total timebeforeClick for all elements: {average_total_time_before_click} ms\n")
    file.write("\n-----\n\n")

    file.write(f"Element with the most clicks: {most_clicks_id}\n")
    file.write(f"Number of clicks for the above element: {most_clicks_count}\n")
    file.write(f"Total clicking visitors for the above element: {most_clicks_clicking_visitors}\n")
    calc6 = (most_clicks_clicking_visitors / total_visit_count) * 100
    file.write(f"Percent of total visitors that click this element: {calc6}")
    file.write(f"Average timeBeforeClick for the element above: {most_clicks_time_before_click} ms\n")
    file.write("\n-----\n\n")
print("Output saved to heatmap.txt")
input()
