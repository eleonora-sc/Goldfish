import os

# find all the probes in Alaska (lists the canada one too, just discard)
os.system('wsl -e sh -c "ripe-atlas probe-search --status 1 --center=61.217,-149.863 --radius 1300 > alaska_probes.txt"') # latlong of anchorage, radius of 1500 km
# os.system('wsl -e sh -c "ripe-atlas probe-search --area anchorage --status 1 > test.txt')