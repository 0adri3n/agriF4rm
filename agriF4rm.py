import os, sqlite3
import random
from lib import externalfunctions, rpc
import tkinter
import sched, time
import threading
import math
from tkinter import ttk
import yaml
from PIL import Image
import tkinter
import tkinter.font as font
import tkinter
import sys
from tkinter.messagebox import askyesno
from pystray import MenuItem as item
import pystray



CLIENT_ID = "1088200928122904607" # Discord RPC Application ID
ID_ACTUAL_USER = None
START_TIME = time.time()


def createfieldStart(username):

    global logLabel2
    global firstConn
    global ID_ACTUAL_USER

    if username != "":

        hash = externalfunctions.random_string(16)
        id = externalfunctions.random_string(10)
        data = (id, username, hash)

        conn = sqlite3.connect('data/field_database.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT username FROM users WHERE username=?""", (username,))


        if cursor.fetchone() !=  None:
            
            logLabel2.configure(text="User already exists.", fg="red")
            cursor.close()

        else:

            cursor.close()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO users(id, username, hashfield) VALUES(?, ?, ?)""", data)
            conn.commit()

            cursor.close()

            data = (hash, 10, 0, 0, 1000, 0, 0, 0, 0)
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO fieldsdetails(hashfield, dimension, rentability, bleamount, money, basic_agri, rare_agri, epic_agri, legendary_agri) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)
            conn.commit()

            logLabel2.configure(text="User created ! Starting agriF4rm...", fg="green")
            ID_ACTUAL_USER= id
            time.sleep(2)
            firstConn.destroy()

    else:

        logLabel2.configure(text="Please enter a username.", fg="red")


settingsfiles = open("config/settings.yaml", "r")
settingsData = yaml.safe_load(settingsfiles)
settingsfiles.close()

ID_ACTUAL_USER = settingsData["lastID"]

if ID_ACTUAL_USER == "None":

    firstConn = tkinter.Tk()
    firstConn.geometry("400x200")
    firstConn.title("agriF4rm")
    firstConn.maxsize(400, 200)
    firstConn.minsize(400, 200)
    if sys.platform == "win32":
        firstConn.iconbitmap("src/img/agricultureICO.ico")
    police = font.Font(family='Courier', size=11)

    firstConn.configure(bg="black")

    welcomeLabel = tkinter.Label(firstConn, text="Welcome in agriF4rm !\nPlease create ur first user to play :)", fg="white", bg="black")
    welcomeLabel.place(x=30, y=10)
    welcomeLabel["font"] = police

    createUserLabel = tkinter.Label(firstConn, text="Username : ", bg="black", fg="white")
    createUserLabel.place(x=30, y=60)
    createUserLabel["font"] = police

    createUserEntry = tkinter.Entry(firstConn, bg="black", fg="white")
    createUserEntry.place(x=145, y=60)
    createUserEntry["font"] = police

    createUserButton = tkinter.Button(firstConn, text="Create", bg="black", fg="white", command=lambda: createfieldStart(createUserEntry.get()))
    createUserButton.place(x=145, y=100)
    createUserButton["font"] = police

    logLabel2 = tkinter.Label(firstConn, text="", bg="black", fg="red")
    logLabel2.place(x=30, y=150)
    logLabel2["font"] = police

    firstConn.mainloop()


def createfield(username):

    global logLabel
    global logLabel2
    global firstConn

    if username != "":

        hash = externalfunctions.random_string(16)
        id = externalfunctions.random_string(10)
        data = (id, username, hash)

        conn = sqlite3.connect('data/field_database.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT username FROM users WHERE username=?""", (username,))


        if cursor.fetchone() !=  None:
            
            logLabel.configure(text="User already exists.", fg="red")
            cursor.close()

        else:

            cursor.close()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO users(id, username, hashfield) VALUES(?, ?, ?)""", data)
            conn.commit()

            cursor.close()

            data = (hash, 10, 0, 0, 1000, 0, 0, 0, 0)
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO fieldsdetails(hashfield, dimension, rentability, bleamount, money, basic_agri, rare_agri, epic_agri, legendary_agri) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)
            conn.commit()

            logLabel.configure(text="User created !", fg="green")

    else:

        logLabel.configure(text="Please enter a username.", fg="red")


def switchUser(username):

    global ID_ACTUAL_USER
    global choiceListCombo
    global logLabel
    global actualLabel

    if choiceListCombo.get() != "":

        conn = sqlite3.connect('data/field_database.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT id FROM users WHERE username=?""", (username,))

        ID_ACTUAL_USER = cursor.fetchone()[0]
        cursor.close()

        logLabel.configure(text="User switched !", fg="green")

        actualLabel.configure(text="Actual user : " + username)
        updateLabels(True)

    else:
        logLabel.configure(text="Please select a user.", fg="red")

