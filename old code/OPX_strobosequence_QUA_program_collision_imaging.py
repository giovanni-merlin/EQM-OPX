# script with the QUA program to run the tweezer, cooler and repumper sequences
# this must contain the definition of the variables that we want to control
# which are then read by the OPX_strobosequence_config.py file

from qm.qua import *
from qm import QuantumMachinesManager, SimulationConfig
from QUA_utilities import *

# unless stated otherwise, all times are in seconds
# and all voltages are in Volts

# whether to run the program in simulation mode or not
Simulation = False

    ###################
    # THE QUA PROGRAM #
    ###################

with program() as program:

    with infinite_loop_():
        #wait_for_trigger('AOM_repump')
        wait_for_trigger('AOM_cool')
        wait_for_trigger('AOM_tweez')

        ############################
        # TWEEZER LOADING SEQUENCE #
        ############################

        ramp_amplitude = 0.15
        ramp_duration = 100e-6
        step_duration = 40e-9
        n_steps = round(ramp_duration / step_duration)
        plateau_amplitude = ramp_amplitude
        plateau_duration = 100e-6 # for signals longer than ~67ms (maximum duration of a pulse) should be a multiple of plateau_intermediate_duration
        plateau_intermediate_duration = 10e-6 # prone to bug: this must be an integer of plateau_duration
        plateau_num_portions = round(plateau_duration / plateau_intermediate_duration) # return an integer    

        long_ramp('tweez_step', 'AOM_tweez', ramp_duration, step_duration=40e-9)
        long_pulse('tweez_plateau', 'AOM_tweez', periods=plateau_num_portions)
        align('AOM_repump', 'AOM_cool', 'AOM_tweez')

        ######################
        # COLLISION SEQUENCE #
        ######################

        collision_sequence_duration = 100e-6 # s
        repumper_square_amplitude_coll = 0.3
        cooler_square_amplitude_coll = 0.3
        tweezer_square_amplitude_coll = 0.15
        square_frequency = 1.75e6 # Hz
        square_period = 1/square_frequency
        duty_cycle_tweezer = 0.4 # high fraction for tweezer
        duty_cycle_rc = 0.3 # high fraction for repumper and cooler
        delay_fraction_rc = 0.1 # delay for repumper and cooler (fraction of period)  
                            # the sum of the repumper/cooler duty cycles must be less than 1
        delay_time_rc = 1/square_frequency*delay_fraction_rc # s
        high_duration_tweezer = 1/square_frequency*duty_cycle_tweezer #s 
        low_duration_tweezer = 1/square_frequency*(1-duty_cycle_tweezer) # s
        high_duration_rc = 1/square_frequency*duty_cycle_rc # s
        low_duration_rc = square_period-delay_time_rc-high_duration_rc # s, computed as the remaining part of the period
        number_of_periods_collision = round(collision_sequence_duration/square_period) # return an integer
        gap_duration = 100e-6 # s

        if low_duration_rc < 16e-9:
            raise ValueError("Low pulse is too short (or negative). Check the repumper/cooler duty cycle and delay: the sum must be less than 1")

        ## here we have an intrinsic delay of 35 ns
        #stroboscopic(('repump_high_collision','repump_low'), 'AOM_repump', number_of_periods_collision, delay=delay_time_rc)
        stroboscopic(('cool_high_collision','cool_low'), 'AOM_cool', number_of_periods_collision, delay=delay_time_rc)
        stroboscopic(('tweez_low','tweez_high_collision'), 'AOM_tweez', number_of_periods_collision)

        # gap
        play('tweez_high_imaging', 'AOM_tweez', duration=round(gap_duration*1e9/4))
        #play('repump_low', 'AOM_repump', duration=round(gap_duration*1e9/4))
        play('cool_low', 'AOM_cool', duration=round(gap_duration*1e9/4))

        ####################
        # IMAGING SEQUENCE # 
        ####################
        # NB: the stroboscopic frequency and modulation is the same as for the collision sequence at the moment

        imaging_sequence_duration = 100e-3#6 # s
        repumper_square_amplitude_imag = 0.15
        cooler_square_amplitude_imag = 0.3
        tweezer_square_amplitude_imag = 0.15
        number_of_periods_imaging = round(imaging_sequence_duration/square_period) # return an integer
        
        #stroboscopic(('repump_high_imaging','repump_low'), 'AOM_repump', number_of_periods_imaging, delay=delay_time_rc)
        stroboscopic(('cool_high_imaging','cool_low'), 'AOM_cool', number_of_periods_imaging, delay=delay_time_rc)
        stroboscopic(('tweez_low','tweez_high_imaging'), 'AOM_tweez', number_of_periods_imaging)

        #wait(int(1e9/4), 'AOM_tweez', 'AOM_cool')

if __name__ == "__main__":
    # here we need the config dictionary
    from OPX_strobosequence_config_collision_imaging import config_dict

    # for debugging
    print(f"\n Number of steps for the tweezer ramp: {n_steps}, each of {step_duration*1e9} ns")
    print(f"Number of plateau portions: {plateau_num_portions}")
    print("Number of collision periods:", number_of_periods_collision)
    print("Number of imaging periods:", number_of_periods_imaging, "\n")
    print(f"Low duration for tweezer: {round(low_duration_tweezer*1e9/4)*4}ns") # these are exactly the values passed to the configuration
    print(f"High duration for tweezer: {round(high_duration_tweezer*1e9/4)*4}ns")
    print(f"Total: {round(low_duration_tweezer*1e9/4)*4 + round(high_duration_tweezer*1e9/4)*4}ns \n")
    print(f"Delay duration for repumper/cooler: {round(delay_time_rc*1e9/4)*4}ns")
    print(f"High duration for repumper/cooler: {round(high_duration_rc*1e9/4)*4}ns")
    print(f"Low duration for repumper/cooler: {round(low_duration_rc*1e9/4)*4}ns")
    print(f"Total: {round(delay_time_rc*1e9/4)*4 + round(low_duration_rc*1e9/4)*4 + round(high_duration_rc*1e9/4)*4}ns \n")

    # open the qm
    ip_address = '130.79.148.167'
    qmm = QuantumMachinesManager(host=ip_address)

    if Simulation == True:
        #simulate_sequence(qmm, config_dict, program, duration=500e-6)

        start_time = time.time()
        simulated_job = qmm.simulate(config_dict, program, SimulationConfig(duration=int(1000*1e3/4)))
        end_time = time.time()
        print(f"Simulation time: {end_time - start_time} s")

        # get DAC and digital samples
        samples = simulated_job.get_simulated_samples()
        plt.figure()
        plt.plot(samples.con1.analog["1"], "-")
        plt.plot(samples.con1.analog["2"], "-")
        plt.plot(samples.con1.analog["3"], "--")
        #plt.plot(samples.con1.digital["10"], "-")
        plt.legend(("tweezer", "cooler", "repumper"))#,"trigger"))
        plt.xlabel("Time [ns]")
        plt.ylabel("Signal [V]")        
        plt.show()
    else:
        qm = qmm.open_qm(config_dict)
        job = qm.execute(program)
        job.halt()