import itertools as it
from os import name,system
    
def menu(menuList):
    "Display a indexed Menu of all the elments in iterable menuList"
    counter = it.count(1)
    for i in menuList:
        print(str(next(counter)) + ". " + i )
def checkInt(n = float("inf")):
    "Checks whether a input given by a user is numerical and less than n. Makes user input again if constraints are not met."
    print("Enter a choice:")
    while True:
        temp = input()
        if temp.isnumeric():
            temp = int(temp)
            if temp <= n and temp > 0:
                clear()
                return temp
            else:
                print("Oops! Wrong input. Try again.")
        else:
            print("Oops! Wrong input. Try again.")
def checkMemberId(idList):
    "Checks wheather a input given by user is present in idList or not. Makes user input again if constraints are not met."
    print("Select Particular Member by it MemberId.(eg.MemberId_1 or just \"1\") or Enter \"-1\" to go back")
    while True:
        temp = input()
        if temp == "-1":
            return False
        if temp.isnumeric():
            temp = "Member_" + temp
        if temp in idList:
            clear()
            return temp
        else:
            print("Oops! Wrong input. Try again.")
def checkBId(idList):
    "Checks wheather a input given by user is present in idList or not. Makes user input again if constraints are not met."
    print("Select Particular book by it BId.(eg.BId_4 or just \"4\") or Enter \"-1\" to go back")
    while True:
        temp = input()
        if temp.isnumeric() and temp != "-1":
            temp = "BId_" + temp
        if temp in idList:
            return temp
        elif temp == "-1":
            clear()
            return False
        else:
            print("Oops! Wrong input. Try again.")
def loginMenu():
    "Displays a login menu and records username and password entered by an user. Returns username and password in tuple format"
    print("Enter account details \nUsername:")
    username = input()
    print("Password:")
    password = input()
    return (username,password)
def loginValidation(directory,username,password):
    "Checks weather particular user is present in directory with username = username and password = password."
    for i in directory:
        if i.userName == username and i.password == password:
            return i
    return False
def clear(): 
    "clears the console/terminal."
    if name == 'nt': 
        _ = system('cls')  
    else: 
        _ = system('clear')


#tests

#1
# menuList = ("Menu Item 1","Menu Item 2","Menu Item 3","Menu Item 4")
# menu(menuList)

#2
# checkInt(10) #discard every choice more than 10 or less than 1

#3
# idList = ("Member_1","Member_2","Member_3")
# checkMemberId(idList)                  #discard every choice which is not in idList

#4
# idList = ("BId_1","BId_4","BId_78","BId_82")
# checkBId(idList)                       #discard every choice which is not in idList

#5
# username,password = loginMenu() 
# print(username,password)              #return username and password entered

#6
# clear() #clears the console