import csv
from Book import Book
import csv
from tabulate import tabulate
import itertools as it
import random
import pytest
class library:
    "Library class. Holds a catalog(list) of book objects"
    def __init__(self):
        "Constructor. Loads book details from a csv file, creates it's book objects and appends them to the Catalog."
        self.catalog = []
        self.IDobj =it.count(1) 
        self.authorSet = set() #containes all the names of authors
        self.publisherSet = set() #containes all the names of publishers
        stock = [1, 2, 1, 6, 10, 3, 4, 10, 6, 0, 3, 3, 6, 1, 3, 7, 0, 0, 10, 0, 0, 7, 0, 5, 5, 4, 10, 3, 2, 6, 2, 1, 4, 1, 7, 3, 2, 9, 0, 8, 10, 3, 5, 1, 10, 8, 4, 10, 6, 1, 2, 5, 9, 3, 1, 9, 4, 6, 6, 5, 0, 0, 10, 7, 8, 9, 2, 7, 10, 1, 2, 4, 7, 7, 4, 10, 9, 5, 0, 7, 5, 9, 1, 0, 5, 10, 8, 9, 2, 9, 1, 9, 9, 0, 10, 1, 4, 7, 6, 5]
        iter_stock = iter(stock)
        with open("data.txt","r",encoding="UTF-8") as csvfile:
            csvreader = csv.reader(csvfile)
            row = []
            next(csvreader)
            i = 0
            while True:
                temp = next(csvreader)
                if "," not in temp[2] and len(temp[1]) < 40 and len(temp[1]) > 0:
                    row.append(temp)
                    i += 1
                if i == 100:
                    break
            for i in row:
                bookobj = Book("BId_" + str(next(self.IDobj)),i[1],i[2],i[0],i[12],i[3],i[5],next(iter_stock))
                self.authorSet.add(i[2])
                self.publisherSet.add(i[12])
                self.catalog.append(bookobj)
    def printAll(self):
        "Print all books in the catalog in tabulated manner."
        print(tabulate(self.catalog,headers=("Book Id","Book Name","Author","Publishing Year","Publisher","Language code","Average Rating","Stock")))
    def searchAll(self):
        "returns the Catalog"
        return self.catalog
    def searchByName(self,name):
        "returns a list with Book objects where bookObj.name is \'name\'"
        listBooks = [] 
        for i in self.catalog:
            if i.name == name:
               listBooks.append(i) 
        return listBooks
    def searchByYear(self,year):
        "returns a list with Book objects where bookObj.year is \'year\'"
        listBooks = []
        for i in self.catalog:
            if i.year == year:
                listBooks.append(i)
        return listBooks
    def searchByAuthor(self,author):
        "returns a list with Book objects where bookObj.author is \'author\'"
        listBooks = [] 
        for i in self.catalog:
            if i.author == author:
               listBooks.append(i) 
        return listBooks
    def searchByPublisher(self,publisher):
        "returns a list with Book objects where bookObj.publisher is \'publisher\'"
        listBooks = [] 
        for i in self.catalog:
            if i.publisher == publisher:
               listBooks.append(i) 
        return listBooks
    def issueBook(self,BId):
        "For Book Object in the catlog where bookObj.id == BId, reduce the stock by 1 and return a bookObj"
        for i in self.catalog:
            if i.id == BId:
                i.stock -= 1
                return i
    def returnBook(self,BId):
        "For Book Object in the catlog where bookObj.id == BId, increase the stock by 1"
        for i in self.catalog:
            if i.id == BId:
                i.stock += 1
    def addBook(self,name,author,year,publisher,language,rating,stock):
        "Creates a Book object and adds it to the Catalog"
        temp = Book("BId_" + str(next(self.IDobj)),name,author,year,publisher,language,rating,stock)
        self.catalog.append(temp)
    def displayBook(self,BId):
        "Display the details of Book Object in the catalog where bookObj.id == BId"
        book = [i for i in self.catalog if i.id == BId]
        book = book[0]
        print(tabulate([[book.id,book.name,book.author,book.year,book.publisher,book.language,book.rating]],headers=("Book Id","Book Name","Author","Publishing Year","Publisher","Language code","Average Rating")))
    def updateStock(self,BId,stock):
        "Change a stock of a Book Object in the Catalog where bookObj.id == BId"
        for book in self.catalog:
            if book.id == BId:
                book.stock = stock
                break
    def removeBook(self,BId):
        "Remove a Boot Object from the catalog where bookObj.id ==  BId"
        for book in self.catalog:
            if book.id == BId:
                self.catalog.remove(book)
