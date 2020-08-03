from tabulate import tabulate
from library import library
from Book import userBook
from datetime import date,timedelta
from log import log
import pytest

class User:
    "Class User"
    Library = library() #Class Variable.Instance of a class library.
    Log = [] #Class Variable. Contains all the logs of all users.
    issuedBId = [] #Class Variable. Contains BId(s) of all the books still in circulation
    def __init__(self,name,age,address,phone_number,aadhar_id,username,password):
        "Constructor"
        self.name = name
        self.age = age
        self.address = address
        self.phoneNumber = phone_number
        self.aadharId = aadhar_id
        self.userName = username
        self.password = password
    @classmethod
    def returnAuthors(cls):
        "Return a set of all the authors."
        return cls.Library.authorSet
    @classmethod
    def returnPublishers(cls):
        "Returns a set of all the publishers."
        return cls.Library.publisherSet
    @classmethod
    def search(cls,by = "all",value = ""):
        "Searches and tabulates books in a library by various parameters and return a dictionary with BId(s) as keys and their respective stock as values.\nVarious parameters for searching are:\nauthor\nname\npublisher\nyear\nall "
        temp = []
        if by == "all":
            temp = cls.Library.searchAll()
            if temp:    
                print(tabulate(temp,headers = ("Book Id","Book Name","Author","Publishing Year","Publisher","Language code","Average Rating","Stock")))
        elif by == "name":
            temp = cls.Library.searchByName(value)
            if temp:    
                print(tabulate(temp,headers = ("Book Id","Book Name","Author","Publishing Year","Publisher","Language code","Average Rating","Stock")))
        elif by == "publisher":
            temp = cls.Library.searchByPublisher(value)
            if temp:    
                print(tabulate(temp,headers = ("Book Id","Book Name","Author","Publishing Year","Publisher","Language code","Average Rating","Stock")))
        elif by == "year":
            temp = cls.Library.searchByYear(value)
            if temp:
                print(tabulate(temp,headers = ("Book Id","Book Name","Author","Publishing Year","Publisher","Language code","Average Rating","Stock")))
        elif by == "author":
            temp = cls.Library.searchByAuthor(value)
            if temp:    
                print(tabulate(temp,headers = ("Book Id","Book Name","Author","Publishing Year","Publisher","Language code","Average Rating","Stock")))
        if temp:
            return {i.id : i.stock for i in temp}
        else:
            return False
    @classmethod 
    def displayLog(cls,memberId = ""):
        "Displays log in a tabulated fashion of a particular member. If memberId is not provided, displays log of all members."
        flag = False
        if memberId != "":
            temp = []
            for log in cls.Log:
                if log.memberId == memberId:
                    temp.append(log)
                    flag = True
        else:
            temp = cls.Log
            if temp:
                flag =  True
        if flag:
            print(tabulate(temp,headers=["Book Id","Book Name","Member Id","Member Name","Issued Date","Returned Date"]))
            return True
        else:
            return False
    @classmethod
    def displayBook(cls,BId):
        cls.Library.displayBook(BId)      

class Member(User):
    "Class Member, inherited from class User. Extra variables are memberId and issuedBooks(list)"
    def __init__(self,name,age,address,phone_number,aadhar_id,username,password,memberid):
        "Constructor"
        super().__init__(name,age,address,phone_number,aadhar_id,username,password)
        self.memberId= memberid
        self.issuedBooks = []
    def displayIssuedBooks(self):
        "Displays all the issued books to a Member in a tabulated fashion along with it's duedate. Returns False if no Book has been assigned"
        if self.issuedBooks:
            print(tabulate(self.issuedBooks,headers=("Book Id","Book Name","Author","Publishing Year","Publisher","Language code","Average Rating","Due date")))
            return list(map(lambda a: a.id,self.issuedBooks))  
        else:
            return False
    def issueBook(self,BId,date = date.today()):
        "Issues a Book(with bookid == BId) to a user for 14 days from a given date(by default it is today). Adds a log to a class-variable log."
        book = self.Library.issueBook(BId)
        temp = userBook(book.id,book.name,book.author,book.year,book.publisher,book.language,book.rating,date + timedelta(days = 14))  
        self.issuedBooks.append(temp)
        self.issuedBId.append(BId)
        tempLog = log(book.id,book.name,self.memberId,self.name,date)  
        self.Log.append(tempLog)
    def returnBook(self,BId,date = date.today()):
        "Returns a book(with bookid == BId) to the Library and adds a log to a class-variable log."
        for book in self.issuedBooks:
            if book.id == BId:
                self.issuedBooks.remove(book)
                for log in self.Log:
                    if log.memberId == self.memberId and log.BId == BId:
                        log.returnLog(date)
        self.Library.returnBook(BId)
        self.issuedBId.remove(BId)
    def __iter__(self):
        "Iter Function. To make user defined class \'Member\' iterable."
        return iterMember(self)
class Librarian(User):
    "Class Librarian, inherited from class User. Extra variables are librarianId."
    def __init__(self,name,age,address,phone_number,aadhar_id,username,password,librarianid):
        "Constructor"
        super().__init__(name,age,address,phone_number,aadhar_id,username,password)
        self.librarianId = librarianid
    def addBook(self,name,author,year,publisher,language,rating,stock):
        "Adds a Book to the Library"
        self.Library.addBook(name,author,year,publisher,language,rating,stock)
    def updateStock(self,BId,stock):
        "Update a Book's stock with bookid == BId"
        self.Library.updateStock(BId,stock)
    def removeBook(self,BId):
        "Removes a Book with bookid == BId. Returns False if the book is still in circulation"
        if BId in self.issuedBId:
            return False
        else:
            self.Library.removeBook(BId)
            return True
    def __iter__(self):
        "Iter Function. To make user defined class \'Librarian\' iterable."
        return iterLibrarian(self)
