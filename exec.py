import ui
from user import Member,Librarian
from tabulate import tabulate
from datetime import date,timedelta


def iterMemberId(n):
    while True:
        yield "Member_" + str(n)
        n += 1
iter_id = iterMemberId(1)

memberList = []
librarianList = []

def addMember(name,age,address,phone_number,aadhar_id,username,password):
    temp = Member(name,age,address,phone_number,aadhar_id,username,password,next(iter_id))
    memberList.append(temp)
    return temp.memberId
def removeMember(memberId):
    for member in memberList:
        if member.memberId == memberId:
            memberList.remove(member)
def dummydata():
    addMember("Ishwarchandra Deshmukh",22,"Jalgaon", 8981212123, 123456789012, "ishudeshmukh","botbotbot")
    addMember("Harish Deshmukh",18,"Jalgaon",7558643221,910283746378,"harideshmukh","xmascandy")
    addMember("Rahul Jaiswal",23,"Jalgaon",8473625199,827364519283,"rahulJ","candycrush")
    memberList[0].issueBook("BId_27",date.today() - timedelta(days = 10))
    memberList[0].issueBook("BId_4",date.today() - timedelta(days = 2))
    memberList[0].returnBook("BId_27",date.today() - timedelta(days = 1))
    memberList[1].issueBook("BId_86",date(2020,7,23))
    memberList[1].issueBook("BId_37",date(2020,7,27))
    memberList[1].returnBook("BId_86",date(2020,7,26))
    temp = Librarian("Sujit Patil",35,"Jalgaon",9273648271,899264728174,"sujitP","admin12345","Librarian_1")
    librarianList.append(temp)
dummydata()    

goBackMenu = ["Go back"]
yesNoMenu = ("Yes","No")
searchMenu = ("Search by Bookname","Search by Author","Search by Publisher","Search by Publishing year","List all Books","Go Back")
startMenu = ("Member Login","Librarian Login","Quit")
dashboardMenu = ("Issued Books","Browse/Issue Books","Log","My profile","Logout")
librarianDashboardMenu = ("Log","Add/Remove Member","Catalog Operations","My Profile","Logout")
failMenu = ("Try Agin","Go to Home page")
failSearchMenu = ("Try Agin","Go to Dashboard page")
catalogUpdateMenu = ("Catalog","Add a Book","Update a Book's stock/Remove a Book","Go back")
addRemoveMemberMenu = ("Members","Add a Member","Remove a Member","Go back")
removeUpdateMenu = ("Remove this book","Update it's stock")

