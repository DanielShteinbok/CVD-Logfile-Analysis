#!/usr/bin/env python

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import plotter
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import pyplot as plt
import gc
#import functools

#files = ["../csv-samples/20220128_13-44-01_DS007_LargeGrains.csv",
#        "../csv-samples/20220131_12-16-00_DS008_LargeGrains.csv",
#        "../csv-samples/20220127_12-31-06_DS005_LargeGrain.csv",
#        ]
#plotter.plotPressureAndTemp(files)
#plt.ion()

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
            fileEntry.nextNode.prevNode = fileEntry.prevNode
            fileEntry.prevNode.nextNode = fileEntry.nextNode
        fileEntry.destroy()
        del fileEntry
        self.currentIndex -= 1


root = Tk()
root.title("Logfile Analysis")
root.geometry("800x500")

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

#files = []
#gui_rows = []

files = FileEntryMan()

# eventually, the below will be a scollable list of files to load
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
    #print(files.fileNames())
    figure = plotter.plotPressureAndTemp(files.fileNames())
    plt.show()

def addFile():
    filename = filedialog.askopenfilename()
    #files.append(filename)

    #gui_row = []
    label = ttk.Label(frame2, text=filename)
    label.grid(column=0, row=files.currentIndex)

    button = ttk.Button(frame2, text="-")
    button.grid(column=1, row=files.currentIndex)

    #gui_row.append(label)
    #gui_row.append(button)
    #gui_rows.append(gui_row)

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
    #index = button.grid_info()["row"]
    #print(index)
    #files.pop(index)
    #for element in gui_rows[index]:
        #element.destroy()
    #gui_rows.pop(index)
    #canvas_container.configure(yscrollcommand=verticalScroll.set, scrollregion="0 0 0 %s" % frame2.winfo_height()) # the scrollregion mustbe the size of the frame inside it
    #frame2.update()
    #plotToCanvas()

ttk.Label(mainframe, text="Files:").grid(column=0, row=0)
ttk.Button(mainframe, text="+", command=addFile).grid(column=1, row=0)
canvas_container.grid(column=0, row=1)
#verticalScroll.grid(column=1, row=1)
#ttk.Label(mainframe, text="Some more text").grid(column=2, row=0)
#plotToCanvas()

#filename = filedialog.askopenfilename()
#figure = plotter.plotPressureAndTemp([filename])

#canvas = FigureCanvasTkAgg(figure, master=root)
#plt.show()
root.mainloop()
