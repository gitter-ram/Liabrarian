import tkinter as tk
class FilePlayground:
  SELECTION = []
  PERMITTED_ICON_SIZES = (16,32,48,256)
  CURR_ICON_SIZE = 32
  def __init__(parent, iconsize=32):
    #First, initialize the canvas and some icons
    CURR_ICON_SIZE = iconsize
    self.canv = tk.Canvas(
