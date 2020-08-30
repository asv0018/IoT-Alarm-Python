import datetime

import pyrebase
import json
import requests

serial_num = "tet"
pathOfConfig = "Resources/config.json"
all_alarm_times = []
all_alarm_days = []
all_alarm_ids = []
all_alarm_everyday = []
all_alarm_days_selected = []
all_alarm_musics = []
all_alarm_snooze = []
all_alarm_plays = []
all_alarm_setters = []


def firebase_handler(response):
    global firebase, uid, data
    data = firebase.database().child("alarms_users").child(uid).get().val()
    json_file = open("Resources/firebase_database_data.json", "w")
    json_file.truncate(0)
    json_file.write(json.dumps(data, indent=4))
    json_file.close()
    refill_the_data_to_variables()


def refill_the_data_to_variables():
    all_alarm_days.clear()
    all_alarm_times.clear()
    all_alarm_plays.clear()
    all_alarm_snooze.clear()
    all_alarm_setters.clear()
    all_alarm_everyday.clear()
    all_alarm_ids.clear()
    all_alarm_days_selected.clear()
    all_alarm_musics.clear()
    json_file = open("Resources/firebase_database_data.json", "r")
    temp__data = json_file.read()
    temp_data = json.loads(temp__data)
    json_file.close()
    for i in temp_data:
        hours, minutes = "", ""
        play = False
        for j in temp_data[i]:
            if j == "setter":
                setter = temp_data[i][j]
                all_alarm_setters.append(setter)
            if j == "hours":
                hours = temp_data[i][j]
            if j == "minutes":
                minutes = temp_data[i][j]
            if j == "id":
                id = temp_data[i][j]
                all_alarm_ids.append(id)
            if j == "music":
                download_music = temp_data[i][j]
                all_alarm_musics.append(download_music)
            if j == "play":
                play = temp_data[i][j]
                all_alarm_plays.append(play)
            if j == "snooze":
                snooze = temp_data[i][j]
                all_alarm_snooze.append(snooze)
            if j == "everytime":
                everytime = temp_data[i][j]
                all_alarm_everyday.append(everytime)
            if j == "days_selected":
                days_selected = temp_data[i][j]
                all_alarm_days_selected.append(days_selected)

        all_alarm_times.append(str(hours) + ":" + str(minutes))


def first_time_init(firebase):
    uid = firebase.database().child("iot_alarm").child(serial_num).child(serial_num)
    uid = uid.get().val()
    if uid is not None:
        stream = firebase.database().child("alarms_users").child(uid).stream(firebase_handler)
        data_file = open("Resources/firebase_database_data.json", "r")
        temp_data = data_file.read()
        data_file.close()
        return uid, stream
    else:
        print("OOPS! :< There is no account paired with this IoT Device")
        data_file = open("Resources/firebase_database_data.json", "r")
        temp_data = data_file.read()
        data_file.close()
        return None, None


#################################################################################################
#                                  THE MAIN PROGRAM STARTS HERE                                 #
#################################################################################################

file = open(pathOfConfig, )
config = json.load(file)
file.close()
firebase = pyrebase.initialize_app(config)
connected_to_internet = False
try:
    check_internet = requests.get("https://www.google.com/",timeout=2)
    print("IoT Alarm is connected to internet :)")
    connected_to_internet = True
except:
    print("NO INTERNET! :< . DEVICE READS PREVIOUS DATA AND ALARMS ACCORDING TO IT")

while True:
    if connected_to_internet:
        uid, stream = first_time_init(firebase)
        if uid is not None and stream is not None:
            while connected_to_internet:
                pass
        else:
            print("OOPS, PLEASE PAIR YOUR DEVICE WITH THE ACCOUNT, RESTART THE DEVICE AND TRY AGAIN")
            keep_in_while_loop_until_restart = True
            while keep_in_while_loop_until_restart:
                pass
    else:
        inner_condition = False
        try:
            refill_the_data_to_variables()
            print("RETRIEVED PREVIOUSLY SAVED DATA")
            inner_condition = True
        except:
            print("OH YOU ARE A NEW USER :> YOU DONT HAVE ANY ALARMS IN YOUR ACCOUNT :)")
            while not inner_condition:
                pass
        while not connected_to_internet:
            pass





