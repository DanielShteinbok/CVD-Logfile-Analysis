import matplotlib.pyplot as plt
import numpy as np
import datetime
import logmanipulator
from mathmanipulation import *

def plotLog(filenames, **kwargs):
    plt.yscale("log")
    for filename in filenames:
        with open(filename, encoding="iso-8859-1") as file:
            plt.plot("runtime", "A3 (974)", data=logmanipulator.processToBigDict(logmanipulator.dictReaderWrapper(file)), label=filename, **kwargs)
    plt.ylabel("Pressure, Torr")
    plt.legend()
    plt.show()

def plotPressureAndTemp(filenames, figsize=(10, 5), areGrowthLogs=True, **kwargs):
    lines = {}
    fig, pressure = plt.subplots()
    fig.set_figwidth(figsize[0])
    fig.set_figheight(figsize[1])
    temperature = pressure.twinx()
    for filename in filenames:
        with open(filename, encoding="iso-8859-1") as file:
            fileDict = logmanipulator.processToBigDict(logmanipulator.dictReaderWrapper(file), isGrowthLog=areGrowthLogs)
            pressureLine, = pressure.plot("runtime", "A3 (974)", data=fileDict, label=filename + ", Pressure", **kwargs, linestyle='-')
            pressure.set_yscale("log")
            pressure.set_ylabel("Pressure, Torr")
            temperatureLine, = temperature.plot("runtime", "Effective Temperature Oven", data=fileDict, label=filename + ", Temperature", **kwargs, linestyle=':')
            temperature.set_ylabel("Temperature, Celsuis")
            lines[filename] = (Transformer(pressureLine), Transformer(temperatureLine))

    pressure.legend(loc="lower left")
    temperature.legend(loc="lower right")
    return fig, lines
