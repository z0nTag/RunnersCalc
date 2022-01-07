import datetime
from os.path import exists
import Runner as run
import Database as db
import Calculate as calc
import json
#import pandas as pd
import requests

# race related
time = 0
distance_km = 0.0
pace = 0
spm = 0
bpm = 0
beat_max = 0

# person related
name = ""
age = 0
height = 0
weight = 0.0
ap_max = 0
ap_min = 0
bmi_score = 1

url = "https://covid-193.p.rapidapi.com/statistics"

querystring = {"country":"sweden"}

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "2ffc369b8bmsh8748918e32e322ep1da2c4jsne6003a2bc283"
    }

response = None
try:
    response = requests.request("GET", url, headers=headers, params=querystring)
except ConnectionError as e:
    print("Error trying to connect to api\n", e, end='\n')

if response is not None:
    json_data = response.json()

    with open('covid.json', 'w') as jsonFile:
        json.dump(json_data, jsonFile)
        jsonFile.close()


print("Welcome to the low pulse race calculator 1.0\n")

while True:

    try:
        print("1. Login  2. Register user  3. Delete user  0. Continue without login")
        choice = int(input("Enter choice: "))
    except ValueError as e:

        print("Only numbers accepted. Please enter a number\n")
        continue

    if choice == 0:
        print("\nLow pulse calculator with no user loaded:\n")
        break

    elif choice == 1:
        db.login()

    elif choice == 2:
        db.register()

    elif choice == 3:
        db.delete_user()

    else:
        print("Choice not available. Please try again\n")

    continue

while True:

    try:
        print("1. Racer  2. Race  3. Calculate race  4. Load racer  0. Exit 999. Covid-19 stats")
        choice = int(input("Enter choice: "))
    except ValueError as e:

        print("Only numbers accepted. Please enter a number\n")
        continue

    if choice == 0:
        break

    elif choice == 999:
        if exists("covid.json") and response is not None:

            try:
                with open("covid.json") as jsonFile:
                    jsonObject = json.load(jsonFile)
                    jsonFile.close()

                response = jsonObject["response"]
                keys = dict(response[0])

                a = keys.keys()
                counter = 0
                for key01 in a:

                    if key01 == "cases" or key01 == "deaths" or key01 == "tests":
                        print(str(key01).capitalize(), end=' = ')
                        key02 = dict(keys.get(key01))
                        b = key02.keys()
                        for key03 in b:
                            print(str(key03).capitalize(), key02.get(key03), sep=': ', end=' ')
                        if counter < 3:
                            print("")
                            counter += 1
                    else:
                        print(str(key01).capitalize(), keys.get(key01), sep=' = ')
            except Exception as e:
                print("Error loading covid stats. Response = ", response, sep='')
        else:
            print("No file found or connection error to api")

        print("")

    elif choice == 1:   ## Personal data

        name = input("Enter your name: ")

        while True:
            try:
                height = int(input("Enter your height in cm: "))
            except ValueError as e:
                print("\n *Only whole numbers accepted* \n")
                continue
            break
        while True:
            try:
                weight = int(input("Enter your weight in kg: "))
            except ValueError as e:
                print("\n *Only whole numbers accepted* \n")
                continue
            break

        stats = run.stats(age, weight, height)

        ap_min = stats[0]
        ap_max = stats[1]
        bmi_score = stats[2]

        json_data = {"name": name, "age": age, "height": height, "weight": weight}

        with open(name + '.json', 'w') as jsonFile:
            json.dump(json_data, jsonFile)
            jsonFile.close()
        print("Runner ", name, " created with data:\n", json_data, sep='')

    elif choice == 2:   ## Race data

        if name != "":
            print("Enter the race result: ")

            try:
                distance_km = float(input("Enter distance: "))
            except ValueError as e:
                print("Enter only numbers\n")

            try:
                time = int(input("Enter time in minutes: "))
                bpm = int(input("Enter average beat per minute: "))

                if bpm > ap_max:
                    print("Average bpm needs to be below ", str(ap_max), "\n"
                            "This is not considered a low pulse race. Please come back again.")
                    exit()

                beat_max = int(input("Enter maximum beat: "))
                spm = int(input("Enter steps per minute: "))
            except ValueError as e:
                print("Enter only whole numbers\n", e)

            pace = int(time / distance_km)
        else:
            print("Please register or load a runner before you register a race\n")

    elif choice == 3:

        if name != "" and time != 0:
            ## low beat race calcutations

            pulse_score_01 = ap_max - bpm
            pulse_score_02 = ap_max - beat_max

            if pulse_score_02 < -20:
                print("Your maximum beat was too high. This is not considered a low pulse race. Please come back again.")
                exit()

            if ap_min > bpm:
                print("Beats per minutes was too low. This is not considered a low pulse race. Please come back again.")
                exit()

            pulse_score_total = pulse_score_01 + pulse_score_02

            if pulse_score_total > 10:
                score = 1.3
            elif pulse_score_total < 10 > 5:
                score = 1.2
            elif pulse_score_total > 0 < 5:
                score = 1.1
            elif pulse_score_total < 0:
                score = 0.9
            else:
                score = 1.0

            final_pulse_score = pulse_score_01 * score

            final_score = calc.calc_score(ap_max, bpm, score, distance_km, pace, time, spm, bmi_score)
            total_score = final_score * final_score

            print("Total score before 2 dec: ", final_score)

            total_score_2dec = format(final_score, ".2f")

            print("Total score after 2 dec: ", total_score_2dec)
            print("Score without sqrt: ", str(total_score))
            print("Score with sqrt: ", str(final_score))
            print("Your score ", name + " are: ", format(final_score, ".2f"))

        elif name == "" and time != 0:
            print("No runner loaded. Please register och load a runner\n")
        elif name != "" and time == 0:
            print("No race registered or values left at 0\n")
        else:
            print("No race and runner registered\n")

    elif choice == 4:
        filename = input("Please enter your name: ")

        if exists(filename + ".json"):

            with open(filename + ".json") as jsonFile:
                jsonObject = json.load(jsonFile)
                jsonFile.close()

            name = jsonObject['name']
            age = jsonObject['age']
            height = jsonObject['height']
            weight = jsonObject['weight']

            print("Runner loaded:", name, age, height, weight, '', sep="\n")

            stats = run.stats(age, weight, height)

            ap_min = stats[0]
            ap_max = stats[1]
            bmi_score = stats[2]
        else:
            print("Runner ", filename, " not found", sep='')
    else:
        print("Choice not available. Please try again\n")

    continue

print("Goodbye! Thank you for using the low pulse calculator :)")
exit()
