class Book:
  acc = int()
  name = int()
  auth = int()
  edition = int()
  yop = int()
  pub = str()
  subj = str()
  lvl = int()
  age_res = int() #minimum age to read the given book
  genre = str()
  qty = int() #No. of books currently availible
  max = int() #No. of books bought or donated
  price = int()
  don = True
  def __init__(self, nm, ac, au,ed, qt, *, donated=True, price=0):
    self.price = price
    self.name = nm
    self.acc = ac
    self.auth = au
    self.edition = ed
    self.qty, self.max = qt, qt
    self.don = donated
  def getName(self):
    return(self.name)
  def getNumIssues(self):
    return(self.max - qty)
  #All the getters and setters
class Account:
  uname = str()
  pswd = str()
  priv = int()
  doj = int()
  #getters and setters
  def __init__(self, nm, ps, privilage):
    self.uname, self.ps, self.priv = nm, ps, privilage
  
  class BorrowerAccount(Account):
    priv = 0
    mail_id = str()
    dues = dict() #key : int(Book.acc), value : int(YYYYMMDD)
    fine = 0
    dor = dict() #key : int(Book.acc), value : int(YYYYMMDD)
    
