import csv
import itertools
import datetime
import numpy as np

class RuntimeMan:
    def __init__(self, startDate, startTime):
        self.startDateTime = datetime.datetime.combine(startDate, startTime)

    def getRuntime(self, currentDate, currentTime):
        return (datetime.datetime.combine(currentDate, currentTime) - self.startDateTime).total_seconds()

class DataDict:
    def __init__(self, isGrowthLog=True):
        self.isGrowthLog = isGrowthLog
        if isGrowthLog:
            self.allDataDict = {"Event #":[], "Time [sec}":[], "Timestamp Date":[], "Timestamp Time":[], "Event Description":[], "P1 (626)":[], "P2 (627)":[],
                "A1 (925)":[], "A2 (275)":[], "A3 (974)":[], "Command Valve":[], "E1 V_APCVD":[], "E2 V_APFine":[], "E3 V_VentFine":[], "E4 V_VentRough":[],
                "E5 V_APRough":[], "E6 V_TubeFlange":[], "E7 V_Angle":[], "E8 V_Poppet":[], "E9 V_Flow":[],
                "L1: Ar/O2":[], "L1: Flow":[], "L1: Vent":[], "L1: Run":[],
                "L2: CO2":[], "L2: Flow":[], "L2: Vent":[], "L2: Run":[],
                "L3: N2":[], "L3: Flow":[], "L3: Vent":[], "L3: Run":[],
                "L4: Air":[], "L4: Flow":[], "L4: Vent":[], "L4: Run":[],
                "R1: CH4 (low)":[], "R1: Flow":[], "R1: Vent":[], "R1: Run":[],
                "R2: CH4 (high)":[], "R2: Flow":[], "R2: Vent":[], "R2: Run":[],
                "R3: H2":[],"R3: Flow":[], "R3: Vent":[], "R3: Run":[],
                "R4: Ar":[], "R4: Flow":[], "R4: Vent":[], "R4: Run":[],
                "Effective Temperature Oven":[], "Operative Setpoint Oven":[], "PID Power Oven":[]}
        else:
            self.allDataDict = {"Date":[], "Time":[], "Operation":[], "P1 (626)":[], "P2 (627)":[], "A1 (925)":[], "A2 (275)":[], "A3 (974)":[],
                "Command Valve":[], "E1 V_APCVD":[], "E2 V_APFine":[], "E3 V_VentFine":[], "E4 V_VentRough":[], "E5 V_APRough":[],
                "E6 V_TubeFlange":[], "E7 V_Angle":[], "E8 V_Poppet":[], "E9 V_Flow":[],
                "L1: Ar/O2":[], "L1: Setpoint":[], "L1: Vent":[], "L1: Run":[],
                "L2: CO2":[], "L2: Setpoint":[], "L2: Vent":[], "L2: Run":[],
                "L3: N2":[], "L3: Setpoint":[], "L3: Vent":[], "L3: Run":[],
                "L4: Air":[], "L4: Setpoint":[], "L4: Vent":[], "L4: Run":[],
                "R1: CH4 (low)":[], "R1: Setpoint":[], "R1: Vent":[], "R1: Run":[],
                "R2: CH4 (high)":[], "R2: Setpoint":[], "R2: Vent":[], "R2: Run":[],
                "R3: H2":[], "R3: Setpoint":[], "R3: Vent":[], "R3: Run":[],
                "R4: Ar":[], "R4: Setpoint":[], "R4: Vent":[], "R4: Run":[],
                "Effective Temperature Oven":[], "Operative Setpoint Oven":[], "PID Power Oven":[], "Oven lid lock":[], "runtime":[]}

    def timestampDateMut(self):
        return self.allDataDict["Timestamp Date" if self.isGrowthLog else "Date"]
    def timestampTimeMut(self):
        return self.allDataDict["Timestamp Time" if self.isGrowthLog else "Time"]


    def convertDate(self, dateConverter):
        self.allDataDict["Timestamp Date" if self.isGrowthLog else "Date"] = list(map(dateConverter, self.allDataDict["Timestamp Date" if self.isGrowthLog else "Date"]))

    def convertTime(self, timeConverter):
        self.allDataDict["Timestamp Time" if self.isGrowthLog else "Time"] = list(map(timeConverter, self.allDataDict["Timestamp Time" if self.isGrowthLog else "Time"]))

    def processPressure(self):
        #######################################################################
        # generate masked numpy array for A3
        # turn this particular array to a numpy ndarray, with the None values converted to numpy.NaN (otherwise it tries to make the dtype Object, which will lead to problems down the road)
        self.allDataDict["A3 (974)"] = np.fromiter(map(lambda val : (np.NaN if val is None else float(val)), self.allDataDict["A3 (974)"]), dtype=float)

        # mask the NaN values; this is where we would mask values that are too far off (which we consider to be erroneous) to distinguish between no data collected (NaN) and bad value (masked).
        # TODO: identify the range outside of which we should consider values erroneous, mask outside that range (can replace np.isnan with an appropriate lambda
        self.allDataDict["A3 (974)"] = np.ma.masked_where(np.isnan(self.allDataDict["A3 (974)"]), self.allDataDict["A3 (974)"])

    def processTemp(self):
        #######################################################################
        # generate masked numpy array for temperature
        # first, check whether there has been any record of temperature
        if len(self.allDataDict["Effective Temperature Oven"]) == 0 :
            # in the case that there is no record, just make an ndarray with all NaN of the same length as the Date, which is the number of rows in the csv file
            self.allDataDict["Effective Temperature Oven"] = np.full(len(self.allDataDict["Event #"]), np.NaN)
        else:
            # in the case that there are some values, read the ones that are float, but convert the missing values (None) or "Oven OFF" values to NaN
            # TODO: handle all non-float values; handle errors in float conversion, set these to NaN
            self.allDataDict["Effective Temperature Oven"] = np.fromiter(map(lambda val : (np.NaN if (val is None) or (val == "Oven OFF") else float(val)), self.allDataDict["Effective Temperature Oven"]), dtype=float)

        # mask all NaN values
        self.allDataDict["Effective Temperature Oven"] = np.ma.masked_where(np.isnan(self.allDataDict["Effective Temperature Oven"]), self.allDataDict["Effective Temperature Oven"])

    def makeRuntime(self, RuntimeMan):
        # calculate the runtime, which will be the x-axis
        # first, initialize a runtime manager and tell it when the program started logging so it can calculate the times:
        runtimeMan = RuntimeMan(self.timestampDateMut()[0], self.timestampTimeMut()[0])
        self.allDataDict["runtime"] = np.fromiter(map(runtimeMan.getRuntime, self.timestampDateMut(), self.timestampTimeMut()), dtype=int)

    def appendData(self, key, value):
        self.allDataDict[key].append(value)

    def getAllData(self):
        return self.allDataDict





