#!/usr/bin/env python

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import plotter
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from mathmanipulation import *
import gc

class FileEntry:
    """
    A single FileEntry object keeps a reference to
    the text and button related to the file entry,
    and remembers the name of the file in question.
    """
    def __init__(self, label, button, filename):
        self.label = label
        self.button = button
        self.filename = filename

        # FileEntries will be nodes in a doubly-linked list
        self.nextNode = None
        self.prevNode = None

    def getFilename(self):
        return self.filename

    def destroy(self):
        self.label.destroy()
        self.button.destroy()



class FileEntryMan:
    """
    A manager class that holds all FileEntry objects.
    Holds a doulby-linked list of FileEntries,
    can traverse this list to return a python list of file name strings,
    can allow for deletion of a particular FileEntry by reference
    """

    def __init__(self):
        self.head = None
        self.currentIndex = 0

    def addFileEntry(self, fileEntry):
        # stick the new FileEntry after the head
        fileEntry.nextNode = self.head

        # if the head is a FileEntry, its prevNode must be updated
        if self.head is not None:
            self.head.prevNode = fileEntry

        # set the head to be the new fileEntry
        self.head = fileEntry
        self.currentIndex += 1

    def fileNames(self):
        filenames = []
        currentNode = self.head
        while currentNode is not None:
            filenames.append(currentNode.getFilename())
            currentNode = currentNode.nextNode
        return filenames

    def removeFileEntry(self, fileEntry):
        if fileEntry is self.head:
            #print("fileEntry is self.head")
            self.head = self.head.nextNode
            if self.head is not None:
                self.head.prevNode = None
        else:
            if fileEntry.nextNode is not None:
                fileEntry.nextNode.prevNode = fileEntry.prevNode
            fileEntry.prevNode.nextNode = fileEntry.nextNode
        fileEntry.destroy()
        del fileEntry

root = Tk()
root.title("Logfile Analysis")
root.geometry("800x500")

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

files = FileEntryMan()

# eventually, the below will be a srcollable list of files to load
canvas_container=Canvas(mainframe, height=100)
frame2=Frame(canvas_container)
verticalScroll=Scrollbar(mainframe,orient="vertical",command=canvas_container.yview) # will be visible if the frame2 is to to big for the canvas
hoizontalScroll=Scrollbar(mainframe,orient="horizontal",command=canvas_container.xview) # will be visible if the frame2 is to to big for the canvas
canvas_container.create_window((0,0),window=frame2,anchor='nw')
frame2.grid(column=0, row=0, sticky=(N, W, E, S))

def plotToCanvas():
    figure, lines = plotter.plotPressureAndTemp(files.fileNames())
    num_files = len(lines)
    sliders = []
    plt.subplots_adjust(bottom=0.13*num_files+0.1)
    for index, key in enumerate(lines):
        sliderAxis = plt.axes([0.45, 0.1 + 0.13*index, 0.45, 0.03])
        slider = Slider(ax=sliderAxis, label=key, valmin=-1000, valmax=1000, valinit=0)
        tempLam = translateAndUpdateLambda(lines[key], figure)
        slider.on_changed(tempLam)
        sliders.append(slider)
    plt.show()

def translateAndUpdate(lines, value, figure):
    for line in lines:
        line.transformY(translateLambdaGenerator(value))
    figure.canvas.draw_idle()
    #print (lines)

def translateAndUpdateLambda(lines, figure):
    return lambda value: translateAndUpdate(lines, value, figure)

def addFile():
    filename = filedialog.askopenfilename()
    if type(filename) is not str or filename == '':
        return

    label = ttk.Label(frame2, text=filename)
    label.grid(column=0, row=files.currentIndex)

    button = ttk.Button(frame2, text="-")
    button.grid(column=1, row=files.currentIndex)

    fileEntry = FileEntry(label, button, filename)
    button.bind("<Button-1>", lambda event: removeFile(fileEntry))

    files.addFileEntry(fileEntry)
    canvas_container.configure(yscrollcommand=verticalScroll.set, scrollregion="0 0 0 %s" % frame2.winfo_height()) # the scrollregion mustbe the size of the frame inside it,
                                                                                                            #in this case "x=0 y=0 width=0 height=frame2height"
                                                                                                            #width 0 because we only scroll verticaly so don't mind about the width.
    frame2.update()
    plotToCanvas()

def removeFile(fileEntry):
    fileEntry.label.destroy()
    files.removeFileEntry(fileEntry)
    gc.collect()
    frame2.update()
    plotToCanvas()

ttk.Label(mainframe, text="Files:").grid(column=0, row=0, sticky="E")
ttk.Button(mainframe, text="+", command=addFile).grid(column=1, row=0, sticky="E")
canvas_container.grid(column=0, row=1, columnspan=2)

root.mainloop()