def deleteUser(username):

    global ID_ACTUAL_USER
    global choiceListCombo
    global logLabel
    global actualLabel

    if choiceListCombo.get() != "":

        conn = sqlite3.connect('data/field_database.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT id FROM users WHERE username=?""", (username,))

        id_user2del = cursor.fetchone()[0]

        if id_user2del == ID_ACTUAL_USER:
            logLabel.configure(text="Can't delete actual user.", fg="red")

        else:

            answer = askyesno(title='Confirmation',message='Are you sure that you want to delete this user ?')
            if answer :
                cursor.execute("""SELECT hashfield FROM users WHERE username=?""", (username,))
                hashfieldDel = cursor.fetchone()[0]
                cursor.execute("""DELETE FROM users WHERE username=?""", (username,))
                cursor.execute("""DELETE FROM fieldsdetails WHERE hashfield=?""", (hashfieldDel,))
                conn.commit()
                logLabel.configure(text="User removed !", fg="green")
                cursor.close()

            else :

                logLabel.configure(text="Deletion canceled.", fg="red")


        updateLabels(True)
        cursor.close()


    else:
        logLabel.configure(text="Please select a user.", fg="red")


def fieldinfo():

    global ID_ACTUAL_USER

    conn = sqlite3.connect('data/field_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT id FROM users WHERE id=?""", (ID_ACTUAL_USER,))


    if cursor.fetchone() !=  None:
        
        cursor.execute("""SELECT hashfield FROM users WHERE id=?""", (ID_ACTUAL_USER,))
        data = cursor.fetchone()
        hashfield = data[0]

        cursor.execute("""SELECT dimension, rentability, bleamount, money, basic_agri, rare_agri, epic_agri, legendary_agri FROM fieldsdetails WHERE hashfield=?""", (hashfield,))
        data = list(cursor.fetchone())
        dicofieldinfo = []
        for i in data:
            dicofieldinfo.append(i)


        return(dicofieldinfo)


def clearLabel(lab):

    time.sleep(10)
    lab.configure(text="")


def multiroll(quantity):

    global ID_ACTUAL_USER
    global resultsRollLabel

    conn = sqlite3.connect('data/field_database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT id FROM users WHERE id=?""", (ID_ACTUAL_USER,))

    if cursor.fetchone() !=  None:

        if quantity != "" and quantity.isdigit() and int(quantity) > 0:

            cursor.execute("""SELECT hashfield FROM users WHERE id=?""", (ID_ACTUAL_USER,))
            hashfield = cursor.fetchone()[0]

            cursor.execute("""SELECT money FROM fieldsdetails WHERE hashfield=?""", (hashfield,))
            money = cursor.fetchone()[0]
            m = False
            if quantity == "max":
                quantity = int(int(money)/500)
                m = True
            if int(money) < 500*int(quantity) and not m or int(money) < int(quantity) and m:
                resultsRollLabel.configure(text="Not enough money.")
                clearThread = threading.Thread(target=lambda: clearLabel(resultsRollLabel))
                clearThread.start()
            else:

                resultsRollLabel.configure(text="Right, let me recruit agricultors for you...")
                
                money = money - 500*int(quantity)
                cursor.execute("""UPDATE fieldsdetails SET money = ? WHERE hashfield = ?""", (money, hashfield))
                conn.commit()
                agriList = ["basic", "rare", "epic", "legendary"]
                basic = 0
                rare = 0
                epic = 0
                legend = 0
                for i in range(int(quantity)):
                    pickedagri = random.choices(agriList, weights=(65, 20, 10, 5), k=1)[0]
                    if pickedagri == "basic" :
                        basic += 1
                    elif pickedagri == "rare" :
                        rare += 1
                    elif pickedagri == "epic" :
                        epic += 1
                    elif pickedagri == "legendary" :
                        legend += 1
                cursor.execute("""SELECT basic_agri FROM fieldsdetails WHERE hashfield=?""", (hashfield,))
                basicamount = cursor.fetchone()[0]
                basicamount += basic
                cursor.execute("""UPDATE fieldsdetails SET basic_agri = ? WHERE hashfield = ?""", (basicamount, hashfield))
                conn.commit()

                cursor.execute("""SELECT rare_agri FROM fieldsdetails WHERE hashfield=?""", (hashfield,))
                rareamount = cursor.fetchone()[0]
                rareamount += rare
                cursor.execute("""UPDATE fieldsdetails SET rare_agri = ? WHERE hashfield = ?""", (rareamount, hashfield))
                conn.commit()

                cursor.execute("""SELECT epic_agri FROM fieldsdetails WHERE hashfield=?""", (hashfield,))
                epicamount = cursor.fetchone()[0]
                epicamount += epic
                cursor.execute("""UPDATE fieldsdetails SET epic_agri = ? WHERE hashfield = ?""", (epicamount, hashfield))
                conn.commit()

                cursor.execute("""SELECT legendary_agri FROM fieldsdetails WHERE hashfield=?""", (hashfield,))
                legendaryamount = cursor.fetchone()[0]
                legendaryamount += legend
                cursor.execute("""UPDATE fieldsdetails SET legendary_agri = ? WHERE hashfield = ?""", (legendaryamount, hashfield))
                conn.commit()

                externalfunctions.updaterenta(hashfield)
                resultsRollLabel.configure(text="Rolls result :\nBasics : " + str(basic) + "\nRares : " + str(rare) + "\nEpics : " + str(epic) + "\nLegendaries : " + str(legend))
                updateLabels(False)

                clearThread = threading.Thread(target=lambda: clearLabel(resultsRollLabel))
                clearThread.start()

        else:

            resultsRollLabel.configure(text="Please enter\na correct amount.")
    


def upgrade():

    global ID_ACTUAL_USER
    global upgradeLog

    conn = sqlite3.connect('data/field_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT id FROM users WHERE id=?""", (ID_ACTUAL_USER,))


    if cursor.fetchone() !=  None:
        
        cursor.execute("""SELECT hashfield FROM users WHERE id=?""", (ID_ACTUAL_USER,))
        hashfield = cursor.fetchone()[0]
    
        cursor.execute("""SELECT dimension, money FROM fieldsdetails WHERE hashfield=?""", (hashfield,))
        data = list(cursor.fetchone())
        dimension = data[0]
        money = data[1]

        dimensiondico = {10: 0, 25: 100000, 50: 1000000, 100: 25000000, 200: 1250000000, 500: 62500000000, 1000: 3125000000000}
        

        key = dimension

        temp = list(dimensiondico)
        try:
            res = temp[temp.index(key) + 1]
        except (ValueError, IndexError):
            res = None

        try:
            if money < dimensiondico[res] :

                upgradeLog.configure(text="Not enough money.")

            else:


                cursor.execute("""UPDATE fieldsdetails SET dimension = ? WHERE hashfield = ?""", (res, hashfield))
                conn.commit()

                diff = money - dimensiondico[res]
                cursor.execute("""UPDATE fieldsdetails SET money = ? WHERE hashfield = ?""", (diff, hashfield))
                conn.commit()

                upgradeLog.configure(text="Field upgraded.")
                updateLabels(False)
        except KeyError:
            pass
                
            

        externalfunctions.updaterenta(hashfield)

    clearThread = threading.Thread(target=lambda: clearLabel(upgradeLog))
    clearThread.start()



def sell():

    global ID_ACTUAL_USER
    global sellLog

    conn = sqlite3.connect('data/field_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT id FROM users WHERE id=?""", (ID_ACTUAL_USER,))


    if cursor.fetchone() !=  None:
        
        cursor.execute("""SELECT hashfield FROM users WHERE id=?""", (ID_ACTUAL_USER,))
        hashfield = cursor.fetchone()[0]
    
        cursor.execute("""SELECT money, bleamount FROM fieldsdetails WHERE hashfield=?""", (hashfield,))
        data = list(cursor.fetchone())
        money = float(data[0])
        wheatamount = float(data[1])

        price = externalfunctions.getwheatprice()
        updatedmoney = round(money + (wheatamount*price), 2)

        cursor.execute("""UPDATE fieldsdetails SET money = ? WHERE hashfield=?""", (updatedmoney, hashfield))
        conn.commit()

        wheatamount = 0
        cursor.execute("""UPDATE fieldsdetails SET bleamount = ? WHERE hashfield=?""", (wheatamount, hashfield))
        conn.commit()

        sellLog.configure(text="You make\n" + str(updatedmoney-money) + "$\n of profit !")

    updateLabels(True)
    clearThread = threading.Thread(target=lambda: clearLabel(sellLog))
    clearThread.start()


def getUpgradesList():

    return({10: 0, 25: 100000, 50: 1000000, 100: 25000000, 200: 1250000000, 500: 62500000000, 1000: 3125000000000})


def updateLabels(fromSwitch):

    global START_TIME

    fieldData = fieldinfo()
    wheatPrice = externalfunctions.getwheatprice()
    
    dimLabel.configure(text="Dimension : " + str(fieldData[0]))
    rentLabel.configure(text="Profitability (w): " + str(fieldData[1]) + "/h | " + str(round(float(fieldData[1]/60), 2)) + "/m")
    rentDollarLabel.configure(text="Profitability ($): " + str(fieldData[1]*wheatPrice) + "/h | " + str(round(float(fieldData[1]*wheatPrice/60), 2)) + "/m")
    wheatLabel.configure(text="Wheat amount : " + str(fieldData[2]))
    moneyLabel.configure(text="Money balance : " + str(round(fieldData[3], 2)))
    basicAgri.configure(text="Basic agricultors : " + str(fieldData[4]))
    rareAgri.configure(text="Rare agricultors : " + str(fieldData[5]))
    epicAgri.configure(text="Epic agricultors : " + str(fieldData[6]))
    legenAgri.configure(text="Legendary agricultors : " + str(fieldData[7]))

    sellingValue.configure(text=str(wheatPrice) + "$")

    settingsfiles = open("config/settings.yaml", "r")
    settingsData = yaml.safe_load(settingsfiles)
    settingsfiles.close()

    playTime = settingsData["totalPlayTime"]
    updatedPlaytime = playTime + (time.time() - START_TIME)
    playTime = round(round(int(updatedPlaytime), 0)/3600, 2)

    playTimeLabel.configure(text="Time played : " + str(playTime) + "h")

    upgradeDict = getUpgradesList()
    upgradeList = list(upgradeDict)
    indexActualDim = upgradeList.index(fieldData[0])
    try:
        nextDim = upgradeList[indexActualDim+1]
        nextDimLabel.configure(text="Next upgrade :\n\n" + str(nextDim) + " : " + str(upgradeDict[nextDim]) + "$")
        actualX = nextDimLabel.place_info()
        if not fromSwitch:
            if nextDim < 51:
                nextDimLabel.place(x=int(actualX["x"]) + len(str(upgradeDict[nextDim])), y=345)
            else:
                nextDimLabel.place(x=int(actualX["x"]) - len(str(upgradeDict[nextDim]))/2, y=345)
        else:
            if nextDim < 51:
                nextDimLabel.place(x=475 + len(str(upgradeDict[nextDim])), y=345)
            else:
                nextDimLabel.place(x=475 - len(str(upgradeDict[nextDim]))/2, y=345)


    except IndexError:
        nextDimLabel.configure(text="Next upgrade :\n\nMax dimension reached.")
        nextDimLabel.place(x=460, y=345)


def renta_loop(scheduler): 

    global ID_ACTUAL_USER

    scheduler.enter(60, 1, renta_loop, (scheduler,))

    conn = sqlite3.connect('data/field_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT hashfield FROM users WHERE id=?""", (ID_ACTUAL_USER,))
    hashfield = cursor.fetchone()[0]

    cursor = conn.cursor()
    cursor.execute("""SELECT rentability, bleamount FROM fieldsdetails WHERE hashfield=?""", (hashfield,))
    data = list(cursor.fetchone())
    renta = float(data[0])
    w = data[1]

    updatedwheat = round(renta/60 + w, 2)

    cursor.execute("""UPDATE fieldsdetails SET bleamount = ? WHERE hashfield=?""", (updatedwheat, hashfield))
    conn.commit()
    cursor.close()

    fieldData = fieldinfo()
    wheatPrice = externalfunctions.getwheatprice()
    
    dimLabel.configure(text="Dimension : " + str(fieldData[0]))
    rentLabel.configure(text="Profitability (w): " + str(fieldData[1]) + "/h | " + str(round(float(fieldData[1]/60), 2)) + "/m")
    rentDollarLabel.configure(text="Profitability ($): " + str(fieldData[1]*wheatPrice) + "/h | " + str(round(float(fieldData[1]*wheatPrice/60), 2)) + "/m")
    wheatLabel.configure(text="Wheat amount : " + str(fieldData[2]))
    moneyLabel.configure(text="Money balance : " + str(round(fieldData[3], 2)))
    basicAgri.configure(text="Basic agricultors : " + str(fieldData[4]))
    rareAgri.configure(text="Rare agricultors : " + str(fieldData[5]))
    epicAgri.configure(text="Epic agricultors : " + str(fieldData[6]))
    legenAgri.configure(text="Legendary agricultors : " + str(fieldData[7]))

    sellingValue.configure(text=str(wheatPrice) + "$")

    settingsfiles = open("config/settings.yaml", "r")
    settingsData = yaml.safe_load(settingsfiles)
    settingsfiles.close()

    playTime = settingsData["totalPlayTime"]
    updatedPlaytime = playTime + (time.time() - START_TIME)
    playTime = round(round(int(updatedPlaytime), 0)/3600, 2)

    playTimeLabel.configure(text="Time played : " + str(playTime) + "h")



def getActualUser():

    global ID_ACTUAL_USER

    conn = sqlite3.connect('data/field_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT username FROM users WHERE id=?""", (ID_ACTUAL_USER,))
    return(list(cursor.fetchall())[0])

def getAllUsers():

    conn = sqlite3.connect('data/field_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT username FROM users""")
    return(list(cursor.fetchall()))


def saveSettings(rpcVar, settingsData, bgFileName):


    settingsData["rpc"] = rpcVar.get()
    settingsData["bgFileName"] = bgFileName.get()

    settingsWrite = open("config/settings.yaml", "w")
    settingsWrite.write(yaml.dump(settingsData, default_flow_style=False))
    settingsWrite.close()

    ToggleDiscordRpc(rpcVar.get())

    newBg = tkinter.PhotoImage(file="src/img/" + bgFileName.get())
    bg.configure(image=newBg)
    bg.image = newBg


def StartRPC():            

    global CLIENT_ID
    global rpc_obj

    rpc_obj = rpc.DiscordIpcClient.for_platform(CLIENT_ID)
    start_time = time.mktime(time.localtime())
    activity = {
                "timestamps": {
            "start": start_time
            },
            "details": "Farming...",  
            "assets": {
                "large_text": "agriF4rm",
                "large_image": "logosquare" 
            },
            "buttons" : [{"label" : "website", "url" : "https://akira-trinity.github.io/agriF4rm/docs/index.html"}]
    }
    
    rpc_obj.set_activity(activity)

def CheckRpcSet():

    global rpc_obj

    with open("config/settings.yaml", "r") as conf:
        confData = yaml.safe_load(conf)
        if confData["rpc"] == 1:
            StartRPC()
        else:
            try:
                rpc_obj.close()
            except:
                pass

def ToggleDiscordRpc(ChoosenMode):

    if ChoosenMode == 1:
        with open("config/settings.yaml", "r") as conf:
            confData = yaml.safe_load(conf)
            confData["rpc"] = 1

        with open("config/settings.yaml", "w") as conf:
            yaml.dump(confData, conf)
    else:
        with open("config/settings.yaml", "r") as conf:
            confData = yaml.safe_load(conf)
            confData["rpc"] = 0

        with open("config/settings.yaml", "w") as conf:
            yaml.dump(confData, conf)

    CheckRpcSet()


def insertMaxRolls():

    global rollAmountEntry

    fieldData = fieldinfo()

    moneyAmount = fieldData[3]
    maxRolls = math.floor(moneyAmount/500)

    rollAmountEntry.delete(0,tkinter.END)
    rollAmountEntry.insert(0, str(maxRolls))



def on_closing():

    global app
    global START_TIME

    settingsRead = open("config/settings.yaml", "r")
    settingsData = yaml.safe_load(settingsRead)
    settingsRead.close()

    savedPT = settingsData["totalPlayTime"]
    settingsData["lastID"] = ID_ACTUAL_USER
    settingsData["totalPlayTime"] = savedPT + (time.time() - START_TIME)

    settingsWrite = open("config/settings.yaml", "w")
    settingsWrite.write(yaml.dump(settingsData, default_flow_style=False))
    settingsWrite.close()

    app.destroy()


# GUI PART


def changeUserWindow():

    global logLabel
    global choiceListCombo
    global actualLabel

    userWin = tkinter.Toplevel()
    userWin.wm_title("User switch")
    userWin.wm_geometry("300x200")
    userWin.wm_minsize(300, 200)
    userWin.wm_maxsize(300, 200)
    if sys.platform == "win32":
        userWin.wm_iconbitmap("src/img/agricultureICO.ico")
    userWin.config(bg="black")
    police = font.Font(family='Courier', size=10)

    actualUser = getActualUser()[0]

    actualLabel = tkinter.Label(userWin, text="Actual user : " + actualUser, bg="black", fg="white")
    actualLabel.place(x=10, y=10)
    actualLabel["font"] = police

    createUserLabel = tkinter.Label(userWin, text="Create user : ", bg="black", fg="white")
    createUserLabel.place(x=10, y=40)
    createUserLabel["font"] = police

    createUserEntry = tkinter.Entry(userWin, bg="black", fg="white")
    createUserEntry.place(x=125, y=40)
    createUserEntry["font"] = police

    createUserButton = tkinter.Button(userWin, text="Create", bg="black", fg="white", command=lambda: createfield(createUserEntry.get()))
    createUserButton.place(x=125, y=70)
    createUserButton["font"] = police

    usersList = getAllUsers()

    choiceLabel = tkinter.Label(userWin, text="Switch user :", bg="black", fg="white")
    choiceLabel.place(x=10, y=110)
    choiceLabel["font"] = police

    choiceListCombo = ttk.Combobox(userWin, values=usersList)
    choiceListCombo.place(x=125, y=110, width=165)
    choiceListCombo["font"] = police

    switchUserButton = tkinter.Button(userWin, text="Switch", bg="black", fg="white", command=lambda: switchUser(choiceListCombo.get()))
    switchUserButton.place(x=125, y=140)
    switchUserButton["font"] = police

    deleteUserButton = tkinter.Button(userWin, text="Delete", bg="black", fg="white", command=lambda: deleteUser(choiceListCombo.get()))
    deleteUserButton.place(x=230, y=140)
    deleteUserButton["font"] = police

    logLabel = tkinter.Label(userWin, text="", bg="black", fg="red")
    logLabel.place(x=10, y=170)
    logLabel["font"] = police


def settingsWindow():


    settingapp = tkinter.Toplevel()
    settingapp.wm_title("Settings")
    settingapp.wm_geometry("300x200")
    settingapp.wm_minsize(300, 200)
    settingapp.wm_maxsize(300, 200)
    if sys.platform == "win32":
        settingapp.wm_iconbitmap("src/img/agricultureICO.ico")
    settingapp.config(bg="black")
    police = font.Font(family='Courier', size=10)


    settingsfiles = open("config/settings.yaml", "r")
    settingsData = yaml.safe_load(settingsfiles)
    settingsfiles.close()

    rpcVar = tkinter.IntVar()

    if settingsData["rpc"] == 1:

        rpcChoice = tkinter.Checkbutton(settingapp, bg="black", fg="black", variable=rpcVar)
        rpcChoice.place(x=10, y=10)
        rpcChoice.select()

    else:

        rpcChoice = tkinter.Checkbutton(settingapp, bg="black", fg="black", variable=rpcVar)
        rpcChoice.place(x=10, y=10)


    rpcText = tkinter.Label(settingapp, text="Discord RPC", bg="black", fg="white")
    rpcText.place(x=30, y=12)
    rpcText["font"] = police

    bgLabel = tkinter.Label(settingapp, text="Background file name :", bg="black", fg="white")
    bgLabel.place(x=10, y=40)
    bgLabel["font"] = police

    bgNameEntry = tkinter.Entry(settingapp, bg="black", fg="white")
    bgNameEntry.place(x=12, y=70)
    bgNameEntry["font"] = police

    bgNameEntry.insert(0, settingsData["bgFileName"])


    saveButton = tkinter.Button(settingapp, text="Save settings", bg="black", fg="white", command= lambda: saveSettings(rpcVar, settingsData, bgNameEntry))
    saveButton.place(x=15, y=165)
    saveButton["font"] = police

def minimize():

    app.withdraw()
    image=Image.open("src/img/agricultureICO.ico")
    menu=(item('Show', lambda: maximize(icon)), item('Quit', lambda: quitFromTray(icon)))
    icon=pystray.Icon("name", image, "agriF4rm", menu)
    icon.run()

def maximize(icon):

    icon.stop()
    app.after(0,app.deiconify())

def quitFromTray(icon):

    icon.stop()
    on_closing()


app = tkinter.Tk()
app.geometry("1100x700")
app.title("agriF4rm")
app.maxsize(1100, 700)
app.minsize(1100, 625)
if sys.platform == "win32":
    app.iconbitmap("src/img/agricultureICO.ico")
police = font.Font(family='Courier', size=11)
titleFont = font.Font(family='Courier', size=13, weight="bold")

settingsfiles = open("config/settings.yaml", "r")
settingsData = yaml.safe_load(settingsfiles)
settingsfiles.close()

bgFileName = settingsData["bgFileName"]
img = tkinter.PhotoImage(file="src/img/" + bgFileName)
bg = tkinter.Label(app,image=img)
bg.place(x=-2, y=-1)


playTime = settingsData["totalPlayTime"]
playTime = round(round(int(playTime), 0)/3600, 2)

playTimeLabel = tkinter.Label(app, text="Time played : " + str(playTime) + "h", bg="black", fg="white")
playTimeLabel.place(x=5, y=215)
playTimeLabel["font"] = police

settingsImg = tkinter.PhotoImage(file="src/img/settings.png", width=52, height=52)

settingsButton = tkinter.Button(app, fg="black", bg="black", image=settingsImg, command=settingsWindow, borderwidth=0, cursor="target")
settingsButton.place(x=1045, y=10)


userImg = tkinter.PhotoImage(file="src/img/user.png", width=52, height=52)

userButton = tkinter.Button(app, fg="black", bg="black", image=userImg, command=changeUserWindow, borderwidth=0, cursor="target")
userButton.place(x=990, y=10)


miniImg = tkinter.PhotoImage(file="src/img/mini.png", width=52, height=52)

miniButton = tkinter.Button(app, fg="black", bg="black", image=miniImg, command=minimize, borderwidth=0, cursor="target")
miniButton.place(x=1041, y=57)


statsLabel = tkinter.Label(app, text="Field's data :", bg="black", fg="red")
statsLabel.place(x=230, y=10)
statsLabel["font"] = font.Font(family='Courier', size=11, weight="bold")

dimLabel = tkinter.Label(app, text="Dimension : ", bg="black", fg="white")
dimLabel.place(x=230, y=30)
dimLabel["font"] = police

rentLabel = tkinter.Label(app, text="Profitability (w):", bg="black", fg="white")
rentLabel.place(x=230, y=50)
rentLabel["font"] = police

rentDollarLabel = tkinter.Label(app, text="Profitability ($) :", bg="black", fg="white")
rentDollarLabel.place(x=230, y=70)
rentDollarLabel["font"] = police

wheatLabel = tkinter.Label(app, text="Wheat amount :", bg="black", fg="white")
wheatLabel.place(x=230, y=90)
wheatLabel["font"] = police

moneyLabel = tkinter.Label(app, text="Money balance :", bg="black", fg="white")
moneyLabel.place(x=230, y=110)
moneyLabel["font"] = police

agriLabel = tkinter.Label(app, text="Agricultors :", bg="black", fg="red")
agriLabel.place(x=230, y=130)
agriLabel["font"] = police 

basicAgri = tkinter.Label(app, text="Basic agricultors :", bg="black", fg="white")
basicAgri.place(x=230, y=150)
basicAgri["font"] = police

rareAgri = tkinter.Label(app, text="Rare agricultors :", bg="black", fg="white")
rareAgri.place(x=230, y=170)
rareAgri["font"] = police

epicAgri = tkinter.Label(app, text="Epic agricultors :", bg="black", fg="white")
epicAgri.place(x=230, y=190)
epicAgri["font"] = police

legenAgri = tkinter.Label(app, text="Legendary agricultors :", bg="black", fg="white")
legenAgri.place(x=230, y=210)
legenAgri["font"] = police

sellingPrice = tkinter.Label(app, text="Wheat price :", bg="black", fg="red")
sellingPrice.place(x=550, y=10)
sellingPrice["font"] = font.Font(family='Courier', size=11, weight="bold")

sellingValue = tkinter.Label(app, text="", bg="black", fg="green")
sellingValue.place(x=676, y=10)
sellingValue["font"] = font.Font(family='Courier', size=11, weight="bold")


dropRateTitle = tkinter.Label(app, text="Drop rate :", bg="black", fg="red")
dropRateTitle.place(x=760, y=10)
dropRateTitle["font"] = font.Font(family='Courier', size=11, weight="bold")

basicAgriRate = tkinter.Label(app, text="Basic agricultors : 65%", bg="black", fg="white")
basicAgriRate.place(x=760, y=30)
basicAgriRate["font"] = police

rareAgriRate = tkinter.Label(app, text="Rare agricultors : 20%", bg="black", fg="white")
rareAgriRate.place(x=760, y=50)
rareAgriRate["font"] = police

epicAgriRate = tkinter.Label(app, text="Epic agricultors : 10%", bg="black", fg="white")
epicAgriRate.place(x=760, y=70)
epicAgriRate["font"] = police

legenAgriRate = tkinter.Label(app, text="Legendary agricultors : 5%", bg="black", fg="white")
legenAgriRate.place(x=760, y=90)
legenAgriRate["font"] = police

prodTitle = tkinter.Label(app, text="Production :", bg="black", fg="red")
prodTitle.place(x=760, y=112)
prodTitle["font"] = font.Font(family='Courier', size=11, weight="bold")

basicAgriProd = tkinter.Label(app, text="Basic agricultors : 1 w/h", bg="black", fg="white")
basicAgriProd.place(x=760, y=130)
basicAgriProd["font"] = police

rareAgriProd = tkinter.Label(app, text="Rare agricultors : 1.5 w/h", bg="black", fg="white")
rareAgriProd.place(x=760, y=150)
rareAgriProd["font"] = police

epicAgriProd = tkinter.Label(app, text="Epic agricultors : 2.5 w/h", bg="black", fg="white")
epicAgriProd.place(x=760, y=170)
epicAgriProd["font"] = police

legenAgriProd = tkinter.Label(app, text="Legendary agricultors : 4 w/h", bg="black", fg="white")
legenAgriProd.place(x=760, y=190)
legenAgriProd["font"] = police


rollTitleLabel = tkinter.Label(app, text="Roll Agricultors", bg="black", fg="red")
rollTitleLabel.place(x=120, y=300)
rollTitleLabel["font"] = titleFont

rollExpLabel = tkinter.Label(app, text="Number of agricultors :\n[500$/roll]", bg="black", fg="white")
rollExpLabel.place(x=100, y=350)
rollExpLabel["font"] = police

rollAmountEntry = tkinter.Entry(app, bg="white", fg="black")
rollAmountEntry.place(x=110, y=420)
rollAmountEntry["font"] = police

maxRollsButton = tkinter.Button(app, text="Max rolls", bg="black", fg="white", command=insertMaxRolls)
maxRollsButton.place(x=110, y=470)
maxRollsButton["font"] = police

RollsButton = tkinter.Button(app, text="Roll", bg="black", fg="white", command=lambda: multiroll(rollAmountEntry.get()))
RollsButton.place(x=245, y=470)
RollsButton["font"] = police

resultsRollLabel = tkinter.Label(app, text="", bg="black", fg="white")
resultsRollLabel.place(x=125, y=520)
resultsRollLabel["font"] = police


upgradeTitleLabel = tkinter.Label(app, text="Upgrade dimension", bg="black", fg="red")
upgradeTitleLabel.place(x=465, y=300)
upgradeTitleLabel["font"] = titleFont

nextDimLabel = tkinter.Label(app, text="Next upgrade :", bg="black", fg="white")
nextDimLabel.place(x=475, y=345)
nextDimLabel["font"] = police

upgradeButton = tkinter.Button(app, text="Upgrade", bg="black", fg="white", command=upgrade)
upgradeButton.place(x=510, y=420)
upgradeButton["font"] = police

upgradeLog = tkinter.Label(app, text="", bg="black", fg="white")
upgradeLog.place(x=480, y=470)
upgradeLog["font"] = police

sellTitleLabel = tkinter.Label(app, text="Sell wheat", bg="black", fg="red")
sellTitleLabel.place(x=800, y=300)
sellTitleLabel["font"] = titleFont

sellButton = tkinter.Button(app, text="Sell", bg="black", fg="white", command=sell)
sellButton.place(x=830, y=360)
sellButton["font"] = police

sellLog = tkinter.Label(app, text="", bg="black", fg="white")
sellLog.place(x=790, y=420)
sellLog["font"] = police



my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(60, 1, renta_loop, (my_scheduler,))
schedThread = threading.Thread(target=my_scheduler.run)
schedThread.daemon = True
schedThread.start()

updateLabels(False)

app.protocol("WM_DELETE_WINDOW", on_closing)

settingsRead = open("config/settings.yaml", "r")
settingsData = yaml.safe_load(settingsRead)
settingsRead.close()
CheckRpcSet()

app.mainloop()
