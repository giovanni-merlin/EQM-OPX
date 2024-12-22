# this is a script to define the configuration of the OPX machines
# for the tweezer, cooler and repumper lasers

#import numpy as np
from OPX_strobosequence_QUA_program_collision_imaging import *

# time is in ns by default
# voltage is in Volts by default


config_dict = {
    'version': 1,

    'controllers': {

        'con1': {
            'type': 'opx1',
            'analog_outputs': {
                1 : {'offset': 0, 'delay': 0},
                2 : {'offset': 0, 'delay': 0},
                3 : {'offset': 0, 'delay': 0},
                4 : {'offset': 0.0, 'delay': 0},
                5 : {'offset': 0.0, 'delay': 0},
                6 : {'offset': 0.0, 'delay': 0},
                7 : {'offset': 0.0, 'delay': 0},
                8 : {'offset': 0.0, 'delay': 0},
                9 : {'offset': 0.0, 'delay': 0},
                10 : {'offset': 0.0, 'delay': 0}
            },
            'digital_outputs': {
                1 : {},
                2 : {},
                3 : {},
                4 : {},
                5 : {},
                6 : {},
                7 : {},
                8 : {},
                9 : {},
                10 : {}
                
            },
            'analog_inputs': { # remember to declare just the pysical ports, otherwise gives a job state error
                1: {'offset': 0.0},
                2: {'offset': 0.0}
            }
        }
    },

    'elements': {

        'AOM_repump': {
            'operations': { # should try to define the operation as a COMBINATION of the pulses, but idk how at the moment
                'repump_high_collision': 'repump_high_pulse_coll',
                'repump_high_imaging': 'repump_high_pulse_imag',
                'repump_low': 'repump_low_pulse',
            },
            'singleInput': {
                 'port': ('con1', 3)
            },
            #'intermediate_frequency': 100e6, #200e6,
        },
        'AOM_cool': {
            'operations': {
                'cool_high_collision': 'cool_high_pulse_coll',
                'cool_high_imaging': 'cool_high_pulse_imag',
                'cool_low': 'cool_low_pulse',
            },
            'singleInput': {
                 'port': ('con1', 2)
            },
            #'intermediate_frequency': 100e6, #200e6,
        },
        'AOM_tweez': {
            'operations': {
                'tweez_plateau': 'plateau_pulse',
                'tweez_high_collision': 'tweez_high_pulse_coll',
                'tweez_high_imaging': 'tweez_high_pulse_imag',
                'tweez_low': 'tweez_low_pulse',
                'tweez_step': 'step_pulse'
            },
            'singleInput': {
                 'port': ('con1', 1)
            },
            #'digitalInputs': {
            #    'output_switch': {
            #        'port': ('con1', 10),
            #        'delay': 0,
            #        'buffer': 0,
            #    }
            #},
            'intermediate_frequency': 100e6# 89.181e6,
        },
    },

    'pulses': {
        # collision pulses
        'repump_high_pulse_coll': {
            'operation': 'control',
            'length': round(high_duration_rc*1e9/4)*4, #ns
            'waveforms': {
                'single': 'repump_const_wf_coll'
            },       
        },
        'cool_high_pulse_coll': {
            'operation': 'control',
            'length': round(high_duration_rc*1e9/4)*4, #ns
            'waveforms': {
                'single': 'cool_const_wf_coll'
            },       
        },
        'tweez_high_pulse_coll': {
            'operation': 'control',
            'length': round(high_duration_tweezer*1e9/4)*4, #ns
            'waveforms': {
                'single': 'tweez_const_wf_coll'
            },       
        },
        # imaging pulses
        'repump_high_pulse_imag': {
            'operation': 'control',
            'length': round(high_duration_rc*1e9/4)*4, #ns
            'waveforms': {
                'single': 'repump_const_wf_imag'
            },       
        },
        'cool_high_pulse_imag': {
            'operation': 'control',
            'length': round(high_duration_rc*1e9/4)*4, #ns
            'waveforms': {
                'single': 'cool_const_wf_imag'
            },       
        },
        'tweez_high_pulse_imag': {
            'operation': 'control',
            'length': round(high_duration_tweezer*1e9/4)*4, #ns
            'waveforms': {
                'single': 'tweez_const_wf_imag'
            },       
        },
        # low pulses
        'repump_low_pulse': {
            'operation': 'control',
            'length': round(low_duration_rc*1e9/4)*4, #ns
            'waveforms': {
                'single': 'zero_wf'
            },       
        },
        'cool_low_pulse': {
            'operation': 'control',
            'length': round(low_duration_rc*1e9/4)*4, #ns
            'waveforms': {
                'single': 'zero_wf'
            },       
        },
        'tweez_low_pulse': {
            'operation': 'control',
            'length': round(low_duration_tweezer*1e9/4)*4, #ns
            'waveforms': {
                'single': 'zero_wf'
            },       
        },
        'plateau_pulse': {
            'operation': 'control',
            'length': plateau_intermediate_duration*1e9, #ns
            'waveforms': {
                'single': 'plateau_wf'
            },       
        },
        'step_pulse': {
            'operation': 'control',
            'length': step_duration*1e9, #ns
            'waveforms': {
                'single': 'step_wf'
            },       
        #'digital_marker': 'trigger' 
        },
    },

    'waveforms': {
        'repump_const_wf_coll': {
            'type': 'constant',
            'sample': repumper_square_amplitude_coll # Volts
        },
        'cool_const_wf_coll': {
            'type': 'constant',
            'sample': cooler_square_amplitude_coll # Volts
        },
        'tweez_const_wf_coll': {
            'type': 'constant',
            'sample': tweezer_square_amplitude_coll # Volts
        },
        'repump_const_wf_imag': {
            'type': 'constant',
            'sample': repumper_square_amplitude_imag # Volts
        },
        'cool_const_wf_imag': {
            'type': 'constant',
            'sample': cooler_square_amplitude_imag # Volts
        },
        'tweez_const_wf_imag': {
            'type': 'constant',
            'sample': tweezer_square_amplitude_imag # Volts
        },
        'zero_wf': {
            'type': 'constant',
            'sample': 0.0 # Volts
        },
        'plateau_wf': {
            'type': 'constant',
            'sample': plateau_amplitude # Volts
        },
        'step_wf': { # NB: this waveform will be modified in amplitude in real time by QUA to generate the discrete ramp
            'type': 'constant',
            'sample': ramp_amplitude, # Volts
        },
    },

    #'digital_waveforms': {
    #    'trigger': {
    #        'samples': [(1, 100)] 
    #    }
    #},
}