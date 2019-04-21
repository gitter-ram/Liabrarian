import os.*
#GUI Specific imports
from tkinter import messagebox
import tkinter as tk
#Gui Specific, custom dialogs
ENTRY_DIALOG_INPUT = ""
class EntryDialog:
  def __init__(self, parent, msg):
    self.top = tk.Toplevel(parent)
    top = self.top
    
    tk.Label(top, text=msg).pack()
    EntryField = tk.Entry(top)
    EntryField.pack()
    tk.Button(top, text="OK", command=lambda(*ignore):evn_buttonPreseed()).pack()
  
  def exportInput(self)
    global ENTRY_DIALOG_INPUT
    ENTRY_DIALOG_INPUT = self.EntryField.get()
    
  def evn_buttonPressed():
    self.exportInput()
    self.top.destroy()
    
#Some global dynamic constants: (CORE)
SYSTEM_TYPE = (os.uname())[0]
ALMANAC_LOCATION = ".alm"
#Some Golobal variables shared between GUI Widgets and Core
CURR_FILE_SELECTION = [] #A list of files currently selected by the user

def encryptFile(file):
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

def evn_encryptButtonPressed():
  #The user has pressed the Encrypt button, start encryption.
  global CURR_FILE_SELECTION
  if (len(CURR_FILE_SELECTION) == 0)
    messagebox.showerror("Error", "No file Selected for encryption/decryption.")
  #Fetch the password for encryption or decryption:
  #Show the password input dialog:
  pass_dialog = EntryDialog(root, "Enter the Password:")
  root.wait_window(pass_dialog.top)
  #fetch the password:
  global ENTRY_DIALOG_INPUT
  global ALMANAC_LOCATION
  psswd = ENTRY_DIALOG_INPUT
  for i in CURR_FILE_SELECTION:
    if(i.endswith(".eny")):
      ret =decryptFile(os.getcwd() + CURR_FILE_SELECTION, psswd, ALMANAC_LOCATION)
      #Error Processing:
      if ret != 0
        #Delete any files generated
        if (os.access(i[0:-4], F_OK)):
          os.remove(i[0:-4])
        #Process the return code:
        if (ret == -1):
          error_str = "The File, " + i + " is unreadable. (No read privialge)"
        if (ret == -2):
          error_str = "Errors during reading or writing files while working with " + i
        if (ret == -3):
          error_str = "Files can only be decrypted on the machine at which they were encrypted."
        if (ret == -4):
          error_str = "Password for the file, " + i + " is wrong. Try Again."
        messagebox.showerror("Error", error_str)
    else: #File has to be encrypted
      #Code for ordering a file encryption follows
      #First, try to encrypt the file
      ret = encryptFile(i)
      if ret == 0: #Encryption successful, delete the source file and make an almanac entry
        try:
          if(os.access(ALMANAC_LOCATION, R_OK)):
            messagebox.showerror("Error", "Encryption failed.No read privilage to the almanac.")
            os.remove(i + ".eny")
            continue
          falm = open(ALMANAC_LOCATION, "a")
          falm.write(i + ":" + i + ".eny" + "\n")
        except (Exception)
          messagebox.showerror("Error", "Errors occured during writing the almanac. Exiting")
          os.remove(i + ".eny")
          continue
      if ret != 0: #Errors occrued
        if (ret == -1):
          error_str = "The File, " + i + " is unreadable. (No read privialge)"
        if (ret == -2):
          error_str = "Errors during reading or writing files while working with " + i
        messagebox.showerror("Error", error_str)
        os.remove(i+".eny")
     messagebox.showinfo("Done", "All operations completed successfully.")