def open_logfile(filename):
    """
    Opens a logfile of a given filename.
    Returns an iterator which gives dicts that map heading to value, with a value of None if not found.
    Assumes 8 lines before the data starts.
    
    Parameters:
        filename (String) : the path to the logfile to open

    Returns:
        csv.DictReader : the DictReader with data starting from line 10
    """
    # open the file in question
    file = open(filename)

    # skip 8 lines, which are typically defining units used in the log.
    # here is an example of those 8 lines:

        # CVD Control Log
        # ***********
        # [pressure] = torr
        # [setpoint] = sccm
        # [commandValve] = deg
        # [E9 V_Flow] = V
        # Everything else is boolean.
        # ***********

    for i in range(8):
        file.readline()

    # now that the lines have been skipped, create the DictReader in question
    return csv.DictReader(file)

def dictReaderWrapper(f, fieldnames=None, restkey=None, restval=None, dialect='excel', *args, **kwds):
    """
    A wrapper around csv.DictReader that just skips the first 8 lines, as above.
    f is an open file (iterable).
    See csv library documentation for details.
    """
    for i in range(8):
        f.readline()

    # now that the lines have been skipped, create the DictReader in question
    return csv.DictReader(f, fieldnames, restkey, restval, dialect, *args, **kwds)

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
    # FIXME compute runtime using an object that is instantiated with a start time
    return (datetime.datetime.combine(date,time)-datetime.datetime.combine(date,datetime.time.min)).total_seconds()
    


