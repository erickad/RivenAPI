#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 22:58:45 2019

@author: erickad
"""
import sys
from os import path
from json import load
from requests import get

import matplotlib
matplotlib.use('TkAgg', warn=False)
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import ttk

class Window(tk.Frame):
    """Main tkinter window"""
    def make_widgets(self):
        self.winfo_toplevel().title("Simple Riven API GUI")
    
    def __init__(self,parent=None):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.pack()
        self.make_widgets()

def parse(filename):
    """Simple parse function"""
    parsed = None
    with open(filename) as f:
        parsed = load(f)
    return parsed

def itemize(jList):
    """
    Itemizes the parsed json for each member, uses string with splits for use with combobox
    """
    itemsList = [  (w["itemType"]+" | "+w["compatibility"]+" | "+"Rolled")
    #Decide if veiled/unrolled/rolled
    if w["compatibility"] is not None and w["rerolled"]
    else 
    (w["itemType"]+" | "+w["compatibility"]+" | "+"Unrolled")
    if w["compatibility"] is not None and not w["rerolled"]
    else ( w["itemType"]+" | "+"Veiled"+" | "+"NaN")  for w in jList]
    return itemsList

def getType(type,iList):
    """Simple function to get what type the riven is"""
    tList = [i for i in iList if i.split(' | ')[0]==type]
    return tList


def selected(event, mid, pFile, LSVars, lbPaneT):
    """"Display only the selected combobox"""
    riven = event.widget.get()
    rivenS = riven.split(' | ')
    rivenR = True if rivenS[2] == "Rolled" else False

    if rivenS[1] != "Veiled":
        for r in pFile:
            if rivenS[1] == r["compatibility"] and rivenR == r["rerolled"]:
                setCurrent(r,lbPaneT, mid)
                break
    else:
        for r in pFile:
            if rivenS[0] == r["itemType"]:
                setCurrent(r,lbPaneT, mid)
                break
    for lVar in LSVars:
        if lVar.get() != riven:
            lVar.set("")
      
def setCurrent(riven, lbPaneT, middle):
    """Function to display the values with tkinter"""
    stddev = riven["stddev"]
    minR = riven["min"]
    maxR = riven["max"]
    pop = riven["pop"]
    median = riven["median"]
    
    mFig = middle.figure
    mFig.clf()
    a = mFig.add_subplot(1,1,1,ylabel="Pop",xlabel="Plat",
                 title="")
    
    x = [minR, max(minR,median-stddev), median,
         min(maxR,median+stddev), maxR]
    y = [0.00001,pop/3,pop,pop/3,0.00001]
    
    
    a.plot(x,y)
    a.annotate("min",(x[0],y[0]))
    a.annotate("-stddev",(x[1],y[1]))
    a.annotate("median",(x[2],y[2]))
    a.annotate("+stddev",(x[3],y[3]))
    a.annotate("max",(x[4],y[4]))

    a.grid()
    
    mFig.canvas.draw()
    displayRiven(lbPaneT, riven)
    
def displayRiven(lbPane, riven):
    """Function used by setCurrent() to set widget values"""
    lbPane.nametowidget("wep").config(text=riven['compatibility'])
    lbPane.nametowidget("typ").config(text=riven['itemType'])
    if (riven['rerolled']):
        lbPane.nametowidget("rol").config(text='True')
    else:
        lbPane.nametowidget("rol").config(text='False')
    lbPane.nametowidget("pop").config(text=riven['pop'])
    lbPane.nametowidget("med").config(text=riven['median'])
    lbPane.nametowidget("avg").config(text=riven['avg'])
    lbPane.nametowidget("std").config(text=riven['stddev'])
    lbPane.nametowidget("minV").config(text=riven['min'])
    lbPane.nametowidget("maxV").config(text=riven['max'])

def printHelp():
    """Prints a help menu on commandline"""
    print("{:<10}: rivenAPI.py [file | int]".format("usage"))
    print("{:<10}: filename present for .json to parse".format("file"))
    print("{:<10}: preset .json files taken from DE repo via internet".format("int"))
    print("            1:PC 2:PS4 3:Xbox 4:Switch")
    print("{:<10}: prints this help".format("-h --help"))
    
    return


#---Parsing data
parsedFile = []
itemizedFile = []
iFileA = []
iFileK = []
iFileM = []
iFileP = []
iFileR = []
iFileS = []
iFileZ = []
defaultFN = "weeklyRivensPC.json"

