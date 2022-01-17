import matplotlib.pyplot as plt
import numpy as np

def processToBigDict(dictReader, dateConverter, timeConverter, runtimeCalculator):
    """
    Makes a dictionary of {key : data} where data is an ordered list, out of a csv.DictReader.
    This is meant to conform to the pyplot signature of:
    >> pyplot.plot('time', 'pressure', processToBigDict(reader))

    adds a runtime value, which is an integer, representing the time in the run (accounts for time of day, etc).
    """
    # TODO: what if one of the values is None?
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
    #allDataDict["Date"] = map(dateConverter, allDataDict["Date"])
    #allDataDict["Time"] = map(timeConverter, allDataDict["Time"])

    # generate masked numpy array for A3
    allDataDict["A3 (974)"] = np.fromiter(map(lambda val : (np.NaN if val is None else float(val)), allDataDict["A3 (974)"]), dtype=float)
    allDataDict["A3 (974)"] = np.ma.masked_where(np.isnan(allDataDict["A3 (974)"]), allDataDict["A3 (974)"])


    return allDataDict

