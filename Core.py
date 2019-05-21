import os
import shutil

# GUI Frontend :
import tkinter.ttk as ttk
import tkinter as tk

class EntryDialog:
    def __init__(self, parent, msg):
        self.uinput = tk.StringVar()
        self.dialog = tk.Toplevel(parent)
        msgl = tk.Label(self.dialog, text=msg)
        inp = tk.Entry(self.dialog, textvar=self.uinput)
        OKButton = tk.Button(self.dialog, text="OK", command=self.OK_button_pressed)
        CancelButton = tk.Button(self.dialog, text="Cancel", command=self.Cancel_button_pressed)
        # Start packing the widgets
        msgl.pack()
        inp.pack()
        OKButton.pack()
        CancelButton.pack()
        self.finalText = None

    def OK_button_pressed(self, *event):
        self.finalText = self.uinput.get()
        self.dialog.destroy()

    def Cancel_button_pressed(self, *event):
        self.finalText = None
        self.dialog.destroy()


class FileLister:
    def __init__(self, parent, dataset):
        frame = tk.Frame(parent)
        self.dataset = dataset
        self.tree = ttk.Treeview(frame, column=dataset[0])
        for i in range(0, len(dataset[0])):
            self.tree.heading(dataset[0][i], text=dataset[1][i])
        for i in range(2, len(dataset)):
            self.tree.insert("", "end", iid=i, text=dataset[i][0], values=dataset[i][1:])
        self.tree.pack()
        frame.pack()


    def getCurrentSelection(self):
        return dataset[int(self.tree.focus())]


class MessageDialog:
    '''
        Modes :
        0 = OK Button
        1 = Yes, No
    '''
    # Some constants for better readability of the code
    DIALOG_OK = 0
    DIALOG_YESNO = 1

    def __init__(self, parent, title, msg, *, mode=0):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title = title
        msgl = tk.Label(self.dialog, text=msg)
        msgl.pack()
        self.mode = mode
        if mode == 1:
            YesButton = tk.Button(self.dialog, text="Yes", command=self.Yes_button_pressed)
            NoButton = tk.Button(self.dialog, text="No", command=self.No_button_pressed)
            YesButton.pack()
            NoButton.pack()
        else:
            OKButton = tk.Button(self.dialog, text="OK", command=self.OK_button_pressed)
            OKButton.pack()
        self.result = ""


    def Yes_button_pressed(self, *event):
        self.result = True
        self.dialog.destroy()

    def No_button_pressed(self, *event):
        self.result = False
        self.dialog.destroy()

    def OK_button_pressed(self, *event):
        self.dialog.destroy()


# Some global dynamic constants: (CORE)
SYSTEM_TYPE = "Need To Be Detected."
ALMANAC_LOCATION = ".alm"
CURR_FILE_SELECTION = []
CUT_ENABLED = False


# Ultra basic:
def encryptFile(file):
    fh, ofh = None, None
    '''A basic complementary file encryption.'''
    try:
        if not (os.access((os.getcwd() + file), os.R_OK)):
            return -1  # -1: No file reading privilage

        fh = open(file, "r")
        if os.access((os.getcwd() + file + ".eny"), os.F_OK):
            # Destination File already exists, remove it.
            os.remove(os.getcwd() + file + ".eny")

        ofh = open((file + ".eny"), "w")
        buff = 10  # 10 bytes per read/write cycle
        a = fh.read(buff)
        while a != "":
            for j in a:
                c = ord(j)
                c = (~c) ^ 0xAA  # Encryption routine
                c = chr(c)
                ofh.write(c)
            a = fh.read(buff)
    except Exception:
        return -2  # Errors during file io
    finally:
        if ofh is not None:
            ofh.close()
        if fh is not None:
            fh.close()
    return 0


