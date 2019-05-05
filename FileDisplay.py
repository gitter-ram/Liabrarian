import tkinter as tk
class FilePlayground:
  SELECTION = []
  PERMITTED_ICON_SIZES = (16,32,48,256)
  CURR_ICON_SIZE = 32
  def __init__(parent, height, width, items, iconsize=32, configdir="C:\\Program Settings\\Liabrarian\\"):
    #First, initialize the canvas and some icons
    ICON_IMG = []
    CURR_ICON_SIZE = iconsize
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
      ICON_IMG.append(tk.PhotoImage(file=ICON))
    #start rendering the canvas:
    #get the height and the width of the parent
