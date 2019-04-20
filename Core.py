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