def decryptFile(file, passwd, alm):
    '''The decryption routine for encrypted files
       Care must be taken that 'file' and 'alm' must have the 
       File name in absolute path
    '''
    # Check alm
    if not os.access(alm, os.R_OK):
        return -3  # Alm unreadable
    pass_match = False
    try:
        falm = open(alm, "r")
        am = falm.readline()
        while am != "":
            if am[-1:-3] == "\n" :
                a = eval(am[0:-1])
            else:
                a = eval(str(am))
            if (file in a):
                if a[file] == passwd:
                    pass_match = True
                else:
                    pass_match = False
                break
            am = (falm.readline)
        if not pass_match:
            return(-4) #Passwords do not match

        #check if the source file is readable
        if not os.access(file, os.R_OK):
            return(-1) #Source file is unreadable
        fh = open(file, "r")
        buff = 10

        #remove the destination fike if it exists
        if (os.access(file[0:-4], os.F_OK)):
            os.remove(file[0:-4])
        fho = open(file[0:-4], "w")

        a = fh.read(buff)
        while a != "":
            for j in a:
                c = ord(j)
                c = ~(c ^ 0xAA)
                c = chr(c)
                fho.write(c)
            a = fh.read(buff)
    except Exception:
        return -2  # io error
    finally:
        if falm is not None:
            falm.close()
        if fho is not None:
            fho.close()
        if fh is not None:
            fh.close()
    return 0  # Success


# ====GUI END=========Do-ers=========IMPLEMENTATION===========

def doCopy():
    global currClip, CURR_FILE_SELECTION
    for i in CURR_FILE_SELECTION:
        currClip.append(os.path.join(os.getcwd(), i))

def doPaste():
    global currClip, CUT_ENABLED
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
            # see if the selected file is a directory or not.
            if os.path.isdir(i):
                # start copying
                shutil.copytree(i, cwd) # Check the syntax
                if CUT_ENABLED:
                    shutil.rmtree(i)
            else:
                if not CUT_ENABLED:
                    shutil.copy(i, cwd)
                if CUT_ENABLED:
                    shutil.move(i, cwd)
    except shutil.Error as err:
        print(err)
    CUT_ENABLED = False
    if errors:
        errorstr = "Errors occured during the pasting of:"
        for i in errornous:
            errorstr += ("\n\t" + i)
        errorstr += "All other files were copied successfully."
        root.wait_window(MessageDialog(root, "Erros Occured During Paste", errorstr).dialog)
    else:
        root.wait_window(MessageDialog(root, "Successfully Pasted", "All Operations completed successfully").dialog)


def doCut():
    global CUT_ENABLED
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

def doTerminal():
    # Open the terminal in the current directory
    cwd = os.getcwd()
    tmp = None
    try:
        tmp = open("temp_007.bat", "w")
        # See if this is the correct drive
        if not (cwd.startswith("C:")):
            tmp.write(cwd[0:2] + "\n")
        tmp.write("cd " + cwd)
    except Exception as e:
        print(e)
    finally:
        if not tmp:
            tmp.close()
    os.system("cmd \\K " + os.path.join(cwd, "temp_007.bat"))

def doRun():
    # attempt to see if the given file is an executable
    # Windows specific implementation:
    global CURR_FILE_SELECTION
    for i in CURR_FILE_SELECTION:
        if i.endswith(".exe"):
            os.system(i)
        else:
            continue


