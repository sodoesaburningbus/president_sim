### This script runs presidential election simulations
### and outputs interesting statistics
### Christopher Phillips

##### START OPTIONS #####

# Number of simulations to run
nsims = 10000

# Candidate names
nameR = 'Trump'
nameD = 'Biden'

# File with the state election odds
ifile = 'input.default.csv'

# Directory to save the images
sdir = 'images/default'

#####  END OPTIONS #####

### Swap plotting backend
import matplotlib
matplotlib.use('Agg')

### Import modules
import cartopy .crs as ccrs
import cartopy.io.shapereader as creader
import matplotlib.pyplot as pp
import numpy as np

from model import simulator

### Setup and run the simulations
sim = simulator(input_file=ifile, nameR=nameR, nameD=nameD)
sim.run_sim(runs=nsims)

### Compute outcomes
nCA_flips = 0
nTX_flips = 0
for sim_map in sim.data['Map']:
    if (sim_map['California'] == nameR):
        nCA_flips += 1
    if (sim_map['Texas'] == nameD):
        nTX_flips += 1

oddsR = np.sum(np.array(sim.data['President']) == nameR)/len(sim.data['President'])*100.0
oddsD = np.sum(np.array(sim.data['President']) == nameD)/len(sim.data['President'])*100.0
oddsT = np.sum(np.array(sim.data['President']) == 'tie')/len(sim.data['President'])*100.0

# Compute cumulative histograms
countR_hist, edgesR = np.histogram(sim.data['CountR'], bins=40, range=(0,540), density=False)
countD_hist, edgesD = np.histogram(sim.data['CountD'], bins=40, range=(0,540), density=False)
centersR = (edgesR[1:]+edgesR[:-1])/2.0
centersD = (edgesD[1:]+edgesD[:-1])/2.0
countR_hist = np.cumsum(countR_hist)/np.sum(countR_hist)*100.0
countD_hist = np.cumsum(countD_hist)/np.sum(countD_hist)*100.0

### print some stuff
print(f'Number of simulations: {nsims}')
print(f'Overall Winner: {sim.data["Overall"]}')
print(f'CA Flips: {nCA_flips}')
print(f'TX Flips: {nTX_flips}')

### Make some plots

# Bar chart with overall result chances
fig, ax = pp.subplots(figsize=(9, 6.5))
ax.bar([1, 2, 3], [oddsR, oddsD, oddsT], color=['darkred', 'darkblue', 'purple'])
ax.set_xlim(0, 4)
ax.set_xticks([1,2,3])
ax.set_xticklabels([nameR, nameD, 'Tie'])
ax.set_ylabel('Victory Odds (%)', fontsize=14, fontweight='roman')
ax.set_xlabel('Result', fontsize=14, fontweight='roman')
ax.set_title('Overall Result', fontsize=14, fontweight='roman')

for i, odds in enumerate([oddsR, oddsD, oddsT]):
    ax.text(i+1, odds+0.5, f'{odds:.02f} %', color='black', fontsize=12, ha='center', va='bottom')

pp.savefig(f'{sdir}/overall_odds.png')
pp.close()

# Histograms of electoral vote distributions
fig, (ax1, ax2) = pp.subplots(figsize=(6.5, 9), nrows=2)

# First histogram
ax1.bar(centersR, countR_hist, color='darkred', width=12)
ax1.set_ylabel('Frequency (%)', fontsize=14, fontweight='roman')
ax1.set_title('Cumulative Electoral Vote Distribution\n', fontsize=14, fontweight='roman')
ax1.set_title(nameR, loc='left', ha='left', fontsize=14, fontweight='roman')
ax1.set_xlim(0, 540)
ax1.set_ylim(0, 100)
ax1.axvline(270, linestyle='--', linewidth=2.0, color='black')
ax1.text(268, 90, '270', ha='right', va='center', color='black', fontsize=12)

# Second histogram
ax2.bar(centersD, countD_hist, color='darkblue', width=12)
ax2.set_ylabel('Frequency (%)', fontsize=14, fontweight='roman')
ax2.set_xlabel('Electoral Votes', fontsize=14, fontweight='roman')
ax2.set_xlim(0, 540)
ax2.set_ylim(0, 100)
ax2.axvline(270, linestyle='--', linewidth=2.0, color='black')
ax2.text(268, 90, '270', ha='right', va='center', color='black', fontsize=12)
ax2.set_title(nameD, loc='left', ha='left', fontsize=14, fontweight='roman')

pp.savefig(f'{sdir}/electoral_vote_histogram.png')
pp.close()

### Create the Modal Map of the election

# Tally victories for each state
countsR = {}
countsD = {}
for emap in sim.data['Map']:
    for k in sorted(emap.keys()):
        try:
            countsR[k] = 0
            countsD[k] = 0
        except:
            pass
        
        if (emap[k] == nameR):
            countsR[k] += 1
        else:
            countsD[k] += 1

# Make the map
# Create plotting objects
fig, ax = pp.subplots(subplot_kw={'projection': ccrs.LambertConformal()}, figsize=(9,6.5))
ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

# Pull in the state shapefile
shapename = 'admin_1_states_provinces_lakes'
states_shp = creader.natural_earth(resolution='110m',
                                     category='cultural', name=shapename)

# Set figure decorations
#ax.background_patch.set_visible(False)
#ax.outline_patch.set_visible(False)
ax.set_title('State Outcomes')

# Loop over the states
for state in creader.Reader(states_shp).records():  

    name = state.__dict__['attributes']['gn_name']

    # simple scheme to assign color to each state
    if (countsR[name] > countsD[name]):
        facecolor = 'darkred'
    elif (countsD[name] > countsR[name]):
        facecolor = 'darkblue'
    else:
        facecolor = 'purple'

    # Add the state to the map
    ax.add_geometries([state.geometry], ccrs.PlateCarree(),
                      facecolor=facecolor, edgecolor='black')

pp.savefig(f'{sdir}/modal_electoral_map.png')