# Parameters optimization with MLOOP

This directory contains scripts for the automatic optimization of the experimental parameters controlled by OPX using the MLOOP package (see https://m-loop.readthedocs.io/en/stable/api/mloop.html).

MLOOP is a framework for handling several kind of optimization algorithms, such as differential evolution (DE), gaussian processes and simple neural networks.
The goal of the optimization can be multiple, and depends on the cost function which is provided. The most straightforward is to maximize atom preparation in tweezers: this is the one implemented.
The notebooks are divided accrding to the parameters chosen for optimization: 
- "amp" for repumper/cooler power (during imaging)
- "det" for repumper/cooler detuning (during imaging)
- "delay" for repumper/cooler delay time in the stroboscopic pulse 
and the possible combinations.

To run the optimization, first modify the "exp_config.txt" file, specifying the optimization parameters.
Then run both the OPX notebook and the "read_image_mloop" notebook, which reads the images produced by the experiment and produce a file named "exp_output.txt". Then run MLOOP from the command line: move to the directory in which the scripts are running and type "m-loop".
Make sure that no previous file named "exp_input.txt" is present in the directory, otherwise it will not trigger the detectino ofa newly created one.