# from  tkinter import *
# from tkinter import filedialog
# root = Tk()
# root.withdraw()
# ScFile =  filedialog.askopenfilename(initialdir = "/", title = "Select Season clients file")
# #VrFile =  filedialog.askopenfilename(initialdir = "/", title = "Select vertical repayment file")

# import pandas as pd

# data = pd.read_excel(scFile)

# print(data.head())

from tkinter import filedialog as fd
from  tkinter import *
root = Tk()
root.withdraw()
file = fd.askopenfile(title="OPEN A FILE")
if file: 
    print(file.name)

import pandas as pd 
import os
data = pd.read_excel(file.name) 

x = data.head(5)

#path = fd.asksaveasfile(initialdir="/", title="Save file",filetypes=(("txt files", "*.txt"),("all files", "*.*")))

path = fd.askdirectory(initialdir="/", title="Select file")

print(path)

os.chdir(path)

x.to_excel('Arsene.xlsx')
 