class TestClass:
    #to test type 'py.test -m library library.py -v' into the terminal
    @pytest.fixture
    def Library(self):
        return library()
    @pytest.mark.library
    def test_library_init(self,Library):
        assert len(Library.catalog) == 100
        assert type(Library.catalog[random.randint(0,99)]) == Book
        assert next(Library.IDobj) == 101
        assert "Stephen King" in Library.authorSet
        assert "Amazon Digital Services,  Inc." in Library.publisherSet
    @pytest.mark.library
    def test_library_searchAll(self,Library):
        assert Library.searchAll() == Library.catalog
    @pytest.mark.library
    def test_library_searchByName(self,Library):
        searchResult = Library.searchByName("Needful Things")[0]
        assert type(searchResult) == Book
        assert searchResult.name == "Needful Things"
    @pytest.mark.library
    def test_library_searchByAuthor(self,Library):
        searchResult = Library.searchByAuthor("Stephen King")
        ranint = random.randint(0,len(searchResult) - 1)
        assert type(searchResult[ranint]) == Book
        assert searchResult[ranint].author == "Stephen King"
    @pytest.mark.library
    def test_library_searchByPublisher(self,Library):
        searchResult = Library.searchByPublisher("Random House LLC")
        ranint = random.randint(0,len(searchResult) - 1)
        assert type(searchResult[ranint]) == Book
        assert searchResult[ranint].publisher == "Random House LLC"
    @pytest.mark.library
    def test_library_searchByYear(self,Library):
        searchResult = Library.searchByYear("2002")
        ranint = random.randint(0,len(searchResult) - 1)
        assert type(searchResult[ranint]) == Book
        assert searchResult[ranint].year == "2002"
    @pytest.mark.library
    def test_library_issueBook(self,Library):
        while True:
            randomBook = Library.catalog[random.randint(0,99)]
            orignalStock = randomBook.stock
            if orignalStock > 0:
                Library.issueBook(randomBook.id)
                afterStock = randomBook.stock
                assert orignalStock - 1 == afterStock
                break
    @pytest.mark.library
    def test_library_returnBook(self,Library):
        while True:
            randomBook = Library.catalog[random.randint(0,99)]
            orignalStock = randomBook.stock
            print("Hello")
            if orignalStock > 0:
                Library.returnBook(randomBook.id)
                afterStock = randomBook.stock
                assert orignalStock + 1 == afterStock
                break
    @pytest.mark.library
    def test_library_addBook(self,Library):
        orignalSize = len(Library.catalog)
        Library.addBook("Poor Economics","Esther Duflo","2011","Vintage","eng-US","4.24",10)
        afterSize = len(Library.catalog)
        assert orignalSize + 1 == afterSize
        assert Library.catalog[afterSize - 1].author == "Esther Duflo"
    @pytest.mark.library
    def test_library_removeBook(self,Library):
        orignalSize = len(Library.catalog)
        Library.removeBook("BId_" + str(random.randint(1,100)))
        afterSize = len(Library.catalog)
        assert orignalSize - 1 == afterSize
    @pytest.mark.library
    def test_library_updateStock(self,Library):
        randomBook = Library.catalog[random.randint(0,99)]
        randomStock = random.randint(1,10)
        Library.updateStock(randomBook.id,randomStock)
        assert randomBook.stock == randomStock
    
# Library = library() #should be ran before testing 1 and 2

# tests

#1
# Library.printAll()

#2
# randomBId = "BId_" + str(random.randint(1,100))
# print("random book id is {0}".format(randomBId))
# Library.displayBook(randomBId)