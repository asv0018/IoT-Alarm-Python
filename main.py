from datetime import datetime
import re
from pygame import mixer
import os, sys
import glob
import pyrebase
import json
import requests
import calendar
import threading

serial_num = "test"
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
downloaded_music_files = []


def firebase_handler(response):
    global firebase, uid, data
    data = firebase.database().child("alarms_users").child(uid).get().val()
    json_file = open("Resources/firebase_database_data.json", "w")
    json_file.truncate(0)
    json_file.write(json.dumps(data, indent=4))
    json_file.close()
    try:
        refill_the_data_to_variables()
    except:
        print("still no data")

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

        print("*************************")
        if len(str(hours)) < 2:
            hours = "0" + str(hours)
            #print(hours)
        else:
            hours = str(hours)
        if len(str(minutes)) < 2:
            minutes = "0" + str(minutes)
            #print(minutes)
        else:
            minutes = str(minutes)

        all_alarm_times.append(str(hours) + ":" + str(minutes))
    thread = threading.Thread(target=download_all_musics, args=("Resources/Downloads/Music", all_alarm_musics))
    thread.start()


def refill_the_data_to_variables_from_storage():
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
        print("*************************")
        if len(str(hours)) < 2:
            hours = "0"+str(hours)
            #print(hours)
        else:
            hours = str(hours)
        if len(str(minutes)) < 2:
            minutes = "0"+str(minutes)
            #print(minutes)
        else:
            minutes = str(minutes)
        all_alarm_times.append(hours + ":" + minutes)


def load_all_songs():
    downloaded_music_files.clear()
    with open("Resources/Downloads/downloaded_music_paths.txt", "r") as file:
        downloaded_music_files.append(file.readline().rstrip("\n"))
    print(downloaded_music_files)


def delete_old_songs():
    delete_files = glob.glob('Resources/Downloads/Music/*')
    for file_to_be_deleted in delete_files:
        os.remove(file_to_be_deleted)
    print("All the old songs are deleted...")


def download_all_musics(path, all_alarms_url_path):
    paths = open("Resources/Downloads/downloaded_music_paths.txt", "w+")
    downloaded_music_files.clear()
    paths.truncate(0)
    for i in all_alarms_url_path:
        music_uri = requests.get(i)
        temp_index = all_alarm_musics.index(i)
        temp_name = all_alarm_ids[temp_index]
        temp_music_name = re.sub('[^A-Za-z0-9]+', "", temp_name)
        temp_path = r"{0}/{1}".format(path, temp_music_name)
        with open(temp_path + ".mp3", 'wb+') as music_file:
            music_file.write(music_uri.content)
        paths.write(temp_path + ".mp3" + "\n")
        downloaded_music_files.append(temp_path + ".mp3")
        print("adding/updating a music file")
    print("ALL MUSIC FILES ARE DOWNLOADED")
    print(downloaded_music_files)
    paths.close()


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

def Thread_to_display_time_on_LCD():
    now = datetime.now()
    day_num = datetime.today().weekday()
    day = str(calendar.day_name[day_num])
    time = str(now.strftime("%H:%M:%S"))
    date = str(now.strftime("%d/%m/%Y"))
    # Here you write te code to display time


def mainLoopWhenNotConnectedToInternet():
    load_all_songs()
    try:
        refill_the_data_to_variables_from_storage()
    except:
        print("There is no data found in the account to play alarm")

    playing = False
    while not connected_to_internet:
        now = datetime.now()
        day_num = datetime.today().weekday()
        day = str(calendar.day_name[day_num])
        time = str(now.strftime("%H:%M"))
        #print(time)
        # print("Downloaded music files:" + str(downloaded_music_files))
        #print(all_alarm_times)
        if time in all_alarm_times:
            index = all_alarm_times.index(time)
            if day in all_alarm_days_selected[index]:
                if all_alarm_plays[index]:
                    print("Alarm time now")
                    if not playing:
                        mixer.music.load(downloaded_music_files[index])
                        mixer.music.play(-1)
                        playing = True
                        if all_alarm_everyday[index] == False:
                            pass
                            # you cannot perform under following operations as, you are not reachable to the internet
                            #databases = firebase.database().child("alarms_users").child(uid).child(all_alarm_ids[index])
                            #databases.update({"play": False})

#################################################################################################
#                                  THE MAIN PROGRAM STARTS HERE                                 #
#################################################################################################

mixer.init()
file = open(pathOfConfig, )
config = json.load(file)
file.close()
firebase = pyrebase.initialize_app(config)
connected_to_internet = False
try:
    check_internet = requests.get("https://www.google.com/", timeout=2)
    print("IoT Alarm is connected to internet :)")
    connected_to_internet = True
except:
    print("NO INTERNET! :< . DEVICE READS PREVIOUS DATA AND ALARMS ACCORDING TO IT")

while True:
    if connected_to_internet:
        uid, stream = first_time_init(firebase)
        if uid is not None and stream is not None:
            print("STARTed IN MODE")
            load_all_songs()
            try:
                refill_the_data_to_variables_from_storage()
            except:
                print("There is no data found in the account to play alarm")


            playing = False
            while connected_to_internet:
                now = datetime.now()
                day_num = datetime.today().weekday()
                day = str(calendar.day_name[day_num])
                time = str(now.strftime("%H:%M"))
                #print(time)
                #print("Downloaded music files:" + str(downloaded_music_files))
                #print(all_alarm_times)
                if time in all_alarm_times:
                    index = all_alarm_times.index(time)
                    if day in all_alarm_days_selected[index]:
                        if all_alarm_plays[index]:
                            print("Alarm time now")
                            if not playing:
                                mixer.music.load(downloaded_music_files[index])
                                mixer.music.play(-1)
                                playing = True
                                if all_alarm_everyday[index]==False:
                                    databases = firebase.database().child("alarms_users").child(uid).child(all_alarm_ids[index])
                                    databases.update({"play":False})



        else:
            print("OOPS, PLEASE PAIR YOUR DEVICE WITH THE ACCOUNT, RESTART THE DEVICE AND TRY AGAIN")
            keep_in_while_loop_until_restart = True
            while keep_in_while_loop_until_restart:
                pass # NO PROGRAMME CAN BE WRITTEN HERE
    else:
        inner_condition = False
        try:
            refill_the_data_to_variables()
            print("RETRIEVED PREVIOUSLY SAVED DATA")
            inner_condition = True
        except:
            print("OH YOU MIGHT SEEM TO BE A NEW USER :> YOU DONT HAVE ANY ALARMS IN YOUR ACCOUNT :)")
            print("Get me synced to internet!. Once you get internet")
            # Write a program in try except block to detect inteernet, if intreernt iss pressent then direclty kill the process and relaunch it. this can be done only in linucx environement
            while not inner_condition:
                pass
        while not connected_to_internet:
            pass
            # This shall be taken care in linux environment
            mainLoopWhenNotConnectedToInternet()
