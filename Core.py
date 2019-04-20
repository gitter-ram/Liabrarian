import os.*
#Some global dynamic constants:
SYSTEM_TYPE = (os.uname())[0]
def encryptFile(file, passwd):
  '''A basic complementary file encryption.'''
  try:
    if not (os.access((os.getcwd() + file), os.R_OK)):
      return (-1) #-1: No file reading privilage
    
    fh = open(file, "r")
    if os.access((os.getcwd() + file + ".eny"), os.F_OK):
      #Destination File already exists, remove it.
      os.remove(os.getcwd() + file + ".eny")
    
    ofh = open((file + ".eny"), "w")
    buff = 10 #10 bytes per read/write cycle
    while (a = fh.read(buff)) != "":
      for j in a:
        c = ord(j)
        c = (~c) ^ (0xAA) #Encryption routine
        c = chr(c)
        ofh.write(c)
  except (Exception):
    return(-2) #Errors during file io
  finally:
    if (ofh != None):
      ofh.close()
    if(fh != None):
      fh.close()
  return(0)

def decryptFile(file, passwd, alm)
  '''The decryption routine for encrypted files
     Care must be taken that 'file' and 'alm' must have the 
     File name in absolute path'''
  #Check alm
  if not os.access(alm, R_OK):
    return(-3) #Alm unreadable
  pass_match = False
  try:
    falm = open(alm, "r")
    while (am = (falm.readline)) != "":
      if(am.endswith("\n")):
        a = eval(am[0:-1])
      else:
        a = eval(am)
      if (file in a):
        if a[file] == passwd)
          pass_match = True
        else:
          pass_match = False
          break
    if not pass_match:
      return(-4) #Passwords do not match
    
    #check if the source file is readable
    if not os.access(file, R_OK)
      return(-1) #Source file is unreadable
    fh = open(file, "r")
    buff = 10
    
    #remove the destination fike if it exists
    if (os.access(file[0:-4], F_OK)):
      os.remove(file[0:-4])
    fho = open(file[0:-4], "w")
    
    while (a = (fh.read(buff))) != "" :
      for j in a:
        c = ord(j)
        c = ~(c ^ 0xAA)
        c = chr(c)
        fho.write(c)
  except (Exception):
    return(-2) #io error
  finally:
    if falm != None:
      falm.close()
    if fho != None:
      fho.close()
    if fh != None:
      fh.close()
  return(0) #Success
  
