import os
import shutil

# GUI Frontend :
import tkinter.ttk as ttk
import tkinter as tk

PNG_CAN_BE_USED = False

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
        inp.bind("<Return>", lambda eve:self.OK_button_pressed())
        inp.focus_set()

    def OK_button_pressed(self, *event):
        self.finalText = self.uinput.get()
        self.dialog.destroy()

    def Cancel_button_pressed(self, *event):
        self.finalText = None
        self.dialog.destroy()


class FileLister:
    def __init__(self, parent, dataset, callback=None,icons=False, nopack=False):
        self.frame = tk.Frame(parent)
        self.dataset = dataset
        self.tree = ttk.Treeview(self.frame, column=dataset[0])
        self.pack_used = not nopack
        self.icons_enabled = icons
        self.double_callback = callback
        for i in range(0, len(dataset[0])):
            if not icons:
                if i == 0:
                    continue
                    self.tree.heading(dataset[0][0], text="")
                else:
                    self.tree.heading(dataset[0][i], text=dataset[1][i])
        for i in range(2, len(dataset)):
            if not icons:
                self.tree.insert("", "end", iid=i, text=dataset[i][0], values=dataset[i][1:])
            else:
                self.tree.insert()
        self.tree.bind("<Double-Button-1>", callback if callback is not None else self.doubleDefault)
        if not nopack:
            self.tree.pack()
            self.frame.pack()

    def updateFileLister(self):
        global CURR_FILES_DISPLAYED
        self.dataset = CURR_FILES_DISPLAYED
        self.tree.pack_forget() if self.pack_used else self.tree.grid_forget()

        self.tree = ttk.Treeview(self.frame, column=self.dataset[0])
        for i in range(0, len(self.dataset[0])):
            if not self.icons_enabled:
                if i == 0:
                    self.tree.heading(self.dataset[0][0], text="")
                    continue
                else:
                    self.tree.heading(self.dataset[0][i], text=self.dataset[1][i])
        for i in range(2, len(self.dataset)):
            if not self.icons_enabled:
                self.tree.insert("", "end", iid=i, text=self.dataset[i][0], values=self.dataset[i][1:])
            else:
                self.tree.insert()
        self.tree.bind("<Double-Button-1>", self.double_callback if self.double_callback is not None else self.doubleDefault)

        self.tree.pack() if self.pack_used else self.tree.grid(row=0, column=1)


    def doubleDefault(self, event):
        print(self.getCurrentSelection())

    def getCurrentSelection(self):
        sel = []
        for i in self.tree.selection():
            i = int(i)
            sel.append(self.dataset[i][0])
        return tuple(sel)


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


def doNewFolder():
    global root
    ed = EntryDialog(root,"Enter the name for the new folder: ")
    root.wait_window(ed.dialog)
    name = ed.finalText
    if not name in os.listdir():
        os.mkdir(name)
    else:
        os.mkdir(name + "(1)")
    directoryChanged(os.getcwd())



# Some global dynamic constants: (CORE)
SYSTEM_TYPE = "Need To Be Detected."
CURR_FILE_SELECTION = []
CUT_ENABLED = False


# =====GUI END=========Do-ers=========IMPLEMENTATION===========
def doCopy():
    global currClip, CURR_FILE_SELECTION
    currClip = []
    CURR_FILE_SELECTION = fileLister.getCurrentSelection()
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
    directoryChanged(os.getcwd())


def doCut():
    global CUT_ENABLED
    doCopy()
    CUT_ENABLED = True

def doDelete():
    global CURR_FILE_SELECTION, fileLister
    CURR_FILE_SELECTION = fileLister.getCurrentSelection()
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
    directoryChanged(os.getcwd())

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
    CURR_FILE_SELECTION = fileLister.getCurrentSelection()
    for i in CURR_FILE_SELECTION:
        if i.endswith(".exe"):
            os.system(i)
        else:
            continue


def doRename():
    global fileLister
    CURR_FILE_SELECTION = fileLister.getCurrentSelection()
    ed = EntryDialog(root, "Enter the new file name:")
    root.wait_window(ed.dialog)
    newFileName = ed.finalText
    # For now it is assumed that the filename supplied by the user is stored in a variable
    # called newFileName
    if len(CURR_FILE_SELECTION) > 1:
        print("Too many files to rename. Rename one file at a time.")
    else:
        os.system("rename " + CURR_FILE_SELECTION[0] + " " + newFileName)
    directoryChanged(os.getcwd())


givenOptions = {"NewFolder":doNewFolder, "Cut":doCut, "Copy":doCopy,
                "Paste":doPaste, "Delete":doDelete,"Open Terminal":doTerminal,
                "Rename":doRename, "Run":doRun}


class Drawer:
    def __init__(self, parent, nopack=False):
        global givenOptions
        self.frame = tk.Frame()
        for i in givenOptions:
            '''image = i + ".gif"
            print(image)
            image = os.path.join(os.path.dirname(__file__), image)
            print(image)
            image = tk.PhotoImage(file=image)
            tk.Button(frame, image=image, command=givenOptions[i]).pack()'''
            tk.Button(self.frame, text=i, command=givenOptions[i], anchor=tk.S).pack()
        if not nopack:
            self.frame.pack()


