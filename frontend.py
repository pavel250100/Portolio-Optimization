from tkinter import *
import tkinter.font as font
from backend import Optimization
import pandas

key = 'zNGkjoezFCzFkGyFwraJ'
optimize = Optimization(key)

def createEntries():
    nextRow = len(Ents)
    ent = Entry(interface)
    ent.grid(row = nextRow + 2, column = 0, columnspan = 3)
    Ents.append(ent)

def deleteEntries():
    Ents[-1].destroy()
    del Ents[-1]

def showEntries():
    Entries.clear()
    for x in Ents:
        Entries.append(x.get())
    optimize.calculation(Entries)

    i = 0
    lowVolPort = Label(interface, text = "Portfolio with the lowest Varience:")
    lowVolPort.grid(row = len(Entries) + 3, column = 0, columnspan = 3)
    lowVolPort['font'] = myFont2
    for x in Entries:
        lab = Label(interface, text = "Weight of " + x + " = " + str(round(optimize.min_variance_port.iloc[0][x + ' Weight'] * 100, 4)) + "%", anchor=W)
        lab.grid(row = len(Entries) + 4 + i, column = 0, columnspan = 3)
        i += 1
    
    i = 0
    sharpeRatioPort = Label(interface, text = "Portfolio with the Sharpe Ratio:")
    sharpeRatioPort.grid(row = len(Entries) * 2 + 4, column = 0, columnspan = 3)
    sharpeRatioPort['font'] = myFont2
    for x in Entries:
        lab = Label(interface, text = "Weight of " + x + " = " + str(round(optimize.sharpe_portfolio.iloc[0][x + ' Weight'] * 100, 4)) + "%", anchor=W)
        lab.grid(row = len(Entries) * 2 + 5 + i, column = 0, columnspan = 3)
        i += 1

    graphButton = Button(interface, text = "Graphics", height = 1, width = 10, command = drawGraph)
    graphButton.grid(row = 6 * len(Entries) + 6, column = 0, columnspan = 3)

def drawGraph():
    optimize.graph()

Entries = []
Ents = []

interface = Tk()
interface.wm_title("Markowitz Optimization")
interface.geometry("320x500")
myFont1 = font.Font(family='Times', size = 20, weight = 'bold')
myFont2 = font.Font(family ='Times', size = 15, weight = 'bold')

quanLab = Label(interface, text = "Type in the indexes in the portfolio:")
quanLab.grid(row = 0, column = 0, columnspan = 3)
quanLab['font'] = myFont1

stockEntry = Entry(interface)
stockEntry.grid(row = 2, column = 0, columnspan = 3)
Ents.append(stockEntry)

addBoxButton = Button(interface, text = "Add", height = 1, width = 10, command = createEntries)
addBoxButton.grid(row = 1, column = 0)

deleteBoxButton = Button(interface, text = "Delete", height = 1, width = 10, command = deleteEntries)
deleteBoxButton.grid(row = 1, column = 1)

showButton = Button(interface, text = "Confirm", height = 1, width = 10, command = showEntries)
showButton.grid(row = 1, column = 2)

interface.mainloop()

