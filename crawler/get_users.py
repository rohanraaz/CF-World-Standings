from datetime import datetime
import requests
import json

# Global Variables #
active_users_url = \
    "https://codeforces.com/api/user.ratedList?activeOnly=false&lang=en"
unknown = "Unknown"

# Static Variables #
session = requests.session()


def get_all_active_users():
    request = session.get(active_users_url)
    plain = request.text
    users_json = json.loads(plain)["result"]
    return users_json


def separate_by_organization(users):
    organizations = {unknown: []}
    for user in users:
        user_datetime = datetime.fromtimestamp(user["lastOnlineTimeSeconds"])
        active = (datetime.now()-user_datetime).days < 30
        if "organization" in user:
            organization = user["organization"]
            if organization not in organizations:
                organizations[organization] = []
            organizations[organization].append([active, user["rating"], user["handle"]])
        else:
            organizations[unknown].append([active, user["rating"], user["handle"]])
    for organization in organizations:
        organizations[organization] = sorted(organizations[organization])[::-1]
    return organizations
