import tkinter as tk
import tkinter.tix as tx

root = tk.Tk()
List1 = ("Lorem", "Ipsum", "Foo", "Bar", "Do")
tLister = tx.TList(root)
for i in List1:
  tLister.insert(tkinter.tix.END, itemtype="text", text=i)
root.pack()
tLister.pack()
root.mainloop()
'''This test is successful if you see a 
   TList with the given tuple of strings.'''
