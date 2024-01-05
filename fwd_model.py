"""
An example of how to use the D8Accumulator class to calculate drainage area and 
extract channel networks from a D8 flow direction raster. Alex Lipp Jan 2024. 

Minor modifications in this script [1] generate D8 grid from topography grid 
(esrii asc format). [2] concentrations of material (e.g. chemicals)
are calculated as they are transported downstream. Gareth Roberts Jan 2024. 
"""

import numpy as np
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
from d8_accumulator import D8Accumulator, write_geotiff, write_geojson
import imageio.v2
from landlab.io.esri_ascii import write_esri_ascii

# optional block to generate D8 grid from digital elevation model
# Load a DEM
import toolkit as tk

mg = tk.load_topo("./topo.asc")

# make and write (optiona) D8 raster to output file
d8 = tk.receivers_to_d8(mg.at_node["flow__receiver_node"], mg )
d8 = tk.convert_to_esri_d8(d8)
mg.add_field("D8", d8, at="node", clobber=True)
d8_flip = mg.node_vector_to_raster(d8, flip_vertically=True)
mg.add_field("D8_flip", d8_flip, at="node", clobber=True)
files = write_esri_ascii("files.asc", mg,  clobber=True)


# Initialize the accumulator
accumulator = D8Accumulator("files_D8_flip.asc")
# Create an array of cell areas
trsfm = accumulator.ds.GetGeoTransform()
dx, dy = trsfm[1], trsfm[5] * -1
cell_area = np.ones(accumulator.arr.shape) * dx * dy
# Calculate drainage area in the base units of the D8 raster
print("Calculating drainage area")
drainage_area = accumulator.accumulate(weights=cell_area)

# calculate accumulation of chemicals (concentrations)
source_concs = imageio.v2.imread('./chem_data.tif').astype('double')
concs = accumulator.accumulate(weights=source_concs)
concs = concs/drainage_area

threshold = 1e7  # m^2
# Extracting channel segments from the drainage area array according to a threshold
print(f"Extracting channel segments with drainage area > {threshold} m^2")
channels = accumulator.get_channel_segments(drainage_area, threshold)

# Write the results to file
write_geotiff("drainage_area.tif", drainage_area, accumulator.ds)
print(f"Wrote drainage area to drainage_area.tif)")
write_geojson("channels.geojson", channels)
print(f"Wrote channels to channels.geojson")

# Pick a random point in the domain
startx, starty = 175000, 150000
print(f"Finding the channel profile starting at ({startx},{starty})")
# Find the corresponding node ID
start_node = accumulator.coord_to_node(startx, starty)
# Get the profile of the channel starting at this node
profile, distance = accumulator.get_profile(start_node)
area_on_profile = drainage_area.flatten()[profile]
concs_on_profile = concs.flatten()[profile]
profile_coords = [accumulator.node_to_coord(node) for node in profile]

print("Visualizing results")
plt.figure(figsize=(12, 10))
plt.subplot(2, 2, 1)
plt.imshow(drainage_area, norm=LogNorm(), extent=accumulator.extent, cmap="Greys")
cb = plt.colorbar()
cb.set_label("Drainage area ($m^2$)")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.title("Drainage area ($m^2$)")

plt.subplot(2, 2, 2)
plt.imshow(concs, norm=LogNorm(), extent=accumulator.extent, cmap="viridis")
cb = plt.colorbar()
cb.set_label("Concentration, mg/kg")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
for channel in channels.coordinates:
    x, y = zip(*channel)
    plt.plot(x, y, c="black")
plt.title(f"Channels with drainage area > {threshold} $m^2$")

plt.subplot(2, 2, 3)
#plt.imshow(drainage_area, norm=LogNorm(), extent=accumulator.extent, cmap="Greys")
plt.imshow(concs, norm=LogNorm(), extent=accumulator.extent, cmap="viridis")
cb = plt.colorbar()
cb.set_label("Concentration, mg/kg)")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.plot(
    [x for x, _ in profile_coords],
    [y for _, y in profile_coords],
    "k-",
    label="Channel profile",
)
plt.plot([startx], [starty], "ko", label="Start point")
plt.legend()
plt.title("Channel profile (planform)")

plt.subplot(2, 2, 4)
#plt.plot(distance, area_on_profile, "k-")
plt.plot(distance, concs_on_profile, "k-")
plt.xlabel("Distance from mouth (m)")
#plt.ylabel("Drainage area ($m^2$)")
plt.ylabel("Concentrations, mg/kg")

# Set the y and x limits to be the min max of the profile
plt.xlim(min(distance), max(distance))
plt.ylim(min(concs_on_profile), max(concs_on_profile))
plt.title("Channel profile (vertical)")

plt.tight_layout()
plt.show()
