#Forward model to mixed chemical concentrations downstream. 


It is an adaptation of Alex Lipp's D8 accumulator code: https://github.com/AlexLipp/FlowAccum.

A setup script is included to produce the digital elevation model and grid of chemicals needed for the forward model. 

Note that I installed gdal 3.7.3, and gmt 6.4.0 in a conda environment. Python version is 3.11.6.

Once you have cloned this github repository you should be able to run the following scripts:

> ./setup_dem_chem_grids.gmt

> python fwd_model.py
