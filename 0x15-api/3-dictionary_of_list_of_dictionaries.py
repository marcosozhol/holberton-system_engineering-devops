#!/usr/bin/python3
"""
export data in the JSON format
"""

import json
import requests
import sys

if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/"
    # gets all users
    users = requests.get("{}users".format(url)).json()
    # jasonizer the users
    file = {}
    for user in users:
        userId = user.get("id")
        username = user.get("username")
        todos = requests.get("{}users/{}/todos".format(url, userId)).json()
        all_task = [{"username": username,
                     "task": all_task.get("title"),
                     "completed": all_task.get("completed"),
                     } for all_task in todos]
        file[userId] = all_task
        # to each user, add a key value pair
        with open("todo_all_employees.json", "w") as filejs:
            json.dump(file, filejs)
