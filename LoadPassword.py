import mouse
import keyboard
import pyperclip
from time import time
from time import sleep 

USR_DELAY = 5 #Seconds to wait before automating the mouse
COPY_DEL = 0.3 #Seconds to wait before coping, needed because it breaks otherwise
MOVE_DEL = 0.1 #Seconds to use for each mouse movement

#Struct base def that holds captured data for further processing
outStruct = {
    "user": "",
    "pass": "",
    "URI": ""
}
#List of positions of where to click
positions = {
    "user": [1500, 218],
    "pass": [1500, 300],
    "URI": [1500, 380],
    "list1": [410, 100],
    "list2": [410, 145]
}
#Moves to do 
moves = ["user", "pass", "URI"]

#Get number of credentials to capture
getUsr = True
while getUsr:
    usrInStr = input("How many elementqqqs do you want to back up?\n")
    if usrInStr != "":
        usrIn = int(usrInStr)
        if usrIn > 0:
            getUsr = False
        else:
            print("Please insert positve number!")
    else:
        print("Inser a valid number!")
MAX = usrIn

#Struct array that holds captured data for further processing
structArr = [dict(outStruct) for x in range(MAX)]
scrollC = 1

#Get the credentials at a certain index
#NOTE: doesn't work well with last page of credentials, also has bugs and takes some values twice others are missed!
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
#Extract the data from the application
def extractData(MAX, COPY_DEL, MOVE_DEL, positions, moves, structArr, selectAtIndex):
    
    print(f"This application should not be relied upon, it is VERY buggy!\nOnce you press y a timer of {USR_DELAY} seconds will start then the script will take mouse control")
    print("Open the bitwarden app in fullscreen mode before starting\nNOTE: The script was developed on a 1920 x 1080 screen with 100% scaling, it may not work on other resolutions")
    usrIn = input("Insert y if you want to start the recovery, q to abort:\n")
    while usrIn != "y":
        if usrIn == "q":
            exit()
        usrIn = input("Insert y if you want to start the recovery:")
    print("CAUTION, the script is about to start!\nPRESS Q TO ABORT!")
    for i in range(USR_DELAY):
        print(f"You have {USR_DELAY - i} seconds before the robot takes over")
        sleep(1)

    i=0
    moveC = 0 #Counts the moves (limited to len(moves))
    totC = 0 #Current total elemnt count
    selectAtIndex(totC)

    while i < (MAX*len(moves)):
        currentMove = moves[moveC]
        mouse.move(positions[currentMove][0], positions[currentMove][1], True, MOVE_DEL)
        mouse.click()
        sleep(COPY_DEL)
        tmp = pyperclip.paste()
    
        print(f"Value:{tmp}, Move:{currentMove}, Elements found:{totC}")
        structArr[totC][currentMove] = tmp
        moveC += 1
        if( moveC == len(moves)):
            totC += 1
            selectAtIndex(totC)
            moveC = 0
    
        if keyboard.is_pressed('q'):
            print("Process aborted prematurely, saving data...")
            saveCsv(totC, structArr)
            exit()
        i+=1

    print(f"Extraction completed, {totC} out of {MAX} logins have been recorded")

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
    errors = 0
    lines = 0
    outArr = [dict(outDataStruct) for x in range(MAX)]
    for i, item in enumerate(structArr):
        outArr[i]["username"] = item["user"]
        outArr[i]["password"] = item["pass"]
        outArr[i]["url"] = item["URI"]

        if item["URI"] == item["pass"]:
            outArr[i]["url"] = "UNKOWN"
            errors += 1

        if "http" in item["URI"] :
            outArr[i]["httpRealm"] = item["URI"]
            outArr[i]["guid"] = item["URI"]
        else:
            outArr[i]["httpRealm"] = ""
            errors += 1
        
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
                lines += 1
    print(f"Succesfully written {lines} lines of which {errors} are probably broken")




extractData(MAX, COPY_DEL, MOVE_DEL, positions, moves, structArr, selectAtIndex)
saveCsv(MAX, structArr)