dataset_templ = [
        ["#0", "#1", "#2", "#3", "#4"],
        ["File name", "Readable", "Writable", "Executable", "Type"]
    ]

def updateUI():
    global root, fileLister, CURR_FILES_DISPLAYED
    fileLister.tree.pack_forget()
    fileLister.updateFileLister()
    print(CURR_FILES_DISPLAYED)

def updateDataset():
    global dataset_templ
    dataset = list(dataset_templ)
    for i in os.listdir():
        j = list()
        j.append(i)
        j.append(True if os.access(i, os.R_OK) else False)
        j.append(True if os.access(i, os.W_OK) else False)
        j.append(True if os.access(i, os.X_OK) else False)
        j.append("Folder" if os.path.isdir(i) else "File")
        dataset.append(j)
    return dataset


def directoryChanged(i):
    global CURR_FILES_DISPLAYED
    print(os.path.isdir(os.path.join(os.getcwd(), i)))
    if os.path.isdir(os.path.join(os.getcwd() , i)):
        os.chdir(i)
        print(os.getcwd())
        CURR_FILES_DISPLAYED = updateDataset()
        print(CURR_FILES_DISPLAYED)
    else:
        doRun()
    updateUI()


def fileDoubleClicked(event):
    global root, CURR_FILES_DISPLAYED
    CURR_FILE_SELECTION = fileLister.getCurrentSelection()
    print(CURR_FILE_SELECTION)
    i = CURR_FILE_SELECTION[0]
    root.title(os.path.join(os.getcwd(), i))
    directoryChanged(i)


def entryDirectory():
    global addressBar
    dir = addressBar.get()
    directoryChanged(dir)


def goBack():
    directoryChanged("..")

def initGUI():
    global root, fileLister, addressBar, scrollbar
    root = tk.Tk()
    drawer = Drawer(root, nopack=True)
    fileLister = FileLister(root, updateDataset(), nopack=True, callback=fileDoubleClicked)
    tk.Button(root, text="Back", command=goBack).grid(row=0, column=0)
    tk.Button(root, text="Go", command=entryDirectory).grid(row=0, column=3)
    addressBar = tk.Entry(root)
    addressBar.grid(row=0, column=1, columnspan=2, sticky=tk.W)
    addressBar.bind("<Return>", lambda eve:entryDirectory())
    drawer.frame.grid(row=1, column=0)
    fileLister.tree.grid(row=1, column=1, columnspan=2)
    fileLister.frame.grid(row=1, column=2, columnspan=2)
    fileLister.tree.focus_set()
    root.bind("<Control-n>", lambda eve:doNewFolder())
    root.title(os.getcwd())
    root.mainloop()


# Testing The GUI Elements
ENTRY_DIALOG_TEST = False
MESSAGE_DIALOG_TEST_1 = False
MESSAGE_DIALOG_TEST_2 = False
FILE_DISPLAY_TEST = False
TREEVIEW_TEST = False
DRAWER_TEST = False
IMAGE_TEST = False
CANVAS_TEST = False
GUI_MAIN_ROTINE_TEST = True
# Testing the EntrDialog
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
    def updateDataset():
        global dataset_templ
        dataset = list(dataset_templ)
        for i in os.listdir():
            j = list()
            j.append(i)
            j.append(True if os.access(i, os.R_OK) else False)
            j.append(True if os.access(i, os.W_OK) else False)
            j.append(True if os.access(i, os.X_OK) else False)
            j.append("Folder" if os.path.isdir(i) else "File")
            dataset.append(j)
        return dataset

    def updateUI():
        global fl, root
        root.destroy()
        del root
        root = tk.Tk()
        root.geometry("1200x300+1+1")
        root.title("File Displayer")
        fl = FileLister(root, dataset)
        tk.Button(root, text="Up a folder", command=doButton1).pack()
        tk.Button(root, text="Go inside this folder", command=doButton2).pack()
        root.mainloop()

    def doButton1():
        os.chdir("..")
        global fl, dataset, root
        dataset = updateDataset()
        updateUI()

    def doButton2(args=None):
        global fl, dataset
        os.chdir(fl.getCurrentSelection()[0])
        dataset = updateDataset()
        updateUI()

    def doButton3():
        print(fl.getCurrentSelection())

    dataset_templ = [
        ["#0", "#1", "#2", "#3", "#4"],
        ["File name", "Readable", "Writable", "Executable", "Type"]
    ]
    dataset = updateDataset()
    root = tk.Tk()

    fl = FileLister(root, dataset)
    tk.Button(root, text="Up a folder", command=doButton1).pack()
    tk.Button(root, text="Go inside this folder", command=doButton2).pack()
    tk.Button(root, text="Print Current selection", command=doButton3).pack()
    print(root.geometry())
    root.mainloop()
if DRAWER_TEST:
    root = tk.Tk()
    drawer = Drawer(root)
    root.mainloop()
if IMAGE_TEST:
    root = tk.Tk()
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()
    img = tk.PhotoImage(file="NewFolder.gif")
    canvas.create_image(20, 20, anchor=tk.NW, image=img)
    root.mainloop()
if CANVAS_TEST:
    root = tk.Tk()
    canv = tk.Canvas()
    canv.pack()
    canv.create_text(10, 10, text="Alpha", anchor=tk.NW)
    root.mainloop()
if GUI_MAIN_ROTINE_TEST:
    initGUI()
