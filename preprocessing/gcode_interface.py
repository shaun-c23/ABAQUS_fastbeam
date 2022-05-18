# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 10:29:15 2022

@author: Shaun
"""

'''both this file and 'G1_code_fastbeam_with_int' need to be in the same folder
   -> gcode_interface.py is used to update path, gcode files and get final results
   -> G1_code_fastbeam_with_int is the library to get this data. Do not modify this 
      file unless you know whatever it is that needs to be fixed
   -> contact Shaun Cooke if any issues that you cant resolve (src@student.ubc.ca)'''

'''add path to files if necessary:
    Spyder->tools-> PYTHONPATH manager -> add path to folderwhere these files are'''

from G1_code_fastbeam_with_int import get_laser_coords
from G1_code_fastbeam_with_int import laser_pos

'''Gcode Summary'''
'''
GCODE COMMANDS FOR THIS CODE ARE ABSOLUTE, NOT INCREMENTAL 
(always uses global coords, not relative to previous position)

G0 - rapid traverse (moving while not printing)
G1 - linear feed (printing along straight line from X0 Y0 Z0 to X1 Y1 Z1)
F after G1 - feed rate in mm/min
G4 - dwell time
F after G4 - time to stay at previous position in seconds
G94 - Required everytime feed rate is set/changed with G1 **appears only on first G1 command**
M37 - laser on
M38 - laser off
S2 - laser power
'''

#path_gcode can be in .txt, .csv, or .gcode format
#please use the same gcode formatting and commands as that in "fastbeam_gcode.txt"
path_gcode = "C:\\Users\\Shaun\\Documents\\ABAQUS_FILES\\fastbeam\\fastbeam_gcode.txt"
path_folder = "C:\\Users\\Shaun\\Documents\\ABAQUS_FILES\\fastbeam\\"

'''ideally, laser travels no more than one element per timestep'''
'''also, want more timesteps in the laser file than in abaqus so its always (more or less) moving'''
timestep = 0.0001
elsize = 0.05 #from Abaqus model

travspeed_init = '10000' #in/min
linspeed_init = 'F0' #initial set to 0 -> gcode will update
circspeed_init = 'F0' #initial set to 0 -> gcode will update

gcode_coords,linspeed,travspeed = get_laser_coords(path_gcode,travspeed_init,linspeed_init,circspeed_init)

start_line = 1 #line to start reading gcode_coords at

laser_position = laser_pos(timestep, elsize,gcode_coords,start_line,linspeed,travspeed)

laser_position.to_csv(path_folder+"laser_pos.txt",index = False, header = None)


len(laser_position)


t0 = laser_position['t'][4]
t1 = laser_position['t'][5]

y0 =  laser_position['x'][4]
y1 =  laser_position['x'][5]

t = 0.0042

y = y0 + (t-t0) * (y1-y0)/(t1-t0)





























