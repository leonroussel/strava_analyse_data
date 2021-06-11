#!/usr/bin/env python3

import datetime
from datetime import date

def less_than_n_days(n, input_date):
    """
    Return a boolean that says if input date is less than n days old
    input_date format : yyyy_mm_dd
    """
    activity_date = datetime.date(int(input_date[0:4]), int(input_date[5:7]), int(input_date[8:10]))
    curr_date = date.today()

    delta = curr_date-activity_date
    return delta.days < n

def activity_last_n_days(n, activities_list):
    """
    Return a list of activities that are less than n days old
    (Activities are classified with the date, when an activitie is outdated, we stop the research)
    """
    res = []
    for activity in activities_list:
        if less_than_n_days(n, activity["start_date"]):
            res.append(activity)
        else:
            return res
    return res