#Handle arguments from commandline
if (len(sys.argv) > 1):
    if '-h' or '--help' in sys.argv:
        printHelp()
    #prioritize filename over integers
    if (True in [path.exists(a) for a in sys.argv[1:]]):
        for a in sys.argv[1:]:
            if path.exists(a):
                fn = a
        parsedFile = parse(fn)
    #integers are prioritized numerically for simplicity
    elif('1' in sys.argv):
        r = get('http://n9e5v4d8.ssl.hwcdn.net/repos/weeklyRivensPC.json')
        parsedFile = r.json() 
    elif('2' in sys.argv):
        r = get("http://n9e5v4d8.ssl.hwcdn.net/repos/weeklyRivensPS4.json")
        parsedFile = r.json() 
    elif('3' in sys.argv):
        r = get("http://n9e5v4d8.ssl.hwcdn.net/repos/weeklyRivensXB1.json")   
        parsedFile = r.json() 
    elif('4' in sys.argv):
        r = get("http://n9e5v4d8.ssl.hwcdn.net/repos/weeklyRivensSWI.json")
        parsedFile = r.json()
    #else use default filename
    else:
        if not path.exists(defaultFN):
            print("No default file \'{}\' found.".format(defaultFN))
            quit()
        else:
            print("No file specified, using default \'{}\'".format(defaultFN))
            parsedFile = parse(defaultFN)
#else use default filename
else:
    if not path.exists(defaultFN):
        print("No default file \'{}\' found.".format(defaultFN))
        quit()
    else:
        print("No file specified, using default \'{}\'".format(defaultFN))
        parsedFile = parse(defaultFN)
itemizedFile = itemize(parsedFile)


iFileA = getType("Archgun Riven Mod", itemizedFile)
iFileK = getType("Kitgun Riven Mod", itemizedFile)
iFileM = getType("Melee Riven Mod", itemizedFile)
iFileP = getType("Pistol Riven Mod", itemizedFile)
iFileR = getType("Rifle Riven Mod", itemizedFile)
iFileS = getType("Shotgun Riven Mod", itemizedFile)
iFileZ = getType("Zaw Riven Mod", itemizedFile)
#---Parsing Data End

#---Create Window
root = tk.Tk()
win = Window(root)
main = tk.PanedWindow(win)
main.pack()
root.title = ('Simple Riven API GUI')

#---Create Left Pane
left = tk.Frame(main)
left.pack(side="left")
#---Create Left Pane End

#---Create LeftT Pane
leftT = tk.Frame(left)
labelL = tk.Label(leftT,text="Weapontype:").grid(columnspan=2)
leftT.pack(side="top")
#---Create LeftT Pane End

#---Create leftB Pane
leftB = tk.Frame(left)
leftBL = tk.Label(leftB,text="Data:")
leftBL.grid(columnspan=2)
leftBWepL = tk.Label(leftB,text="Weapon:",relief="groove")
leftBWepL.grid(row=1,column=0, sticky='e')
leftBTypL = tk.Label(leftB,text="Type:",relief="groove")
leftBTypL.grid(row=2,column=0, sticky='e')
leftBRolL = tk.Label(leftB,text="Rolled:",relief="groove")
leftBRolL.grid(row=3,column=0, sticky='e')
leftBPopL = tk.Label(leftB,text="Popularity:",relief="groove")
leftBPopL.grid(row=4,column=0, sticky='e')
leftBMedL = tk.Label(leftB,text="Median:",relief="groove")
leftBMedL.grid(row=5,column=0, sticky='e')
leftBAvgL = tk.Label(leftB,text="Average:",relief="groove")
leftBAvgL.grid(row=6,column=0, sticky='e')
leftBStdL = tk.Label(leftB,text="Standard deviation:",relief="groove")
leftBStdL.grid(row=7,column=0, sticky='e')
leftBMinL = tk.Label(leftB,text="Minimum:",relief="groove")
leftBMinL.grid(row=8,column=0, sticky='e')
leftBMaxL = tk.Label(leftB,text="Maximum:",relief="groove")
leftBMaxL.grid(row=9,column=0, sticky='e')
leftBWepVaL = tk.Label(leftB, anchor='w',name='wep')
leftBWepVaL.grid(row=1,column=1, sticky='w')
leftBTypVaL = tk.Label(leftB, anchor='w',name='typ')
leftBTypVaL.grid(row=2,column=1, sticky='w')
leftBRolVaL = tk.Label(leftB, anchor='w',name='rol')
leftBRolVaL.grid(row=3,column=1, sticky='w')
leftBPopVaL = tk.Label(leftB, anchor='w',name='pop')
leftBPopVaL.grid(row=4,column=1, sticky='w')
leftBMedVaL = tk.Label(leftB, anchor='w',name='med')
leftBMedVaL.grid(row=5,column=1, sticky='w')
leftBAvgVaL = tk.Label(leftB, anchor='w',name='avg')
leftBAvgVaL.grid(row=6,column=1, sticky='w')
leftBStdVaL = tk.Label(leftB, anchor='w',name='std')
leftBStdVaL.grid(row=7,column=1, sticky='w')
leftBMinVaL = tk.Label(leftB, anchor='w',name='minV')
leftBMinVaL.grid(row=8,column=1, sticky='w')
leftBMaxVaL = tk.Label(leftB, anchor='w',name='maxV')
leftBMaxVaL.grid(row=9,column=1, sticky='w')
leftB.pack(side="top")
#---Create leftB Pane End