while True:
    ui.clear()
    ui.menu(startMenu)
    startMenuChoice = ui.checkInt(len(startMenu))
    if startMenuChoice == 1:
        memberObj = False
        while True:
            breakFlag = False
            print("++++++ Member Login ++++++")
            username, password = ui.loginMenu()
            memberObj = ui.loginValidation(memberList,username,password)
            if memberObj:
                ui.clear()
                break
            else:
                print("---------------------------------\nEnter Valid username or password!\n---------------------------------")
                ui.menu(failMenu)
                if ui.checkInt(len(failMenu)) == 2:
                    breakFlag = True
                    break
        if breakFlag == False:
            print("Welcome {0}".format(memberObj.name))
            while True:
                ui.menu(dashboardMenu)
                dashboardMenuChoice = ui.checkInt(len(dashboardMenu))
                if dashboardMenuChoice == 1:
                    idList = memberObj.displayIssuedBooks()
                    if idList:
                        BId = ui.checkBId(idList)
                        if BId:
                            ui.clear()
                            memberObj.displayBook(BId)
                            print("Do you want to Return this book?")
                            ui.menu(yesNoMenu)
                            if ui.checkInt(len(yesNoMenu)) == 1:
                                memberObj.returnBook(BId)
                                print("{0} has been returned".format(BId))
                                ui.menu(goBackMenu)
                                ui.checkInt(len(goBackMenu))
                    else:
                        print("No Issued Books")
                        ui.menu(goBackMenu)
                        backChoice = ui.checkInt(1)
                elif dashboardMenuChoice == 2:
                    while True:
                        ui.menu(searchMenu)
                        searchMenuChoice = ui.checkInt(len(searchMenu))
                        if searchMenuChoice == 1:
                            print("Enter Bookname:")
                            name = input()
                            idList = memberObj.search(by = "name",value = name)
                        elif searchMenuChoice == 2: 
                            print("Enter Author's Name(Enter \"all\" for a list of authors):")
                            author = input()
                            if author == "all" or author == "All":
                                ui.clear()
                                authorList = list(memberObj.returnAuthors())
                                ui.menu(authorList)
                                authorChoice = ui.checkInt(len(authorList))
                                author = authorList[authorChoice - 1] 
                            idList = memberObj.search(by = "author",value = author)
                        elif searchMenuChoice == 3:
                            print("Enter Publisher's Name(Enter \"all\" for a list of publishers):")
                            publisher = input()
                            if publisher == "all" or publisher == "All":
                                ui.clear()
                                publisherList = list(memberObj.returnPublishers())
                                ui.menu(publisherList)
                                publisherChoice = ui.checkInt(len(publisherList))
                                publisher = publisherList[publisherChoice - 1]
                            idList = memberObj.search(by = "publisher",value = publisher)
                        elif searchMenuChoice == 4:
                            while True:
                                print("Enter Publishing Year:")
                                year = input()
                                if year.isnumeric():
                                    break
                                else:
                                    print("Oops! Wrong input. Try again.")
                            idList = memberObj.search(by = "year",value = year)
                        elif searchMenuChoice == 5:
                            idList = memberObj.search()
                        elif searchMenuChoice == 6:
                            break
                        if idList:  
                            BId = ui.checkBId(idList)
                            ui.clear() 
                            if BId:
                                if idList[BId]: 
                                    memberObj.displayBook(BId)
                                    print("Do you want to issue this book for yourself?")
                                    ui.menu(yesNoMenu)
                                    if ui.checkInt(len(yesNoMenu)) == 1:
                                        memberObj.issueBook(BId)
                                        print("{0} has been issued to you for 14 days".format(BId))
                                        ui.menu(goBackMenu)
                                        ui.checkInt(len(goBackMenu))
                                        break
                                else:
                                    print("Sorry! This book is currently out of stock. Please try again later.")
                                    ui.menu(goBackMenu)
                                    ui.checkInt(len(goBackMenu))
                        else:
                            print("No Book found!")
                            ui.menu(failSearchMenu)
                            if ui.checkInt(len(failSearchMenu)) == 2:
                                break
                elif dashboardMenuChoice == 3:
                    if memberObj.displayLog(memberObj.memberId) == False:
                        print("No log so far!")
                    ui.menu(goBackMenu)
                    ui.checkInt(len(goBackMenu))
                elif dashboardMenuChoice == 4:
                    print(tabulate([memberObj], headers = ["Full name","Age","Address","Phone Number","Aadhar Card Number","Member Id","Username","Password"]))
                    ui.menu(goBackMenu)
                    backChoice = ui.checkInt(1)
                elif dashboardMenuChoice == 5:
                    break
    if startMenuChoice == 2:
        librarianObj = False
        while True:
            breakFlag = False
            print("++++++++ Librarian Login ++++++++")
            username, password = ui.loginMenu()
            librarianObj = ui.loginValidation(librarianList,username,password)
            if librarianObj:
                ui.clear()
                break
            else:
                print("---------------------------------\nEnter Valid username or password!\n---------------------------------")
                ui.menu(failMenu)
                if ui.checkInt(len(failMenu)) == 2:
                    breakFlag = True
                    break
        if breakFlag == False:
            print("Welcome {0}".format(librarianObj.name))
            while True:
                ui.menu(librarianDashboardMenu)
                librarianDashboardMenuChoice = ui.checkInt(len(librarianDashboardMenu))
                if librarianDashboardMenuChoice == 1:
                    if librarianObj.displayLog() == False:
                        print("No log so far!")
                    ui.menu(goBackMenu)
                    ui.checkInt(len(goBackMenu))
                elif librarianDashboardMenuChoice == 2:
                    while True:
                        ui.menu(addRemoveMemberMenu)
                        addRemoveMemberMenuChoice = ui.checkInt(len(addRemoveMemberMenu))
                        if addRemoveMemberMenuChoice == 1:
                            print(tabulate(memberList,headers=["Full name","Age","Address","Phone Number","Aadhar Card Number","Member Id","Username","Password"]))
                            ui.menu(goBackMenu)
                            goBackMenuChoice = ui.checkInt(1)
                        elif addRemoveMemberMenuChoice == 2:
                            while True:
                                print("Enter Member's Name:")
                                name = input()
                                ui.clear()
                                print("Enter Member's Age:")
                                while True:
                                    age = input()
                                    if age.isnumeric() and int(age) < 100:
                                        age = int(age)
                                        break
                                    else:
                                        print("Oops! Wrong input. Try again.")
                                ui.clear()
                                print("Enter Member's Address:")
                                address = input()
                                ui.clear()
                                print("Enter Member's Phone Number:")
                                while True:
                                    phone_number = input()
                                    if phone_number.isnumeric() and len(phone_number) == 10:
                                        phone_number = int(phone_number)
                                        break
                                    else:
                                        print("Oops! Wrong input. Try again.")
                                ui.clear()
                                print("Enter Member's Aadhar Id:")
                                while True:
                                    aadhar_id = input()
                                    if aadhar_id.isnumeric() and len(aadhar_id) == 12:
                                        aadhar_id = int(aadhar_id)
                                        break
                                    else:
                                        print("Oops! Wrong input. Try again.")
                                ui.clear()
                                while True:
                                    flag = True
                                    print("Enter Member's assigned username:")
                                    username = input()
                                    for member in memberList:
                                        if member.userName == username:
                                            flag == False
                                    if flag:
                                        ui.clear()
                                        break
                                    else:
                                        print("Username already exist. Try using another username")
                                print("Enter Member's assigned password:")
                                password =  input()
                                ui.clear()
                                print("Entered Info:\nName: {0}\nAge: {1}\nAddress: {2}\nPhone Number: {3}\nAadhar Number: {4}\n Username: {5}\n Password: {6}".format(name,age,address,phone_number,aadhar_id,username,password))
                                ui.menu(("Confirm data and enter book into the catalog","Something's wrong? Enter information again","Go back"))
                                choice =  ui.checkInt(3)
                                if choice == 1:
                                    addMember(name,age,address,phone_number,aadhar_id,username,password)
                                    print("Member added succesfully")
                                    ui.menu(goBackMenu)
                                    goBackMenuChoice = ui.checkInt(1)
                                    break
                                elif choice == 3:
                                    break
                        elif addRemoveMemberMenuChoice == 3:
                            print(tabulate(memberList,headers=["Full name","Age","Address","Phone Number","Aadhar Card Number","Member Id","Username","Password"]))
                            memberIdList = [member.memberId for member in memberList]
                            memberId = ui.checkMemberId(memberIdList)
                            if memberId:
                                for member in memberList:
                                    if member.memberId == memberId:
                                        if member.issuedBooks:
                                            print("Particular Member still has booked issued to him/her. Can't remove this member from directory!")
                                            break
                                        else:
                                            removeMember(memberId)
                                            print("Particular member has been removed from the directory!")
                                            break
                                ui.menu(goBackMenu)
                                goBackMenuChoice = ui.checkInt(1)
                        elif addRemoveMemberMenuChoice == 4:
                            break
                elif librarianDashboardMenuChoice == 3:
                    while True:
                        ui.menu(catalogUpdateMenu)
                        catalogUpdateMenuChoice = ui.checkInt(len(catalogUpdateMenu))
                        if catalogUpdateMenuChoice == 1:
                            librarianObj.search()
                            ui.menu(goBackMenu)
                            choice = ui.checkInt(1)
                        elif catalogUpdateMenuChoice == 2:
                            while True:
                                print("Input Book's Name:")
                                name = input()
                                ui.clear()
                                print("Input Book's Author:")
                                author = input()
                                ui.clear()
                                while True:
                                    print("Enter Publishing Year:")
                                    year = input()
                                    if year.isnumeric():
                                        break
                                    else:
                                        print("Oops! Wrong input. Try again.")
                                ui.clear()
                                print("Enter Publisher:")
                                publisher = input()
                                ui.clear()
                                print("Enter Book's Language code:")
                                language = input()
                                ui.clear()
                                while True:
                                    print("Enter Book's Average rating on NYT rating(format: \"D.DD\" eg. 4.25):")
                                    rating = input()
                                    if len(rating) == 4 and rating[0].isnumeric() and rating[2:4].isnumeric():
                                        if int(rating[0]) < 5:
                                            break
                                        else:
                                            print("Oops! Wrong input. Try again.")
                                    else:
                                        print("Oops! Wrong input. Try again.")
                                ui.clear()
                                while True:
                                    print("Enter the number of books:")
                                    stock = input()
                                    if stock.isnumeric() and int(stock) > 0:
                                        break
                                    else:
                                        print("Oops! Wrong input. Try again.")
                                ui.clear()
                                print("Entered Info:\nBookname: {0}\nAuthor: {1}\nPublishing year: {2}\nPublisher: {3}\nLanguage code: {4}\nAverage Rating: {5}\nNumber of books: {6}".format(name,author,year,publisher,language,rating,stock))
                                ui.menu(("Confirm data and enter book into the catalog","Something's wrong? Enter information again","Go back"))
                                choice = ui.checkInt(2)
                                if choice ==  1 or choice == 3:
                                    break
                            if choice == 1:
                                librarianObj.addBook(name,author,year,publisher,language,rating,stock)
                                print("Book succesfully added")
                                ui.menu(goBackMenu)
                                ui.checkInt(len(goBackMenu))
                        elif catalogUpdateMenuChoice == 3:
                            while True:
                                ui.menu(searchMenu)
                                searchMenuChoice = ui.checkInt(len(searchMenu))
                                if searchMenuChoice == 1:
                                    print("Enter Bookname:")
                                    name = input()
                                    idList = librarianObj.search(by = "name",value = name)
                                elif searchMenuChoice == 2: 
                                    print("Enter Author's Name(Enter \"all\" for a list of authors):")
                                    author = input()
                                    if author == "all" or author == "All":
                                        ui.clear()
                                        authorList = list(librarianObj.returnAuthors())
                                        ui.menu(authorList)
                                        authorChoice = ui.checkInt(len(authorList))
                                        author = authorList[authorChoice - 1] 
                                    idList = librarianObj.search(by = "author",value = author)
                                elif searchMenuChoice == 3:
                                    print("Enter Publisher's Name(Enter \"all\" for a list of publishers):")
                                    publisher = input()
                                    if publisher == "all" or publisher == "All":
                                        ui.clear()
                                        publisherList = list(librarianObj.returnPublishers())
                                        ui.menu(publisherList)
                                        publisherChoice = ui.checkInt(len(publisherList))
                                        publisher = publisherList[publisherChoice - 1]
                                    idList = librarianObj.search(by = "publisher",value = publisher)
                                elif searchMenuChoice == 4:
                                    while True:
                                        print("Enter Publishing Year:")
                                        year = input()
                                        if year.isnumeric():
                                            break
                                        else:
                                            print("Oops! Wrong input. Try again.")
                                    idList = librarianObj.search(by = "year",value = year)
                                elif searchMenuChoice == 5:
                                    idList = librarianObj.search()
                                elif searchMenuChoice == 6:
                                    break
                                if idList:  
                                    BId = ui.checkBId(idList)
                                    ui.clear() 
                                    if BId:
                                        ui.menu(removeUpdateMenu)
                                        removeUpdateMenuChoice = ui.checkInt(len(removeUpdateMenu)) 
                                        if removeUpdateMenuChoice == 1:
                                            if librarianObj.removeBook(BId):
                                                print("Book removed")
                                            else:
                                                print("Book cannot be removed! It is still in circulation.")
                                            ui.menu(goBackMenu)
                                            choice = ui.checkInt(1)
                                        elif removeUpdateMenuChoice == 2:
                                            print("{0}'s stock in catalog is {1}".format(BId,idList[BId]))
                                            print("Enter New stock value")
                                            stock = ui.checkInt()
                                            librarianObj.updateStock(BId,stock)
                                            ui.clear()
                                            print("Stock updated!")
                                            ui.menu(goBackMenu)
                                            choice = ui.checkInt(1)
                                else:
                                    print("No Book found!")
                                    ui.menu(failSearchMenu)
                                    if ui.checkInt(len(failSearchMenu)) == 2:
                                        break
                        elif catalogUpdateMenuChoice == 4:
                            break
                elif librarianDashboardMenuChoice == 4:
                    print(tabulate([librarianObj], headers = ["Full name","Age","Address","Phone Number","Aadhar Card Number","Librarian Id","Username","Password"]))
                    ui.menu(goBackMenu)
                    backChoice = ui.checkInt(1)
                elif librarianDashboardMenuChoice == 5:
                    break

    if startMenuChoice == 3:
        break