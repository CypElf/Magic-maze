"""
This module handles all the time related things.
"""
from time import time

def invert_hourglass(start_time, timeout):
    """
    Return a new start time corresponding from which the time elapsed has been inverted according to the timout.
    """
    now = time()
    return now - (timeout * 60 + start_time - now) - 1

def get_timer(start_time, timeout):
    """
    Return True if the time has elapsed, and False otherwise.
    """
    return timeout * 60 + start_time - time()

def adjust_time(start_time, current_time):
    """
    Return a new time corresponding to the current time minus the saved time to restore the timer to a previous state.
    """
    return start_time + (time() - current_time)