# Forward model to mix chemical concentrations downstream. 

The code in this repository can be used to calculate the concentrations of things (e.g. chemicals) as they are transported downstream in a directed network (e.g. a river). It makes use of Alex Lipp's D8 accumulator code: https://github.com/AlexLipp/FlowAccum. The things being transported are assumed to be well mixed and conservative (e.g. no decay, transformation, etc.). See Lipp et al. ([2020](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020JF005700), [2021](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021GC009838)) for examples of the forward model (also discussed with respect to benchmarking below).  

A setup script is included to produce the digital elevation model and grid of chemicals needed for the forward model. 

Note that I installed gdal 3.7.3, and gmt 6.4.0 in a conda environment, my python version is 3.11.6.

Once you have cloned (> git clone https://github.com/garethgroberts/concs_downstream.git) this repository you should be able to run the following scripts, which make use of example data:

> ./setup_dem_chem_grids.gmt

> python fwd_model.py

In this simple example source concentrations are assumed to be have an arbitrary Gaussian distribution. You can replace `chem_data.asc' with your own geochemical data. There is an example for converting a text file into a suitable grid file in setup_dem_chem_grids.gmt.


## Benchmarking

The directory "benchmark" contains a simple example for benchmarking. It shows results for a single channel flowing atop a substrate with concentrations = 1 (arbitrary units, but let's say 1 mg/kg) in all cells part one in which concentration is 10 (mg/kg). The figure below shows the results. 

![Figure_1](https://github.com/garethgroberts/concs_downstream/assets/11752321/6cacd0ca-9546-4766-a3c6-063cc4fb8319)

Top left panel shows the drainage area (essentially a grid of flow accumulation) generated from the d8_benchmark.asc file. Top right panel shows the source concentrations and the drainage network. Bottom left panel shows the planform of the river along which concentrations downstream are sought, and calculated concentrations (coloured grid). Bottom right shows source and downstream concentrations along the river shown in bottom left panel. 

The files d8_benchmark.asc and concs_benchmark.asc can be used to change flow routing and source concentrations if you wish. Notes: [1] Flow directions follow the Esri scheme, i.e. flow from a cell to adjacent cardinal and intercardinal cells, going clockwise from 90 degrees (east), have values 1, 2, 4, 8, 16, 32, 64, 128. [2] after changing concs_benchmark.asc convert the asc-file into a tiff before running the forward model, I use: 

> gdal_translate -of "GTiff" concs_benchmark.asc concs_benchmark.tif

and to run the forward model: 

> python fwd_model_benchmark.py

You can compare the results to a manual calcualtion of concentrations downstream, $d$, if you wish. The forward model being solved is:
```math
d = \frac{1}{Q} \sum^{N}_{i=1} q_i c_i \qquad {\rm where} \qquad Q = \sum^{N}_{i=1}q_i.
```
where $` q_i `$ is export rate (or flux) from each cell, in this simple example $q = 1$, and $c$ = source concentrations in each cell. $i$ and $N$ are indices and maximum number of cells in the calculation. 