def doEncrypt():
    # The user has pressed the Encrypt button, start encryption.
    global CURR_FILE_SELECTION
    if len(CURR_FILE_SELECTION) == 0:
        root.wait_window(MessageDialog(root, "Error", "No File selected for encryption/decryption").dialog)

    # Fetch the password for encryption or decryption:
    # Show the password input dialog:
    pass_dialog = EntryDialog(root, "Enter the Password:")
    root.wait_window(pass_dialog.dialog)
    # fetch the password:
    global ALMANAC_LOCATION
    psswd = pass_dialog.finalText
    del pass_dialog
    for i in CURR_FILE_SELECTION:
        if i.endswith(".eny"):
            ret = decryptFile(os.getcwd() + CURR_FILE_SELECTION, psswd, ALMANAC_LOCATION)
            # Error Processing:
            if ret != 0:
                error_str = ""
                # Delete any files generated
                if os.access(i[0:-4], os.F_OK):
                    os.remove(i[0:-4])
                # Process the return code:
                if ret == -1:
                    error_str = "The File, " + i + " is unreadable. (No read privialge)"
                if ret == -2:
                    error_str = "Errors during reading or writing files while working with " + i
                if ret == -3:
                    error_str = "Files can only be decrypted on the machine at which they were encrypted."
                if ret == -4:
                    error_str = "Password for the file, " + i + " is wrong. Try Again."
                root.wait_window(MessageDialog(root, "Errors Occured", error_str).dialog)
        else:  # File has to be encrypted
            # Code for ordering a file encryption follows
            # First, try to encrypt the file
            ret = encryptFile(i)
            if ret == 0:  # Encryption successful, delete the source file and make an almanac entry
                try:
                    if os.access(ALMANAC_LOCATION, os.R_OK) :
                        root.wait_window(MessageDialog(root, "Error", "Encryption failed. No read privilage to the almanac.").dialog)
                        os.remove(i + ".eny")
                        continue
                    falm = open(ALMANAC_LOCATION, "a")
                    falm.write(i + ":" + i + ".eny" + "\n")
                except Exception:
                    root.wait_window(MessageDialog(root, "Error", "Errors Occcured during writing the almanac.").dialog)
                    os.remove(i + ".eny")
                    continue
            if ret != 0:  # Errors occrued
                error_str = ""
                if ret == -1:
                    error_str = "The File, " + i + " is unreadable. (No read privialge)"
                if ret == -2:
                    error_str = "Errors during reading or writing files while working with " + i
                root.wait_window(MessageDialog(root, "Error", error_str).dialog)
                os.remove(i+".eny")
        root.wait_window(MessageDialog(root, "Done", "All operations completed successfully.").dialog)


def doRename():
    global CURR_FILE_SELECTION
    ed = EntryDialog(root, "Enter the new file name:")
    root.wait_window(ed.dialog)
    newFileName = ed.finalText
    # For now it is assumed that the filename supplied by the user is stored in a variable
    # called newFileName
    if len(CURR_FILE_SELECTION) > 1:
        print("Too many files to rename. Rename one file at a time.")
    else:
        os.system("rename " + CURR_FILE_SELECTION[0] + " " + newFileName)


# Testing The GUI Elements
ENTRY_DIALOG_TEST = False
MESSAGE_DIALOG_TEST_1 = False
MESSAGE_DIALOG_TEST_2 = False
FILE_DISPLAY_TEST = False
TREEVIEW_TEST = True
# Testing the EntryDialog
if ENTRY_DIALOG_TEST:
    root = tk.Tk()
    ed = EntryDialog(root, "Lorem Ipse")
    root.wait_window(ed.dialog)
    print(ed.finalText)
    root.mainloop()
if MESSAGE_DIALOG_TEST_1:
    root = tk.Tk()
    root.wait_window(MessageDialog(root, "Lorem Ipsum", "All Good.").dialog)
    root.mainloop()
if MESSAGE_DIALOG_TEST_2:
    root = tk.Tk()
    md = MessageDialog(root, "Lorem Ipsum", "All Good", mode=MessageDialog.DIALOG_YESNO)
    root.wait_window(md.dialog)
    print(md.result)
    root.mainloop()
if FILE_DISPLAY_TEST:
    def doButton():
        print(fl.getCurrentSelection())
    root = tk.Tk()
    frm = tk.Frame(root)
    fl = FileLister(frm, [["#0", "one", "two"], ["Latin", "English", "Hindi"], ["Lumos", "Light", "Prakash"], ["Juno", "Jupiter", "Vishnu Dev"]])
    frm.pack()
    tk.Button(root, text="Print Selection", command=doButton).pack()
    root.mainloop()
if TREEVIEW_TEST:
    def doButton():
        global fl
        print(fl.getCurrentSelection())
    dataset = [
        ["#0", "#1", "#2"],
        ["Heading 1", "Heading 2", "Heading 3"],
        ["Content 1 1", "Content 1 2", "Content 1 3"],
        ["Contnet 2 1", "Content 2 1", "Content 2 3"],
        ["End 1", "End 2", "End 3"]
    ]
    root = tk.Tk()
    fl = FileLister(root, dataset)
    tk.Button(root, text="Show what's entered", command=doButton).pack()
    root.mainloop()