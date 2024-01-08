# Forward model to mix chemical concentrations downstream. 


It is an adaptation of Alex Lipp's D8 accumulator code: https://github.com/AlexLipp/FlowAccum.

A setup script is included to produce the digital elevation model and grid of chemicals needed for the forward model. 

Note that I installed gdal 3.7.3, and gmt 6.4.0 in a conda environment. Python version is 3.11.6.

Once you have cloned this github repository you should be able to run the following scripts, which make use of example data:

> ./setup_dem_chem_grids.gmt

> python fwd_model.py


## Benchmarking

The directory "benchmark" contains a simple example of the code for benchmarking. It shows the results for a single channel flowing atop a substrate with concentrations = 1 (arbitrary units, but let's say 1 mg/kg) in all cells part one in which concentration is 10 (mg/kg). The figure below shows the results. 

![Figure_1](https://github.com/garethgroberts/concs_downstream/assets/11752321/6cacd0ca-9546-4766-a3c6-063cc4fb8319)

The files d8_benchmark.asc and concs_benchmark.asc can be used to change flow routing and source concentrations if you wish. Note that after changing concs_benchmark.asc convert the asc into a tiff before running the forward model:

> gdal_translate -of "GTiff" concs_benchmark.asc concs_benchmark.tif

> python fwd_model_benchmark.py

You can compare the results to a manual calcualtion of concentrations downstream if you wish. The forward model being solved is:

$$ d = \frac{1}{Q} \sum^{N}_{i=1} q_i c_i \qquad {\rm where} Q = \sum^{N}_{i=1}q_i$$.

where $` q_i `$ is export rate (or flux) from each cell, in this simple example $q = 1$, and $c$ = source concentrations in each cell. $i$ and $N$ are indices and maximum number of cells in the calculation. 
