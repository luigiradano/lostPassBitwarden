import mouse
import keyboard
import pyperclip
from time import time
from time import sleep 

MAX = 180
COPY_DEL = 0.3
MOVE_DEL = 0.1

outStruct = {
    "user": "",
    "pass": "",
    "URI": ""
}
positions = {
    "user": [1500, 218],
    "pass": [1500, 300],
    "URI": [1500, 380],
    "list1": [410, 100],
    "list2": [410, 145]
}

moves = ["user", "pass", "URI"]

structArr = [dict(outStruct) for x in range(MAX)]
scrollC = 1


def selectAtIndex(i):
    global scrollC
    stepY = positions["list2"][1] - positions["list1"][1]
   

    if i > 15 * scrollC:
        mouse.move(positions["list1"][0], positions["list1"][1], True, MOVE_DEL)
        mouse.wheel(-6)
        scrollC += 1

    totalMove = stepY * (i-15*(scrollC -1))

    
    totalMove += positions["list1"][1]
    mouse.move(positions["list1"][0], totalMove, True, MOVE_DEL)
    mouse.click()

def extractData(MAX, COPY_DEL, MOVE_DEL, positions, moves, structArr, selectAtIndex):
    print("You have 3 seconds to switch windows")
    sleep(3)
    i=0
    moveC = 0
    totC = 0
    selectAtIndex(totC)

    while i < (MAX*len(moves)):
        currentMove = moves[moveC]
        mouse.move(positions[currentMove][0], positions[currentMove][1], True, MOVE_DEL)
        mouse.click()
        sleep(COPY_DEL)
        tmp = pyperclip.paste()
    
        print(tmp, currentMove, moveC)
        structArr[totC][currentMove] = tmp
        moveC += 1
        if( moveC == len(moves)):
            totC += 1
            selectAtIndex(totC)
            moveC = 0
    
        if keyboard.is_pressed('q'):
            exit()
        i+=1

    print(f"{totC} logins have been recorded")

def saveCsv(MAX, structArr):
    field_names = ["url","username","password","httpRealm","formActionOrigin","guid","timeCreated","timeLastUsed","timePasswordChanged"]
    outDataStruct = {
    "username": "",
    "password": "",
    "url": "",
    "httpRealm": "",
    "formActionOrigin": "",
    "guid": "",
    "timeCreated": "",
    "timeLastUsed": "",
    "timePasswordChanged": ""
}

    outArr = [dict(outDataStruct) for x in range(MAX)]
    for i, item in enumerate(structArr):
        outArr[i]["username"] = item["user"]
        outArr[i]["password"] = item["pass"]
        outArr[i]["url"] = item["URI"]

        if item["URI"] == item["pass"]:
            outArr[i]["url"] = "UNKOWN"

        if "http" in item["URI"] :
            outArr[i]["httpRealm"] = item["URI"]
            outArr[i]["guid"] = item["URI"]
        else:
            outArr[i]["httpRealm"] = ""
        
        outArr[i]["timeCreated"] = str(time())
        outArr[i]["timeLastUsed"] = str(time()+1000)
        outArr[i]["timePasswordChanged"] = str(time+2000)

    with open('out.csv', 'w') as csvfile:
        csvfile.write('"url","username","password","httpRealm","formActionOrigin","guid","timeCreated","timeLastUsed","timePasswordChanged"\n')
        for item in outArr:
            if item["url"] != "":
                for field in field_names:
                    csvfile.write('"' + item[field] + '",')
                csvfile.write("\n")




extractData(MAX, COPY_DEL, MOVE_DEL, positions, moves, structArr, selectAtIndex)
saveCsv(MAX, structArr)