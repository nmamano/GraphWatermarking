"""
auxiliary functions that may be useful for different modules
"""
import datetime

def list_head_to_string(items, max_items=10):
    """
    returns the string representation of a list,
    but only showing the first max_items elements
    """
    res = "["
    for i, item in enumerate(items):
        if i >= max_items:
            break
        if i > 0:
            res += ", "
        res += str(item)
    if len(items) > max_items + 2:
        res += ", ..., " + str(items[-1])
    res += "]"
    if len(items) > max_items + 2:
        res += " (size: "+str(len(items))+")"
    return res

def current_time():
    """ returns current time in format hh:mm:ss """
    time = str(datetime.datetime.now()).split('.')[0]
    return time.split()[1]

def printts(string):
    """ print with timestamp (adds endline at the end) """
    print('(', current_time(), ') ', string, sep='', flush=True)
