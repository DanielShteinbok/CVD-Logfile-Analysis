import matplotlib.pyplot as plt
import numpy as np
import datetime
import logmanipulator

def processDate(dateString):
    """
    produces datetime.date object from a provided dateString

    Parameters:
        dateString (String) : the slash-delimited date, e.g. 24/08/2021 to represent Aug 24, 2021
    Returns:
        date (datetime.date)
    """
    day, month, year = map(int, dateString.split('/'))
    return datetime.date(year, month, day)

def processTime(timeString):
    """
    produces datetime.timedelta object from a provided timeString
    it seems that the recorded time in the logfiles is actually time from starting, not absolute time in the day. Therefore, timedelta is more appropriate

    Parameters:
        timeString (String) : the colon-delimited time delta, e.g. 00:04:53 to represent 0 hours, 4 minutes, 53 seconds
    Returns:
        time (datetime.timedelta)
    """
    hours, minutes, seconds = map(int, timeString.split(':'))
    return datetime.time(hour=hours, minute=minutes, second=seconds)

def plotLog(filenames, **kwargs):
    plt.yscale("log")
    for filename in filenames:
        with open(filename, encoding="iso-8859-1") as file:
            plt.plot("runtime", "A3 (974)", data=logmanipulator.processToBigDict(logmanipulator.dictReaderWrapper(file)), label=filename, **kwargs)
    plt.ylabel("Pressure, Torr")
    plt.legend()
    plt.show()

def plotPressureAndTemp(filenames, figsize=(10, 5), **kwargs):
    fig, pressure = plt.subplots()
    fig.set_figwidth(figsize[0])
    fig.set_figheight(figsize[1])
    temperature = pressure.twinx()
    for filename in filenames:
        with open(filename, encoding="iso-8859-1") as file:
            fileDict = logmanipulator.processToBigDict(logmanipulator.dictReaderWrapper(file))
            pressure.plot("runtime", "A3 (974)", data=fileDict, label=filename + ", Pressure", **kwargs, linestyle='-')
            pressure.set_yscale("log")
            pressure.set_ylabel("Pressure, Torr")
            temperature.plot("runtime", "Effective Temperature Oven", data=fileDict, label=filename + ", Temperature", **kwargs, linestyle=':')
            temperature.set_ylabel("Temperature, Celsuis")

    pressure.legend(loc="lower left")
    temperature.legend(loc="lower right")
    plt.show()

