import os.*

#GUI Specific imports
import tkinter as tk
import tkinter.tix as tx
import tkMessageBox

#Gui Specific, custom dialogs
PROPERTIES_DIALOG_ATRRIBS = {}

#Some Golobal variables shared between GUI Widgets and Core
CURR_FILE_SELECTION = [] #A list of files currently selected by the user
ENTRY_DIALOG_INPUT = [] #The input given by the user in the last input dialog

class EntryDialog:
  def __init__(self, parent, msg):
    self.top = tk.Toplevel(parent)
    top = self.top
    
    tk.Label(top, text=msg).pack()
    EntryField = tk.Entry(top)
    EntryField.pack()
    tk.Button(top, text="OK", command=evn_buttonPreseed).pack()
  
  def exportInput(self)
    global ENTRY_DIALOG_INPUT
    ENTRY_DIALOG_INPUT.append(self.EntryField.get())
    
  def evn_buttonPressed():
    self.exportInput()
    self.top.destroy()
    
class PropertiesDialog:
  def __init__(self, parent, attributes, editmode, tup_ControlsReq, tup_commands):
    self.root = parent
    self.top = tk.Toplevel(parent)
    top = self.top
    top.pack()
    
    if not editmode:
      j = 0
      for i in attributes:
        j += 1
        tk.Label(top, text=i, anchor=tk.W).grid(row=j, column=0, sticky=tk.W)
        tk.Label(top, text=" : ").grid(row=j, column=1)
        tk.Label(top, text=attributes[i]).grid(row=j, column=2)
      btn_OK = tk.Button(top, text="OK", command=evn_BTNPressed_OK)
      btn_OK.grid(row=(j + 1), column=1)
    else:
      #The properties need to be edited
      '''How this Works:
          The user passes the names of all the widgets that must be added to the Properties fields.
          Each widget is placed right next to the attribute it points to. Further, the widgets that utilize
          the 'command' parameter can be given custom funtions to be passed to the command attribute.
          All these functions are stored as objects in the 'commands'
          tuple, passed to the initializer.
      '''
      self.dict_Entries = {} #An empty dictionary containing <attribute_name>:<Entry_widget>
      self.dict_CheckBoxes = {} #an empty dictionary like the one above
      self.checkboxes = [] #state of all the checkboxes.
      j = 0
      for i in attributes:
        j += 1
        tk.Label(top, text=i, anchor=tk.W).grid(row=j, column=0, sticky=tk.W)
        tk.Label(top, text=" : ").grid(row=j, column=1)
        #Process which command is to be added
        if(tup_ControlsReq[j] == "Label"):
          tk.Label(top, text=attributes[i]).grid(row=j, column=2)
        elif (tup_ControlsReq[j] == "Entry"):
          self.dict_Entries.update({i:tk.Entry(top, text=attributes[i])})
          self.dict_Entries[i].grid(row=j, column=2)
        elif (tup_ControlsReq[j] == "Checkbox"):
          #Code for adding a checkbox                             (TO DO)
          self.dict_CheckBoxes.update({i:tk.Checkbutton(top, text=attributes[j], onvalue=True, offvalue=False, variable=checkboxes[j])})
          self.dict_CheckBoxes[i].grid(row=j, column=2)
      btn_OK = tk.Button(top, text="OK", command=evn_BTNPressed_OK)
      btn_OK.grid(row=(j + 1), column=0)
      btn_APPLY = tk.Button(top, text="Apply", command=evn_BTNPressed_APPLY)
      btn_APPLY.grid(row=(j + 1), column=1)
      btn_Cancel = tk.Button(top, text="Cancel", command=top.destroy)
      btn_Cancel.grid(row=(j + 1), column=2)
    #Copy the attributes to the global variable:
    for i in attributes:
      PROPERTIES_DIALOG_ATTRIB.update({i:atrributes[i]})
    
  def evn_BTNPressed_OK(self):
    self.top.destroy()
  
  def evn_BTNPressed_APPLY(self):
    global PROPERTIES_DIALOG_ATTRIB
    for i in self.dict_Entries:
      PROPERTIES_DIALOG_ATTRIB.update({i:self.dict_Entries[i].get()})
    j = 0
    for i in self.dict_CheckBoxes:
      PROPERTIES_DIALOG_ATTRIB.update({i:self.checkboxes[j]})
      j += 1
    #destroy:
    self.top.destroy()

