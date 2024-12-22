"""
this utility contains some macros for standard sequences 
controlled by the OPX

version 0: in the simplest case functions are just shorthand for the operations that we perform in the program
           but do not modify the configuration. This means that you have to write the configuration file 
           beforehand: specify all the necessary variables etc... and be sure to call the right pulses

in version 1 maybe we want to write classes for each operation: the constructor will then add the necessary 
attributes to the configuration dictionary.
"""

from qm.qua import *
from qm import SimulationConfig
from qm import generate_qua_script
import numpy as np
import matplotlib.pyplot as plt
import time

# TODO: might implement some checks, e.g. if the operation or element are present in the config dictionary?

# Long constant pulse
def long_pulse(operation, element, periods):
    """
    Generate a long constant pulse by repeating the same pulse a specified number of times.

    Inputs: 
    operation (str): The constant operation to be played.
    element (str): The element on which the operation is played.
    periods (int): The number of periods to play the operation.

    Returns:
    None
    """
    iteration = declare(int, value=0)
    with for_(iteration, 0, iteration < periods, iteration+1):
        play(operation, element)

# Ramp
def long_ramp(operation, element, duration, step_duration=40e-9):
    """
    Function to generate a ramp of any length. 
    It works by discretizing in small parts (40ns) a constant pulse.
    Inputs: 
    operation: the operation linked to the constant pulse which is being discretized (str). 
    element: the element played (str)
    duration: the duration of the ramp in seconds (float)
    step_duration: the duration of the discretization steps in seconds (float). 
                    Default is 40ns
    Return: 
    None

    At the moment we cannot go below 36 ns of step duration.
    Might be due to the fact that we use a fixed type?
    """
    n_steps = round(duration / step_duration)
    x = declare(fixed, value=0)
    with for_(x, 0, x < 1, x+1/n_steps):
        play(operation*amp(x), element) # amp() accepts numbers between -2 and 2

# Stroboscopic
def stroboscopic(operations, element, periods, delay=0):
    """
    Function to generate the stroboscopic sequence.
    Inputs: 
    operations: ORDERED tuple with the high and low operation to play (tuple of str)
    element: the element played (str)
    periods: the number of periods to play (int)
    delay: the delay time in s to apply to the beginning of the sequence. 
        This is only to be used for the repumper/cooler, for which the low pulse is 
        the second in the tuple. Notice that this will not affect the duration of the subsequent pulses, 
        so make sure that they have the right timing (float)
    
    Return: 
    None
    """
    iteration = declare(int, value=0)
    with for_(iteration, 0, iteration < periods, iteration+1):
        if delay != 0: 
            play(operations[1], element, duration=round(delay*1e9/4))
        play(operations[0], element)
        play(operations[1], element) 


# Simulate and plot
def simulate_sequence(qmm, config_dictionary, program, duration):
    """
    beta version.
    Function to simulate and plot the job.

    Inputs: 
    qmm (qmm instance): a QuantumMachinesmanager instance.
    config_dictionary (dict): the configuration dictionary.
    program: the QUA program.
    duration (float): the duration of the simulation in seconds. 

    Returns:
    None
    """
    start_time = time.time()
    simulated_job = qmm.simulate(config_dictionary, program, SimulationConfig(duration=int(duration*1e9/4)))
    end_time = time.time()
    print(f"Simulation time: {end_time - start_time} s")

    # get DAC and digital samples
    samples = simulated_job.get_simulated_samples()
    plt.figure()
    plt.plot(samples.con1.analog["1"], "-")
    plt.plot(samples.con1.analog["2"], "-")
    plt.plot(samples.con1.analog["3"], "--")
    plt.legend(("tweezer", "cooler", "repumper"))
    plt.xlabel("Time [ns]")
    plt.ylabel("Signal [V]")        
    plt.show()

# generate debug file
def generate_debug_file(filename, config_dictionary):
    """
    filename (str)
    config_dictionary
    """
    sourceFile = open(filename, 'w')
    print(generate_qua_script(program, config_dictionary), file=sourceFile) 
    sourceFile.close()