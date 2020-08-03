from datetime import date
import pytest
class Book:
    "Blueprint of each book object stored in a library"
    def __init__(self,id,name,author,year,publisher,language,rating,stock):
        "Constructor"
        self.id = id
        self.name = name
        self.author = author
        self.year = year
        self.publisher = publisher
        self.language = language
        self.rating = rating
        self.stock = stock
          
    def __iter__(self):
        "Iter function. To make user defined class \"Book\" iterable."
        return iterBook(self)
class userBook(Book):
    "Inherited class of Book. It has extra parameter as duedate and it's stock is always set to \"1\""
    def __init__(self,id,name,author,year,publisher,language,rating,duedate):
        "Constructor"
        super().__init__(id,name,author,year,publisher,language,rating,1)
        self.duedate = duedate
    def __iter__(self): 
        "Iter function. To make user defined class \"userBook\" iterable."        
        return iterUserBook(self)
class iterBook:
    "Iterable class of Book"
    def __init__(self,book):
        "Constructer"
        self.book = book
        self.index = 0
    def __next__(self):
        "Next function. Returns id, name, author, year, publisher, language, rating & stock in a similar order."
        tup = (self.book.id,self.book.name,self.book.author,self.book.year,self.book.publisher,self.book.language,self.book.rating,self.book.stock)
        if self.index < 8:
            self.index += 1
            return tup[self.index - 1]
        else:
            raise StopIteration
class iterUserBook:
    "Iterable class of userBook"
    def __init__(self,userbook):
        "Constructor"
        self.book = userbook
        self.index = 0
    def __next__(self):
        "Next function. Returns id, name, author, year, publisher, language, rating & due-date in a similar order."
        tup = (self.book.id,self.book.name,self.book.author,self.book.year,self.book.publisher,self.book.language,self.book.rating,self.book.duedate)
        if self.index < 8:
            self.index += 1
            return tup[self.index - 1]
        else:
            raise StopIteration

class TestClass:
    #to test type 'py.test -m Book Book.py -v' into the terminal
    @pytest.mark.Book
    def test_Book_init(self):
        book =  Book("BId_16","Needful Things","Stephen King","1991","Amazon Digital Services,  Inc.","","3.87",7)
        assert book.id == "BId_16"
        assert book.name == "Needful Things"
        assert book.author == "Stephen King"
        assert book.year == "1991"
        assert book.publisher == "Amazon Digital Services,  Inc."
        assert book.language == ""
        assert book.rating == "3.87"
        assert book.stock == 7
    @pytest.mark.userBook
    def test_userBook_init(self):
        userbook =  userBook("BId_16","Needful Things","Stephen King","1991","Amazon Digital Services,  Inc.","","3.87",date.today())
        assert userbook.id == "BId_16"
        assert userbook.name == "Needful Things"
        assert userbook.author == "Stephen King"
        assert userbook.year == "1991"
        assert userbook.publisher == "Amazon Digital Services,  Inc."
        assert userbook.language == ""
        assert userbook.rating == "3.87"
        assert userbook.stock == 1
        assert userbook.duedate ==  date.today()
