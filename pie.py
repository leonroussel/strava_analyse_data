#!/usr/bin/env python3

import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

import get_strava_info
import date_regulation

import datetime

import matplotlib.pyplot as plt
import numpy as np

# Dictionnary to complete with the all kind of sport to get a beautiful pie graph
# Decription of each indice of the list
# [0] : order in the graph, [1] label's name, [2] light color, [3] dark color 
dict_bdd = {"Run" : [1, 'CAP', 'lightgreen', 'mediumseagreen'],\
            "Ride" : [2, 'Vélo', 'lightsalmon', 'orangered'],\
            "Crossfit" : [3, 'PPG', 'violet', 'darkorchid'],\
            "NordicSki" : [4, 'Ski', 'lightskyblue', 'steelblue'],\
            "Workout" : [5, 'PPG', 'violet', 'darkorchid']}
    
"""
Set of colors in matplotlib link 2 by 2 :
silver, whitesmoke
lightcoral, indianred
mediumseagreen, lightgreen
orangered, lightsalmon
steelblue, lightskyblue
violet, darkorchid
"""

def create_pie(activities_list, title):
    """
    Create a pie graph
    Ex of param :
    [('Run', [1.4, 0.8, 1.6, 0.6, 0.8]), ('Ride', [0.9, 1.0, 1.0]), ('NordicSki', [2.2, 1.5])]
    """
    # Creation of the extern disk of the pie
    total_duration_activities_list = []
    for activity_info in activities_list:
        activity_type, duration_list = activity_info
        total_duration_activities_list.append((activity_type, round(sum(duration_list), 1)))
    
    # width of the circles
    size = 0.45
    
    # get the duration's lists
    total_durations = np.array([e[1] for e in total_duration_activities_list])
    single_duration = np.concatenate([durations[1] for durations in activities_list], axis = None)
    
    # get most practiced activity and the index of this activity in the parameter list
    major_activity = max(total_duration_activities_list, key=lambda x:x[1])
    index_mayor_activity = total_duration_activities_list.index(major_activity)
    # put this activity forward by exploding this part of the circle
    explode = [0 if not i == index_mayor_activity else 0. for i in range(len(total_duration_activities_list))]
    
    # labels : activity + duration
    labels = tuple([dict_bdd[e[0]][1] + "\n" + str(e[1]) + "h" for e in total_duration_activities_list])
    color_label = tuple([dict_bdd[e[0]][3] for e in total_duration_activities_list])
    
    # colors of each sport, extern and intern
    total_colors = [dict_bdd[e[0]][2] for e in total_duration_activities_list]
    single_colors = [dict_bdd[e[0]][3]  for e in activities_list for e2 in e[1]]
    
    # create the plot
    fig, ax = plt.subplots(figsize=(8,6))
    # make the two pie, intern and 
    # Docs : https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.pie.html
    _, texts = ax.pie(total_durations, colors=total_colors, explode=explode, \
           wedgeprops=dict(width=size, edgecolor='w'), shadow=True, labels=(labels), \
           textprops={'fontsize': 14}, labeldistance = 0.77)
    ax.pie(single_duration, colors=single_colors, radius=1-size, shadow=True,\
           wedgeprops=dict(width=size/2, edgecolor='w'))
    
    # set labels color
    for i, text in enumerate(texts):
    # Docs : https://matplotlib.org/3.3.3/api/text_api.html#matplotlib.text.Text
        text.set_color(color_label[i])
        text.set_fontsize(14)
        text.set_fontweight("semibold")
        text.set_verticalalignment("center")
        text.set_horizontalalignment("center")
        # text.set_bbox(text.get_bbox_patch())

    # set the second part of the title
    total_duration = round(sum(total_durations),1)
    plt.title(title + f"Total : {total_duration}h", fontweight="bold", fontsize = 16)
    
    date_string = "Crée le " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    plt.text(1.3, -1.6, date_string, fontsize=8, bbox=dict(facecolor='grey', alpha=0.3))
    # set the name of the png file with the current date
    current_time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    script_path = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(f'{script_path}/{current_time}.svg')
    
    # show the result !
    plt.show()

def get_info_pie(activities_list):
    """
    Create the parameter of create_pie
    """
    dict_activities = {}

    # construct the parameter of create_pie, the liste with each activity
    for activity in activities_list:
        activity_type = activity["type"]
        # moving_time in hours
        moving_time = round(activity["moving_time"]/3600, 1)
        if activity_type in dict_activities:
            # add the moving type to the list that already exists
            dict_activities[activity_type].append(moving_time)
        else:
            ## add the activity type and the first moving_time
            dict_activities[activity_type] = [moving_time]
            
    # convert to a list and sort the activities with the order (that is the first case of dict_bdd)
    res = list(dict_activities.items())
    res.sort(key=lambda x:dict_bdd[x[0]][0])
    return res
        
if __name__ == "__main__":
    # n days limit
    n = 7
    
    # get k last activities
    k = 30
    local_activity_list = get_strava_info.get_all_activities(k)
    
    # troncation of the list to keep only the activities that happen in the last n days
    # (use date_regulation module)
    last_activities = date_regulation.activity_last_n_days(n, local_activity_list)
    
    param_create_pie = get_info_pie(last_activities)
    
    # create title :
    date = datetime.datetime.now()
    week = date.isocalendar()[1]
    
    curr_title = f"Semaine {week}\n"
    create_pie(param_create_pie, curr_title)

# DOCS :
# Documentation ax.pie :
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.pie.html

# labels : https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_and_donut_labels.html