def processToBigDict(dictReader, dateConverter=processDate, timeConverter=processTime, RuntimeMan=RuntimeMan, isGrowthLog=True):
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

    # for ControlLogs
    #allDataDict = {"Date":[], "Time":[], "Operation":[], "P1 (626)":[], "P2 (627)":[], "A1 (925)":[], "A2 (275)":[], "A3 (974)":[], "Command Valve":[], "E1 V_APCVD":[], "E2 V_APFine":[], "E3 V_VentFine":[], "E4 V_VentRough":[], "E5 V_APRough":[], "E6 V_TubeFlange":[], "E7 V_Angle":[], "E8 V_Poppet":[], "E9 V_Flow":[], "L1: Ar/O2":[], "L1: Setpoint":[], "L1: Vent":[], "L1: Run":[], "L2: CO2":[], "L2: Setpoint":[], "L2: Vent":[], "L2: Run":[], "L3: N2":[], "L3: Setpoint":[], "L3: Vent":[], "L3: Run":[], "L4: Air":[], "L4: Setpoint":[], "L4: Vent":[], "L4: Run":[], "R1: CH4 (low)":[], "R1: Setpoint":[], "R1: Vent":[], "R1: Run":[], "R2: CH4 (high)":[], "R2: Setpoint":[], "R2: Vent":[], "R2: Run":[], "R3: H2":[], "R3: Setpoint":[], "R3: Vent":[], "R3: Run":[], "R4: Ar":[], "R4: Setpoint":[], "R4: Vent":[], "R4: Run":[], "Effective Temperature Oven":[], "Operative Setpoint Oven":[], "PID Power Oven":[], "Oven lid lock":[], "runtime":[]}
    
    # for GrowthLogs
    #allDataDict = {"Event #":[], "Time [sec}":[], "Timestamp Date":[], "Timestamp Time":[], "Event Description":[], "P1 (626)":[], "P2 (627)":[], "A1 (925)":[], "A2 (275)":[], "A3 (974)":[], "Command Valve":[], "E1 V_APCVD":[], "E2 V_APFine":[], "E3 V_VentFine":[], "E4 V_VentRough":[], "E5 V_APRough":[], "E6 V_TubeFlange":[], "E7 V_Angle":[], "E8 V_Poppet":[], "E9 V_Flow":[], "L1: Ar/O2":[], "L1: Flow":[], "L1: Vent":[], "L1: Run":[], "L2: CO2":[], "L2: Flow":[], "L2: Vent":[], "L2: Run":[], "L3: N2":[], "L3: Flow":[], "L3: Vent":[], "L3: Run":[], "L4: Air":[], "L4: Flow":[], "L4: Vent":[], "L4: Run":[], "R1: CH4 (low)":[], "R1: Flow":[], "R1: Vent":[], "R1: Run":[], "R2: CH4 (high)":[], "R2: Flow":[], "R2: Vent":[], "R2: Run":[], "R3: H2":[],"R3: Flow":[], "R3: Vent":[], "R3: Run":[], "R4: Ar":[], "R4: Flow":[], "R4: Vent":[], "R4: Run":[], "Effective Temperature Oven":[], "Operative Setpoint Oven":[], "PID Power Oven":[]}
    # go through all rows via dictReader, add those values to the allDataDict
    allDataDictObj = DataDict(isGrowthLog)

    firstRow = next(dictReader)
    for key in firstRow:
        allDataDictObj.appendData(key, firstRow[key])
    for row in dictReader:
        for key in row:
            # for each key in the row, 
            # append the value accessed by that key in the row 
            # to the array accessed by that key in the allDataDict
            #allDataDict[key].append(row[key])
            allDataDictObj.appendData(key, row[key])

    # convert Dates to date format via dateConverter
    #allDataDict["Timestamp Date"] = list(map(dateConverter, allDataDict["Timestamp Date"]))
    #allDataDict["Timestamp Time"] = list(map(timeConverter, allDataDict["Timestamp Time"]))
    allDataDictObj.convertDate(dateConverter)
    allDataDictObj.convertTime(timeConverter)
    #######################################################################
    # generate masked numpy array for A3
    # turn this particular array to a numpy ndarray, with the None values converted to numpy.NaN (otherwise it tries to make the dtype Object, which will lead to problems down the road)
    #allDataDict["A3 (974)"] = np.fromiter(map(lambda val : (np.NaN if val is None else float(val)), allDataDict["A3 (974)"]), dtype=float)

    # mask the NaN values; this is where we would mask values that are too far off (which we consider to be erroneous) to distinguish between no data collected (NaN) and bad value (masked).
    # TODO: identify the range outside of which we should consider values erroneous, mask outside that range (can replace np.isnan with an appropriate lambda
    #allDataDict["A3 (974)"] = np.ma.masked_where(np.isnan(allDataDict["A3 (974)"]), allDataDict["A3 (974)"])

    allDataDictObj.processPressure()
    allDataDictObj.processTemp()
    #######################################################################
    # generate masked numpy array for temperature
    # first, check whether there has been any record of temperature
    #if len(allDataDict["Effective Temperature Oven"]) == 0 :
        # in the case that there is no record, just make an ndarray with all NaN of the same length as the Date, which is the number of rows in the csv file
        #allDataDict["Effective Temperature Oven"] = np.full(len(allDataDict["Event #"]), np.NaN)
    #else:
        # in the case that there are some values, read the ones that are float, but convert the missing values (None) or "Oven OFF" values to NaN
        # TODO: handle all non-float values; handle errors in float conversion, set these to NaN
        #allDataDict["Effective Temperature Oven"] = np.fromiter(map(lambda val : (np.NaN if (val is None) or (val == "Oven OFF") else float(val)), allDataDict["Effective Temperature Oven"]), dtype=float)

    # mask all NaN values
    #allDataDict["Effective Temperature Oven"] = np.ma.masked_where(np.isnan(allDataDict["Effective Temperature Oven"]), allDataDict["Effective Temperature Oven"])

    # calculate the runtime, which will be the x-axis
    # first, initialize a runtime manager and tell it when the program started logging so it can calculate the times:
    #runtimeMan = RuntimeMan(allDataDict["Timestamp Date"][0], allDataDict["Timestamp Time"][0])
    #allDataDict["runtime"] = np.fromiter(map(runtimeMan.getRuntime, allDataDict["Timestamp Date"], allDataDict["Timestamp Time"]), dtype=int)
    allDataDictObj.makeRuntime(RuntimeMan)

    return allDataDictObj.getAllData()