#---Create Middle Pane
fig = Figure(figsize=(10,10),dpi=100)
rect = 0.08,0.08,0.89,0.89
a = fig.add_subplot(1,1,1,ylabel="Popularity",xlabel="Platinum",
                 title="")
middle = FigureCanvasTkAgg(fig, master=main)
middle.get_tk_widget().pack(side="left", anchor="e")
#---Creat Middle Pane End

#---GUI
leftVarAll = tk.StringVar(leftT)
leftVarA = tk.StringVar(leftT)
leftVarK = tk.StringVar(leftT)
leftVarM = tk.StringVar(leftT)
leftVarP = tk.StringVar(leftT)
leftVarR = tk.StringVar(leftT)
leftVarS = tk.StringVar(leftT)
leftVarZ = tk.StringVar(leftT)
lStrVars = [leftVarAll, leftVarA, leftVarK,leftVarM,leftVarP,
                  leftVarR,leftVarS,leftVarZ]

labelAll = tk.Label(leftT,text='All').grid(row=2,column=0)
labelA = tk.Label(leftT,text='Archgun').grid(row=3,column=0)
labelK = tk.Label(leftT,text='Kitgun').grid(row=4,column=0)
labelM = tk.Label(leftT,text='Melee').grid(row=5,column=0)
labelP = tk.Label(leftT,text='Pistol').grid(row=6,column=0)
labelR = tk.Label(leftT,text='Rifle').grid(row=7,column=0)
labelS = tk.Label(leftT,text='Shotgun').grid(row=8,column=0)
labelZ = tk.Label(leftT,text='Zaw').grid(row=9,column=0)

ddmAll = ttk.Combobox(leftT,textvariable =leftVarAll,
                    values=itemizedFile,width=50,
                    state="readonly")
ddmAll.grid(row=2,column=1)
ddmAll.bind("<<ComboboxSelected>>", lambda event,
          arg=0: selected(event, middle, parsedFile, lStrVars, leftB))

ddmA = ttk.Combobox(leftT,textvariable =leftVarA,
                    values=iFileA,width=50,
                    state="readonly")
ddmA.grid(row=3,column=1)
ddmA.bind("<<ComboboxSelected>>", lambda event,
          arg=0: selected(event, middle, parsedFile, lStrVars, leftB))

ddmK = ttk.Combobox(leftT,textvariable =leftVarK,
                    values=iFileK,width=50,
                    state="readonly")
ddmK.grid(row=4,column=1)
ddmK.bind("<<ComboboxSelected>>", lambda event,
          arg=0: selected(event, middle, parsedFile, lStrVars, leftB))

ddmM = ttk.Combobox(leftT,textvariable =leftVarM,
                    values=iFileM,width=50,
                    state="readonly")
ddmM.grid(row=5,column=1)
ddmM.bind("<<ComboboxSelected>>", lambda event,
          arg=0: selected(event, middle, parsedFile, lStrVars, leftB))

ddmP = ttk.Combobox(leftT,textvariable =leftVarP,
                    values=iFileP,width=50,
                    state="readonly")
ddmP.grid(row=6,column=1)
ddmP.bind("<<ComboboxSelected>>", lambda event,
          arg=0: selected(event, middle, parsedFile, lStrVars, leftB))

ddmR = ttk.Combobox(leftT,textvariable =leftVarR,
                    values=iFileR,width=50,
                    state="readonly")
ddmR.grid(row=7,column=1)
ddmR.bind("<<ComboboxSelected>>", lambda event,
          arg=0: selected(event, middle, parsedFile, lStrVars, leftB))

ddmS = ttk.Combobox(leftT,textvariable =leftVarS,
                    values=iFileS,width=50,
                    state="readonly")
ddmS.grid(row=8,column=1)
ddmS.bind("<<ComboboxSelected>>", lambda event,
          arg=0: selected(event, middle, parsedFile, lStrVars, leftB))

ddmZ = ttk.Combobox(leftT,textvariable =leftVarZ,
                    values=iFileZ,width=50,
                    state="readonly")
ddmZ.grid(row=9,column=1)
ddmZ.bind("<<ComboboxSelected>>",  lambda event,
          arg=0: selected(event, middle, parsedFile, lStrVars, leftB))
#---GUI End

root.mainloop()
#---Create Window End
