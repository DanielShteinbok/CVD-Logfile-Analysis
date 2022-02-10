#!/usr/bin/env python

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import plotter
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import pyplot as plt
#import functools

#files = ["../csv-samples/20220128_13-44-01_DS007_LargeGrains.csv",
#        "../csv-samples/20220131_12-16-00_DS008_LargeGrains.csv",
#        "../csv-samples/20220127_12-31-06_DS005_LargeGrain.csv",
#        ]
#plotter.plotPressureAndTemp(files)
#plt.ion()

root = Tk()
root.title("Logfile Analysis")

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

files = []
gui_rows = []

canvas_container=Canvas(mainframe, height=100)
frame2=Frame(canvas_container)
verticalScroll=Scrollbar(mainframe,orient="vertical",command=canvas_container.yview) # will be visible if the frame2 is to to big for the canvas
hoizontalScroll=Scrollbar(mainframe,orient="horizontal",command=canvas_container.xview) # will be visible if the frame2 is to to big for the canvas
canvas_container.create_window((0,0),window=frame2,anchor='nw')
frame2.grid(column=0, row=0, sticky=(N, W, E, S))

def plotToCanvas():
    #canvas = FigureCanvasTkAgg(plotter.plotPressureAndTemp(files), master=root)
    #canvas.draw()
    #canvas.get_tk_widget().grid(column=2, row=1)
    #return canvas
    figure = plotter.plotPressureAndTemp(files)
    plt.show()

def addFile():
    filename = filedialog.askopenfilename()
    files.append(filename)

    gui_row = []
    label = ttk.Label(frame2, text=filename)
    label.grid(column=0, row=len(files)-1)

    button = ttk.Button(frame2, text="-")
    button.grid(column=1, row=len(files)-1)
    button.bind("<Button-1>", lambda event: removeFile(button))

    gui_row.append(label)
    gui_row.append(button)
    gui_rows.append(gui_row)

    frame2.update()
    plotToCanvas()

def removeFile(button):
    index = button.grid_info()["row"]
    print(index)
    files.pop(index)
    for element in gui_rows[index]:
        element.destroy()
    gui_rows.pop(index)

    frame2.update()
    plotToCanvas()

ttk.Label(mainframe, text="Files:").grid(column=0, row=0)
ttk.Button(mainframe, text="+", command=addFile).grid(column=1, row=0)
canvas_container.grid(column=0, row=1)
verticalScroll.grid(column=1, row=1)
#ttk.Label(mainframe, text="Some more text").grid(column=2, row=0)
#plotToCanvas()

#filename = filedialog.askopenfilename()
#figure = plotter.plotPressureAndTemp([filename])

#canvas = FigureCanvasTkAgg(figure, master=root)
#plt.show()
root.mainloop()
