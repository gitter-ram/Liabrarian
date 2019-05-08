import tkinter as tk
class FilePlayground:
  SELECTION = []
  PERMITTED_ICON_SIZES = (16,32,48,256)
  CURR_ICON_SIZE = 32
  def __init__(parent, height, width, items, iconsize=32, configdir="C:\\Program Settings\\Liabrarian\\"):
    #First, initialize the canvas and some icons
    self.ICON_IMG = {}
    self.CURR_ICON_SIZE = iconsize
    self.canv = tk.Canvas(master, width=width, height=height)
    self.canv.pack()
    #add the icons and their discriptions
    for i in items:
      #Load the icons:
      if os.isdir(i):
        ICON = os.path.join(configdir, "\\icons\\current theme\\folder.gif"))
      else:
        if i.find('.') == -1:
          ICON = os.path.join(configdir, ("\\icons\\current theme\\" + i + ".gif"))
        else:
          ICON = os.path.join(configdir, ("\\icons\\current theme\\" + i[(i.find('.') + 1):] + ".gif"))
      ICON_IMG.update({i[((i.find('.')+1):]:tk.PhotoImage(file=ICON)})
    #start rendering the canvas:
    #get the height and the width of the parent
    tk.update()
    canv_height = self.canv.winfo_height
    canv_width = self.canv.winfo_width
    #Read the settings file
    af = open(os.path.join(configdir, "settings.cnf"), "r")
    #start reading:
    while (a = af.readline()) != "":
      if(a == "</Display>"):
        break
      if(a == "<Display>"):
        flag = True
      if flag:
        if ((a.trim())[0:(a.trim().find(':'))]) == "SpaceBetweenIcons":
          self.ICON_SPACING = int((a.trim())[(a.trim().find(':')+1):])
          break
    af.close()
    #place the icons
    self.grid = [(self.canv_width // (self.ICON_SIZE + self.ICON_SPACING)), (self.canv_height // (self.ICON_SIZE + self.ICON_SPACING))]
    self.updateCanvas(items, nodelete=True)
  
  def updateCanvas(items, selected, nodelete=False):
    #Delete all the items on the canvas first:
    if not nodelete:
      self.canv.delete(self.objectsDrawn) #objectsdrawn is a list of all the objects that were drawn.
    #Start drawing the objects
    j = 0
    TEXT_ICON_SPACE = 5
    NUM_COLUMNS = self.parent.winfo_width() // (self.ICON_SIZE + (4 * self.ICON_SPACING))
    NUM_ROWS = self.parent.winfo_height() // (self.ICON_SIZE + (2 * self.ICON_SPACING))
    for i in range(0, NUM_ROWS):
      for j in range(0, NUM_COLUMNS):
        x = (j * (self.ICON_SIZE + self.ICON_SPACING))
        y = (i * (self.ICON_SIZE + 2 * self.ICON_SPACING))
        alpha = i * NUM_COLUMNS + j
        #Find the appropriate icons and display them.
        if selected[items[alpha]] == True:
          #draw a blue rectangle around the icon:
          objectsDrawn.append(canv.create_rectangle((x - (ICON_SPACING // 2), (y - (ICON_SPACING // 2)), (x + ICON_SIZE + (ICON_SPACING // 2)), (y + ICON_SIZE + (ICON_SPACING // 2)), fill='blue') 
        extension =(iems[alpha])[(items[alpha].find('.') + 1):]
        objectsDrawn.append(canv.create_image(x, y, self.ICON_IMG[extension]))
        #display the names as well.
        objectsDrawn.append(canv.create_text((x + 5), (y + self.ICON_SIZE + self.ICON_SPACING), text=items[alpha])
        
         
