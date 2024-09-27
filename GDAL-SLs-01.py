# Libraries
import os
import subprocess
import re

# Path to DEM file
DEM = r"DEMs/dem_01.tif"

# Path to shapefile
SHP = r"SHPs/basins_01.shp"

# Activate conda environment with GDAL installed

# Initiate Anaconda prompt
CMD_0 = r"C:/Users/Juan/anaconda3/Scripts/activate.bat"

# Activate the environment
CMD_1 = f"{CMD_0} && conda activate gdal"

# List of basins ID
Bs = [
"B-01", "B-02", "B-03", "B-04", "B-05", "B-06",
"B-07","B-08", "B-09", "B-10", "B-11", "B-12",
"B-13", "B-14", "B-15", "B-16", "B-17", "B-18", "B-19"
]

# Empty dictionary to store outputs
DICT_SLs = {}

# Iterate over each basin
for B in Bs:

    print(f"{B}:")
    
    print("- Clipping DEM.")
            
    # Path to output file
    OUT_1 = os.path.join('Output', f'DEM_{B}.tif')
    
    # Generate the command to clip
    CMD_2 = f"{CMD_1} && gdalwarp -overwrite -of GTiff -cutline {SHP} -cwhere \"ID_1='{B}'\" -dstnodata -9999 -crop_to_cutline {DEM} {OUT_1}"
    
    # Execute the command
    subprocess.run(CMD_2, stdout=subprocess.DEVNULL)

    # Calculate slopes from clipped DEM

    print(f"- Calculating slope.")
    
    # Path to output file
    OUT_2 = os.path.join('Output', f'SL_{B}.tif')

    # Generate the command to calculate slope
    CMD_3 = f"{CMD_1} && gdaldem slope {OUT_1} {OUT_2} -of GTiff -b 1 -s 1.0 -p"

    # Execute the command
    subprocess.run(CMD_3, stdout=subprocess.DEVNULL)

    # Read slope file and compute statistics over it.
    print(f"- Analysing slope file.")
    
    # Path to output file
    OUT_3 = os.path.join('Output', f'SL_{B}.txt')
    
    # Generate the command to calculate statistics
    CMD_4 = f"{CMD_1} && gdalinfo -stats {OUT_2} > {OUT_3}"
    
    # Execute the command
    subprocess.run(CMD_4, stdout=subprocess.DEVNULL)

    # Open txt file and extract mean slope
    with open(OUT_3, 'r') as file:
        
        TXT = file.read()

    # Regular expression to find the value of STATISTICS_MEAN
    SL_1 = re.findall(r"STATISTICS_MEAN=([\d.]+)", TXT)

    SL_2 = float(SL_1[0])
    
    print(f"- Mean slope: {SL_2:.2f} %\n")

    # Store value in dictionary
    DICT_SLs[f"{B}"] = SL_2

# Write dicitionary to a txt file

with open(os.path.join("Output", "SLs.txt"), 'w') as F:
    
    F.write(str(DICT_SLs))
    print("Created SLs.txt containing the mean slope of each basin.")