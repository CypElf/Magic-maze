from time import time

def invert_hourglass(start_time, timeout):
    """
    Returns a new start time corresponding from which the time elapsed has been inverted according to the timout.
    """
    now = time()
    return now - (timeout * 60 + start_time - now) - 1

def is_time_elapsed(start_time, timeout):
    """
    Returns True if the time has elapsed, and False otherwise.
    """
    return timeout * 60 + start_time - time() <= 0