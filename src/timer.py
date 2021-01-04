"""
This module handles all the time related things.
"""
import src.game_state as gs
from time import time

def invert_hourglass():
    """
    Return a new start time corresponding from which the time elapsed has been inverted according to the timout.
    """
    now = time()
    return now - (gs.timeout * 60 + gs.start_time - now) - 1

def get_timer():
    """
    Return True if the time has elapsed, and False otherwise.
    """
    return gs.timeout * 60 + gs.start_time - time()

def adjust_time(previous_start_time, save_time, offset = 0):
    """
    Restore the game state start_time variable to a previous state, to restore the time elapsed since this previous time. If you see an offset between the saved timer and restored one, you can add as many seconds as you want to the restored timer with the offset parameter. Defaults to 0.
    """
    gs.start_time = previous_start_time + (time() - save_time) + offset