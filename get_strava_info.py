#!/usr/bin/env python3

# ----------------------------------------------
# Module than give back information about athlete 
# or his activities with the STRAVA API
# ----------------------------------------------

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_access_token():
    # ------
    # Return the access_token that has a lifetime, refresh_token has no lifetime
    # ------

    auth_url = "https://www.strava.com/oauth/token"
    payload = {
    'client_id': "57789",
    'client_secret': 'a1b970d296f165a0f9953db6725ae1ef447aca7d',
    'refresh_token': '3ac636e4138324e03ebb2ad942b3e8fb348dfca1',
    'grant_type': "refresh_token",
    'f': 'json'
    }
    
    print("Requesting Token...\n")

    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']

    print(f"Access Token = {access_token}\n")

    return access_token

def get_all_activities(per_page = 10, page = 1):
    # ------
    # Return a dict with information about last activities 
    # ------

    print('Get all activities ...')
    
    # Get access token with a post request
    access_token = get_access_token()
    
    url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': per_page, 'page': page}
    
    my_dataset = requests.get(url, headers=header, params=param).json()
    
    return my_dataset

#---------------TESTS-----------------------
# if __name__ == "__main__":
#     # id_activity = "4454656535"
#     # temp_get_acti_stream = get_activity_stream(id_activity, "altitude")
#     # distance_list = temp_get_acti_stream["distance"]["data"]
#     # altitude_list = temp_get_acti_stream["altitude"]["data"]
#     # print(distance_list)
#     # print(altitude_list)
    
#     last_activities = get_all_activities(5, 1)
#     for e in last_activities:
#         print(e)
#         print()
#-------------------------------------------
