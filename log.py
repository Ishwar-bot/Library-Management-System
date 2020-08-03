from datetime import date,timedelta
import pytest
class log:
    "Class Log: Creates a log of issuing and returning of a book to and from particular Member"
    def __init__(self,BId,bookName,memberId,memberName,issueDate):
        "Constructor"
        self.BId = BId
        self.bookName = bookName
        self.memberId = memberId
        self.memberName = memberName
        self.issueDate = issueDate
        self.returnDate = "Not yet returned"
    def returnLog(self,returnDate):
        "Sets returnDate"
        self.returnDate = returnDate
    def __iter__(self):
        "Iter Function. To make user defined class \'log\' iterable."
        return iterLog(self)
class iterLog:
    "Iterable class of log."
    def __init__(self,log):
        "Constructor"
        self.log = log
        self.index = 0
    def __next__(self):
        "Next Function. Returns BId, bookname, memberId, memberName, issueDate & returnDate in a similar order."
        tup = (self.log.BId,self.log.bookName,self.log.memberId,self.log.memberName,self.log.issueDate,self.log.returnDate)
        if self.index < 6:
            self.index += 1
            return tup[self.index - 1]
        else:
            raise StopIteration
class TestClass:
    #to test type 'py.test -m log log.py -v' into the terminal
    @pytest.mark.log  
    def test_log_init(self):
        Log = log("BId_3","Daughter of Smoke & Bone","Member_2","Harish Deshmukh",date.today() - timedelta(days = 3))  
        assert Log.BId == "BId_3"
        assert Log.bookName == "Daughter of Smoke & Bone"
        assert Log.memberId == "Member_2"
        assert Log.memberName == "Harish Deshmukh"
        assert Log.issueDate == date.today() - timedelta(days = 3)
        assert Log.returnDate == "Not yet returned"
    @pytest.mark.log  
    def test_log_returnLog(self):
        Log = log("BId_3","Daughter of Smoke & Bone","Member_2","Harish Deshmukh",date.today() - timedelta(days = 3))
        Log.returnLog(date.today())
        assert Log.returnDate == date.today()
