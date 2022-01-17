import csv
import itertools

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

