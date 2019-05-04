import tkinter as tk
class FilePlayground:
  SELECTION = []
  PERMITTED_ICON_SIZES = (16,32,48,256)
  CURR_ICON_SIZE = 32
  def __init__(parent, height, width, items, iconsize=32):
    #First, initialize the canvas and some icons
    CURR_ICON_SIZE = iconsize
    self.canv = tk.Canvas(master, width=width, height=height)
    self.canv.pack()
    #add the icons and their discriptions
    for i in items:
      #Load the icons:
