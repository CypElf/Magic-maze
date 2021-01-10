"""
This module handles all the time related things.
"""
from time import time

import src.game_state as gs

def invert_timer():
    """
    Invert the timer as an hourglass would, according to the timeout.
    """
    now = time()
    return now - (gs.timeout * 60 + gs.start_time - now) - 1

def get_timer():
    """
    Return True if the time has elapsed, and False otherwise.
    """
    return gs.timeout * 60 + gs.start_time - time()

def adjust_timer(previous_start_time, save_time, offset = 0):
    """
    Restore the start_time to a previous state, to restore the time elapsed since this previous time. You can add bonus seconds to the restored timer with the offset parameter. Defaults to 0.
    """
    gs.start_time = previous_start_time + (time() - save_time) + offset