def initToolbar(parent):
  global toolbar, commands
  options = ("New Folder", "Delete", "Cut", "Copy",\
             "Paste", "Rename", "Properties",\
             "Settings", "Zip/Extraxt", "Encrypt",\
             "Protect Access", "Run", "Run with arguments",\
             "Add to Bookmarks", "Add to Favourites",\
             "Open Terminal here", "Help", "Music Player",\
             "Downloads", "Menu")
    commands = (doNewFolder, doDelete, doCut, doCopy,\
                doPaste, doRename, doProperties, doSettings,\
                doCompress, doEncrypt, doAccessProtect,\
                doRun, doRunWithArgs, doBookmarks,\
                doFavourites, doTerminal, doHelp,\
                doMP3, doDownload, doMenu)
    assert len(options) == len(commands), "900 : Options and commands do not match!"
    frm = tk.Frame(parent)
    toolbar = tk.Frame(frm)
    try:
      alp = open("icons.dat", "r")
    except (Exception):
      print(Exception)
    for i in range(0, len(options)):
      #Initialize the toolbar
      try:
        a = alp.readline()
        dicta = eval(a)
        if(dicta.keys()[0] != options[i]):
          return(-1)
        image = tk.PhotoImage(file=dicta[(dicta.keys()[0])])
        buttn = tk.Button(toolbar, image=image, command=commands[i])
        buttn.grid(row=0, column=i)
      except tk.TclError as tclerr:
        print(tclerr)
    toolbar.grid(row=0, column=0, sticky=tk.NW)
    
#Some global dynamic constants: (CORE)
SYSTEM_TYPE = (os.uname())[0]
ALMANAC_LOCATION = ".alm"

#====GUI END=========Do-ers=========IMPLEMENTATION===========

def doCopy():
  global currClip, CURR_FILE_SELECTION
  for i in CURR_FILE_SELECTION:
    currClip.append(os.path.join(os.getcwd(), i))
  
def doPaste():
  global currClip
  cwd = os.getcwd()
  errors = False
  errornous = []
  try:
    for i in currClip:
      #error checking:
      if not os.access(i, os.R_OK):
        errors = True
        errornous.append("No permission to read the file: " + i)
      if not os.access(cwd, os.W_OK):
        errors = True
        errornous.append("No permission to write to the folder: " + cwd)
      #see if the selected file is a directory or not.
      if os.path.isdir(i):
        #start copying
        shutil.copytree(i, cwd) #!Check the syntax
        if (CUT_ENABLED):
          shutil.rmtree(i)
      else:
        if not CUT_ENABLED:
          shutil.copy(i, cwd)
        if (CUT_ENABLED):
          shutil.move(i, cwd)
  except Error as err:
    print(err)
  CUT_ENABLED = False
  if errors:
    errorstr = "Errors occured during the pasting of:"
    for i in errornous:
      errorstr += ("\n\t" + i)
    errorstr += "All other files were copied successfully."
    tkMessageBox.showerror("Errors Occured during Paste", errorstr)
  else:
    tkMessageBox.showinfo("Successfully Pasted", "All Operations completed successfully.")

def doCut():
  doCopy()
  CUT_ENABLED = True

def doDelete():
  global CURR_FILE_SELECTION
  cwd = os.getcwd()
  try:
    for i in CURR_FILE_SELECTION:
      j = os.path.join(cwd, i)
      if os.path.isfile(j):
        os.remove(j)
      else:
        shutil.rmtree(j)
  except Exception as expt:
    print(expt)

#Encryption Module:

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
  psswd = ENTRY_DIALOG_INPUT[0]
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