class iterMember:
    "Iterable class of Member"
    def __init__(self,Member):
        "Constructor"
        self.index = 0
        self.user = Member
    def __next__(self):
        "Next function. Returns name, age, address, phone number, aadhar number, memberId, username, password in a same order."
        tup = (self.user.name,str(self.user.age),self.user.address,str(self.user.phoneNumber),str(self.user.aadharId),self.user.memberId,self.user.userName,self.user.password)
        if self.index < len(tup):
            self.index += 1
            return tup[self.index - 1]
        else:
            raise StopIteration
class iterLibrarian:
    "Iterable class of Librarian"
    def __init__(self,Librarian):
        "Constructor"
        self.index = 0
        self.user = Librarian
    def __next__(self):
        "Next function. Returns name, age, address, phone number, aadhar number, librarianId, username, password in a same order."
        tup = (self.user.name,str(self.user.age),self.user.address,str(self.user.phoneNumber),str(self.user.aadharId),self.user.librarianId,self.user.userName,self.user.password)
        if self.index < len(tup):
            self.index += 1
            return tup[self.index - 1]
        else:
            raise StopIteration
class TestClass:
    #to test User class type 'py.test -m User user.py -v' into the terminal
    #to test Member class type 'py.test -m Member user.py -v' into the terminal
    #to test Library class type 'py.test -m Library user.py -v' into the terminal
    @pytest.mark.User
    def test_user_init(self):   
        user = User("Ishwarchandra Deshmukh",22,"Jalgaon", 8981212123, 123456789012, "ishudeshmukh","botbotbot")
        assert type(user.Library) ==  library
        assert user.name == "Ishwarchandra Deshmukh"
        assert user.age == 22
        assert user.address == "Jalgaon"
        assert user.phoneNumber == 8981212123
        assert user.aadharId == 123456789012
        assert user.userName == "ishudeshmukh"
        assert user.password == "botbotbot"
    @pytest.mark.User
    def test_user_returnAuthors(self):
        authorSet = User.returnAuthors() #it is a class method, so can be called directly by the class name.
        assert type(authorSet) == set
        assert "Stephen King" in authorSet
    @pytest.mark.User
    def test_user_returnPublishers(self):
        publisherSet = User.returnPublishers() #it is a class method, so can be called directly by the class name.
        assert type(publisherSet) == set
        assert "Random House LLC" in publisherSet
    @pytest.mark.User
    def test_user_search(self):
        temp = User.search(by="author",value = "Stephen King")
        assert type(temp) == dict
    @pytest.mark.Member
    def test_member_init(self):
        member = Member("Ishwarchandra Deshmukh",22,"Jalgaon", 8981212123, 123456789012, "ishudeshmukh","botbotbot","Member_1")
        assert type(member.Library) ==  library
        assert member.name == "Ishwarchandra Deshmukh"
        assert member.age == 22
        assert member.address == "Jalgaon"
        assert member.phoneNumber == 8981212123
        assert member.aadharId == 123456789012
        assert member.userName == "ishudeshmukh"
        assert member.password == "botbotbot"
        assert member.memberId == "Member_1"
    @pytest.mark.Member
    def test_member_issueBook(self):
        member = Member("Ishwarchandra Deshmukh",22,"Jalgaon", 8981212123, 123456789012, "ishudeshmukh","botbotbot","Member_1")
        member.issueBook("BId_24")
        assert member.issuedBooks[0].id == "BId_24"
    @pytest.mark.Member
    def test_member_returnBook(self):
        member = Member("Ishwarchandra Deshmukh",22,"Jalgaon", 8981212123, 123456789012, "ishudeshmukh","botbotbot","Member_1")
        member.issueBook("BId_24")
        assert len(member.issuedBooks) == 1
        member.returnBook("BId_24")
        assert len(member.issuedBooks) == 0
    @pytest.mark.Librarian
    def test_librarian_init(self):
        librarian = Librarian("Sujit Patil",35,"Jalgaon",9273648271,899264728174,"sujitP","admin12345","Librarian_1")
        assert type(librarian.Library) ==  library
        assert librarian.name == "Sujit Patil"
        assert librarian.age == 35
        assert librarian.address == "Jalgaon"
        assert librarian.phoneNumber == 9273648271
        assert librarian.aadharId == 899264728174
        assert librarian.userName == "sujitP"
        assert librarian.password == "admin12345"
        assert librarian.librarianId == "Librarian_1"
    @pytest.mark.Librarian
    def test_librarian_addBook(self):
        librarian = Librarian("Sujit Patil",35,"Jalgaon",9273648271,899264728174,"sujitP","admin12345","Librarian_1")
        librarian.addBook("Poor Economics","Esther Duflo","2011","Vintage","eng-US","4.11",6)
        assert librarian.Library.catalog.pop().name == "Poor Economics"
    @pytest.mark.Librarian
    def test_librarian_removeBook(self):
        librarian = Librarian("Sujit Patil",35,"Jalgaon",9273648271,899264728174,"sujitP","admin12345","Librarian_1")
        orignalSize = len(librarian.Library.catalog)
        librarian.removeBook("BId_24")
        afterSize = len(librarian.Library.catalog)
        assert orignalSize - 1 == afterSize
    

# tests

#User

#1
# User.displayBook("BId_2")

#Member

#1
# member = Member("Ishwarchandra Deshmukh",22,"Jalgaon", 8981212123, 123456789012, "ishudeshmukh","botbotbot","Member_1")
# member.issueBook("BId_24")
# member.issueBook("BId_32")
# member.displayIssuedBooks()
