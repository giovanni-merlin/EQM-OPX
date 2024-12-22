"""
macros for standard sequences used in OPX.
This is a wrapper of the qua library.
version 2.0
"""

from qm.qua import *
from quam.components import BasicQuAM, SingleChannel
from quam.components.pulses import SquarePulse
import warnings

def long_pulse(operation, element, time, slices=10, **kwargs):
    """
    Generate a long constant pulse by repeating the same pulse a specified number of times.

    Inputs: 
    operation (str): The constant operation to be played.
    element (str): The element on which the operation is played.
    time (int): The total time of the operation (in ns?)
    slices
    kwargs: keyword arguments to pass to the play function
    """
    iteration = declare(int, value=0)
    if time != slices * round(time/slices/4)*4:
        warnings.warn(f"The played time: {slices*round(time/slices/4)*4} is different from the desired time: {time}. This might be due to roundoff of clock cycles, try to change the number of slices.")
    with for_(iteration, 0, iteration < slices, iteration+1):
        play(operation, element, duration=round(time/slices/4), **kwargs)

# TODO
# for the moment we need to have a distinct function to do amplitude modulation.
# in principle the best would be to have a single one
def long_pulse_amp_mod(operation, element, time, amp_mod, slices=10, **kwargs):
    """
    Generate a long constant pulse by repeating the same pulse a specified number of times.

    Inputs: 
    operation (str): The constant operation to be played.
    element (str): The element on which the operation is played.
    time (int): The total time of the operation (in ns?)
    slices
    amp_mod: QUA variable for the real-time correction factor to the pulse amplitude. 
            To be used with input streams from the contrl computer (QUA variable of type fixed)
    kwargs: keyword arguments to pass to the play function
    """
    iteration = declare(int, value=0)
    with if_((amp_mod>2) | (amp_mod<-2)):
        warnings.warn(f"The amplitude modulation factor {amp_mod} is not in [-2,2].")
    if time != slices * round(time/slices/4)*4:
        warnings.warn(f"The played time: {slices*round(time/slices/4)*4} is different from the desired time: {time}. This might be due to roundoff of clock cycles, try to change the number of slices.")
    with for_(iteration, 0, iteration < slices, iteration+1):
        play(operation*amp(amp_mod), element, duration=round(time/slices/4), **kwargs)

def long_ramp(operation, element, time, step_duration=40):
    """
    Generate a ramp of any length. 
    It works by discretizing in small parts (40ns) a constant pulse. The amp functions accepts as arguments only qua variables in [-2,2]
    Inputs: 
    operation (object): the operation linked to the constant pulse which is being discretized. 
    element: the element played (str)
    time: the duration of the ramp in seconds (float)
    step_duration: the duration of the discretization steps in seconds (float). Default is 40ns. At the moment we cannot go below 36 ns of step duration.
    """
    n_steps = round(time/step_duration)
    x = declare(fixed, value=0)
    with for_(x, 0, x < 1, x+1/n_steps):
        play(operation*amp(x), element)


def stroboscopic(operations, element, periods, delay=0,  **kwargs):
    """
    Function to generate the stroboscopic sequence.
    Inputs: 
    operations: ORDERED tuple with the high and low operation to play (tuple of str)
    element: the element played (str)
    periods: the number of periods to play (int)
    delay: the delay time in s to apply to the beginning of the sequence. 
        Important: this is only to be used for the repumper/cooler, for which the low pulse is 
        the second in the tuple (float)
    """
    iteration = declare(int, value=0)
    if delay == 0:
        with for_(iteration, 0, iteration < periods, iteration+1):
            play(operations[0], element, **kwargs)
            play(operations[1], element,  **kwargs)
    elif delay != 0:
        with for_(iteration, 0, iteration < periods, iteration+1):
            play(operations[1], element, duration=round(delay*1e9/4),  **kwargs)
            play(operations[0], element, **kwargs)
            play(operations[1], element, **kwargs)

# TODO
# for the moment we need to have a distinct function to do amplitude modulation.
# in principle the best would be to have a single one
def stroboscopic_amp_mod(operations, element, periods, amp_mod, delay=0, **kwargs):
    """
    Function to generate the stroboscopic sequence.
    Inputs: 
    operations: ORDERED tuple with the high and low operation to play (tuple of str)
    element: the element played (str)
    periods: the number of periods to play (int)
    delay: the delay time in s to apply to the beginning of the sequence. 
        Important: this is only to be used for the repumper/cooler, for which the low pulse is 
        the second in the tuple (float)
    amp_mod: QUA variable for the real-time correction factor to the pulse amplitude. 
            To be used with input streams from the contrl computer (QUA variable of type fixed)
    kwargs: keyword arguments to pass to the play function
    """
    iteration = declare(int, value=0)
    with if_((amp_mod>2) | (amp_mod<-2)):
        warnings.warn(f"The amplitude modulation factor {amp_mod} is not in [-2,2].")
    if delay == 0:
            with for_(iteration, 0, iteration < periods, iteration+1):
                play(operations[0]*amp(amp_mod), element, **kwargs)
                play(operations[1], element,  **kwargs)
    elif delay != 0:
        with for_(iteration, 0, iteration < periods, iteration+1):
            play(operations[1], element, duration=round(delay*1e9/4),  **kwargs)
            play(operations[0]*amp(amp_mod), element, **kwargs)
            play(operations[1], element, **kwargs)