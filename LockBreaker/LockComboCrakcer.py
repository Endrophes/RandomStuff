# Python 3

import json

MAX_VALUE = 9999
COMBO_FILE = "comboTracking.json"

run = True

combinations = dict()

def generateCombos():
    for i in range(0, MAX_VALUE+1):
        combinations["{:04d}".format(i)] = ""

def save():
    json_object = json.dumps(combinations, indent=4)
    with open(COMBO_FILE, "w") as f:
        f.write(json_object)

def load():
    loadedData = dict()
    with open(COMBO_FILE, "r") as f:
        loadedData = json.load(f)
    return loadedData

while run:

    userInput = input("please input a command\n")

    match userInput:
        case "Exit" | "exit":
            # userInput = input("Save progress?\n")
            save()
            print("Access terminated by user")
            run = False
        case "Start" | "start":
            generateCombos()
            print("READY!!")
        case "Load" | "load":
            combinations = load()
            print("loaded")
        case "Save" | "save":
            save()
            print("saved")
        case _:
            result = userInput.split("-")
            if result[0].isnumeric():
                if combinations[result[0]] != '':
                    print("You tried that one already")
                else:
                    if result[1] == "*":
                        print("Damn!")
                    if result[1] == "+":
                        print("The Winner man!")
                    combinations[result[0]] = "x"
                    save() #Boooo!!!!!
            print("Combo Tested And Saved")
            # TODO: Save on every input
        
    