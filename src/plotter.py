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

def runtimeCalculator(date, time):
    return (datetime.datetime.combine(date,time)-datetime.datetime.combine(date,datetime.time.min)).total_seconds()
    

def processToBigDict(dictReader, dateConverter=processDate, timeConverter=processTime, runtimeCalculator=runtimeCalculator):
    """
    Makes a dictionary of {key : data} where data is an ordered list, out of a csv.DictReader.
    This is meant to conform to the pyplot signature of:
    >> pyplot.plot('time', 'pressure', processToBigDict(reader))

    adds a runtime value, which is an integer ndarray, representing the time in the run (accounts for time of day, etc) so that it is easy to plot.
    """
    # TODO: what if one of the values is None? ANSWER: it should be masked. To mask, seems like you need to make an ndarray with NaN for the None values
    # TODO: what if the process runs through midnight?
    # TODO: take function parameters for calculation of date, time, and runtime
    # TODO: make masked arrays for all values, where None is masked

    allDataDict = {"Date":[], "Time":[], "Operation":[], "P1 (626)":[], "P2 (627)":[], "A1 (925)":[], "A2 (275)":[], "A3 (974)":[], "Command Valve":[], "E1 V_APCVD":[], "E2 V_APFine":[], "E3 V_VentFine":[], "E4 V_VentRough":[], "E5 V_APRough":[], "E6 V_TubeFlange":[], "E7 V_Angle":[], "E8 V_Poppet":[], "E9 V_Flow":[], "L1: Ar/O2":[], "L1: Setpoint":[], "L1: Vent":[], "L1: Run":[], "L2: CO2":[], "L2: Setpoint":[], "L2: Vent":[], "L2: Run":[], "L3: N2":[], "L3: Setpoint":[], "L3: Vent":[], "L3: Run":[], "L4: Air":[], "L4: Setpoint":[], "L4: Vent":[], "L4: Run":[], "R1: CH4 (low)":[], "R1: Setpoint":[], "R1: Vent":[], "R1: Run":[], "R2: CH4 (high)":[], "R2: Setpoint":[], "R2: Vent":[], "R2: Run":[], "R3: H2":[], "R3: Setpoint":[], "R3: Vent":[], "R3: Run":[], "R4: Ar":[], "R4: Setpoint":[], "R4: Vent":[], "R4: Run":[], "Effective Temperature Oven":[], "Operative Setpoint Oven":[], "PID Power Oven":[], "Oven lid lock":[], "runtime":[]}

    # go through all rows via dictReader, add those values to the allDataDict
    for row in dictReader:
        for key in row:
            # for each key in the row, 
            # append the value accessed by that key in the row 
            # to the array accessed by that key in the allDataDict
            allDataDict[key].append(row[key])

    # convert Dates to date format via dateConverter
    allDataDict["Date"] = list(map(dateConverter, allDataDict["Date"]))
    allDataDict["Time"] = list(map(timeConverter, allDataDict["Time"]))

    #######################################################################
    # generate masked numpy array for A3
    # turn this particular array to a numpy ndarray, with the None values converted to numpy.NaN (otherwise it tries to make the dtype Object, which will lead to problems down the road)
    allDataDict["A3 (974)"] = np.fromiter(map(lambda val : (np.NaN if val is None else float(val)), allDataDict["A3 (974)"]), dtype=float)

    # mask the NaN values; this is where we would mask values that are too far off (which we consider to be erroneous) to distinguish between no data collected (NaN) and bad value (masked).
    # TODO: identify the range outside of which we should consider values erroneous, mask outside that range (can replace np.isnan with an appropriate lambda
    allDataDict["A3 (974)"] = np.ma.masked_where(np.isnan(allDataDict["A3 (974)"]), allDataDict["A3 (974)"])

    #######################################################################
    # generate masked numpy array for temperature
    # first, check whether there has been any record of temperature
    if len(allDataDict["Effective Temperature Oven"]) == 0 :
        # in the case that there is no record, just make an ndarray with all NaN of the same length as the Date, which is the number of rows in the csv file
        allDataDict["Effective Temperature Oven"] = np.full(len(allDataDict["Date"]), np.NaN)
    else:
        # in the case that there are some values, read the ones that are float, but convert the missing values (None) or "Oven OFF" values to NaN
        # TODO: handle all non-float values; handle errors in float conversion, set these to NaN
        allDataDict["Effective Temperature Oven"] = np.fromiter(map(lambda val : (np.NaN if (val is None) or (val == "Oven OFF") else float(val)), allDataDict["Effective Temperature Oven"]), dtype=float)

    # mask all NaN values. TODO: mask non-NaN values that we consider out of range or something else
    allDataDict["Effective Temperature Oven"] = np.ma.masked_where(np.isnan(allDataDict["Effective Temperature Oven"]), allDataDict["Effective Temperature Oven"])

    # calculate the runtime, which will be the x-axis
    allDataDict["runtime"] = np.fromiter(map(runtimeCalculator, allDataDict["Date"], allDataDict["Time"]), dtype=int)

    return allDataDict

def plotLog(filenames):
    for filename in filenames:
        with open(filename) as file:
            plt.plot("runtime", "A3 (974)", data=processToBigDict(logmanipulator.dictReaderWrapper(file)), label=filename)
    plt.legend()
    plt.show()

def plotPressureAndTemp(filenames):
    fig, pressure = plt.subplots()
    temperature = pressure.twinx()
    for filename in filenames:
        with open(filename) as file:
            fileDict = processToBigDict(logmanipulator.dictReaderWrapper(file))
            pressure.plot("runtime", "A3 (974)", data=fileDict, label=filename)
            temperature.plot("runtime", "Effective Temperature Oven", data=fileDict, label=filename)

    plt.legend()
    plt.show()

