#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Shaun

"""

import re
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

#---------------------read Gcode----------------------------------------------
#-------laser coordinate function definition to call from anywhere-------------
#make input for units so it converts to m only when needed

def bare_numpy_mat(mat_v, mat_u):
   return np.sqrt(np.sum((mat_v - mat_u) ** 2))

def get_laser_coords(path,travspeed,linspeed,circspeed):
    

    x = []
    y = []
    z = []
    cg = []
    r = []
    i = []
    j = []
    feedy = []
    lON = []
    p=[]
    

    with open(path) as gcode:
        for line in gcode:
            line = line.strip()

            print(line)
            command = re.findall(r'[G].?\d',line)
            feed = re.findall(r'[F].?\d+.\d+',line)
            
            coordx = re.findall(r'[X].?\d+.\d+', line)
            
            if not coordx:
                coordx = re.findall(r'[X]\d+', line)
            
            if not coordx:
                coordx = re.findall(r'[X].\d+', line)
                
            coordy= re.findall(r'[Y].?\d+.\d+', line)
            
            if not coordy:
                coordy = re.findall(r'[Y]\d+', line)
            
            if not coordy:
                coordy = re.findall(r'[Y].\d+', line)
            
            coordz = re.findall(r'[Z].?\d+.\d+', line)
            
            if not coordz:
                coordz = re.findall(r'[Z]\d+', line)
            
            if not coordz:
                coordz = re.findall(r'[Z].\d+', line)
                
            lasON = re.findall(r'[M].?\d',line)
            power = re.findall(r'[S].?\d+.\d+',line)
            #print(power)
            coordR = re.findall(r'[R].?\d+.\d+', line)
            coordI = re.findall(r'[I].?\d+.\d+', line)
            coordJ = re.findall(r'[J].?\d+.\d+', line)
            
            k=0
            e=0
            for loop in command:
                if loop == 'G1' or loop == 'G0' or loop == 'G2' or loop == 'G3':
                    check = True
                    break
                
                else:
                    if loop == 'G94':
                        linspeed = feed[0]   
                    elif loop == 'G95':
                        circspeed = feed[0]
                        
                    check = False
                    k+=1
                e+=1
                
            if command:

                if check == True:
                    cg.append(command[e])
                else:
                    cg.append(command[0])
            else:
                cg.append('G')
            
            if lasON:
                if lasON[0] == 'M37' or lasON[0] == 'M38':
                    lON.append(lasON[0])
                else:
                    lON.append('L')
                    
            else:
                lON.append('L')


            if power:
                p.append(power[0])

            else:
                p.append('P')
            
            if feed:
                feedy.append(feed[0])
            else:
                feedy.append('F')
       
            if coordx:
                x.append(coordx[0])
            else:
                x.append('X')
                
            if coordy:
                y.append(coordy[0])
            else:
                y.append('Y')
                
            if coordR:
                r.append(coordR[0])
            else:
                r.append('R')
                
            if coordI:
                i.append(coordI[0])
            else:
                i.append('I')
                
            if coordJ:
                j.append(coordJ[0])
            else:
                j.append('J')
                
            if coordz:
                z.append(coordz[0])
            else:
                z.append('Z')

    laser_coord = pd.DataFrame(zip(cg,x,y,z,r,i,j,feedy,p,lON),columns = ['command','x','y','z','R','I','J','feed','power','laser switch'])

    laser_coord['x'] = [item.strip('X') for item in laser_coord['x']]
    laser_coord['y'] = [item.strip('Y') for item in laser_coord['y']]
    laser_coord['z'] = [item.strip('Z') for item in laser_coord['z']]
    laser_coord['R'] = [item.strip('R') for item in laser_coord['R']]
    laser_coord['I'] = [item.strip('I') for item in laser_coord['I']]
    laser_coord['J'] = [item.strip('J') for item in laser_coord['J']]
    laser_coord['power'] = [item.strip('S2') for item in laser_coord['power']]
    laser_coord['power'] = [item.strip('=') for item in laser_coord['power']]
    laser_coord['power'] = [item.strip('P') for item in laser_coord['power']]
    laser_coord['laser switch'] = [item.strip('L') for item in laser_coord['laser switch']]
    

    i = 0
    for rowx in laser_coord['x']:
        if not rowx:
            if i == 0:
                laser_coord['x'][i] = 0.0
            else:
                laser_coord['x'][i] = laser_coord['x'][i-1]
        i+=1
        
    j = 0
    for rowy in laser_coord['y']:
        if not rowy:
            if j == 0:
                laser_coord['y'][j] = 0.0
            else:
                laser_coord['y'][j] = laser_coord['y'][j-1]
        j+=1
    
    k = 0
    for rowz in laser_coord['z']:
        if not rowz:
            if k == 0:
                laser_coord['z'][k] = 0.0
            else:
                laser_coord['z'][k] = laser_coord['z'][k-1]
        k+=1
    
    q = 0
    for rowR in laser_coord['R']:
        if not rowR:
            laser_coord['R'][q] = 0.0
        q+=1
        
    laser_coord['R'][5] = 0.0
    
        
    q = 0
    for rowI in laser_coord['I']:
        if not rowI:
            laser_coord['I'][q] = 0.0
        q+=1
    
    q = 0
    for rowJ in laser_coord['J']:
        if not rowJ:
            laser_coord['J'][q] = 0.0
        q+=1
    
    
    laser_coord['laser switch'] = laser_coord['laser switch'].replace('',np.nan).ffill().astype(str)
    
    n=0
    for rows in laser_coord['laser switch']:
        if laser_coord['laser switch'][n] != 'M37':
            n+=1
        else:
            break
        
    for rows in range(0,n) :
        laser_coord['laser switch'][rows] = 0.0
    
    q=0    
    for rowsw in laser_coord['laser switch']:
        
        if rowsw == 'M37':
            laser_coord['laser switch'][q] = 1

        
        if rowsw == 'M38':
            laser_coord['laser switch'][q] = 0
        q+=1

    
    laser_coord['command'] = laser_coord['command'].replace('G',np.nan).ffill().astype(str)
    
    q=0    
    for rowf in laser_coord['command']:
        if laser_coord['command'][q] == 'G4' and laser_coord['feed'][q] == 'F':
            laser_coord['command'][q] = 'G1'
            
        q+=1
    
    q=0
    for rowf in laser_coord['feed']:
        if laser_coord['command'][q] == 'G1' and laser_coord['feed'][q] == 'F':
            laser_coord['feed'][q] = linspeed
        
        if laser_coord['command'][q] == 'G0' and laser_coord['feed'][q] == 'F':
            laser_coord['feed'][q] = travspeed
        
        if laser_coord['command'][q] == 'G2' and laser_coord['feed'][q] == 'F':
            laser_coord['feed'][q] = circspeed
            
        if laser_coord['command'][q] == 'G3' and laser_coord['feed'][q] == 'F':
            laser_coord['feed'][q] = circspeed
            
        q+=1
        
        
    laser_coord['feed'] = [item.strip('F') for item in laser_coord['feed']]

    

    laser_coord['power'] = laser_coord['power'].replace('',np.nan).ffill().astype(str)
    

    laser_coord['x'] = laser_coord['x'].astype(float)
    laser_coord['y'] = laser_coord['y'].astype(float)
    laser_coord['z'] = laser_coord['z'].astype(float)
    laser_coord['R'] = laser_coord['R'].astype(float)
    laser_coord['I'] = laser_coord['I'].astype(float)
    laser_coord['J'] = laser_coord['J'].astype(float)
    laser_coord['laser switch'] = laser_coord['laser switch'].astype(float)
    laser_coord['power'] = laser_coord['power'].astype(float)

    q=0
    for row in laser_coord['feed']:
        if row == '':
            #laser_coord['feed'][q] = 0
            laser_coord.loc[q,'feed']=0
        q+=1
    
    laser_coord['feed'] = laser_coord['feed'].astype(float)
    
    
    
    q=0
    for row in laser_coord['power']:
        #laser_coord['power'][q] = row*laser_coord['laser switch'][q]
        laser_coord.loc[q,'power'] = row*laser_coord['laser switch'][q]
        q+=1
    
    laser_coord['power'] = laser_coord['power'].fillna(0)
    
    del laser_coord['laser switch']
    
    
    travspeed = float(travspeed.strip('F'))/60
    linspeed = float(linspeed.strip('F'))/60
    circspeed = float(circspeed.strip('F'))/60
    
    laser_coord['x'] = laser_coord['x']
    laser_coord['y'] = laser_coord['y']
    laser_coord['z'] = laser_coord['z']
    laser_coord['R'] = laser_coord['R']
    laser_coord['I'] = laser_coord['I']
    laser_coord['J'] = laser_coord['J']
    
    k=0
    for row in laser_coord['command']: #preserve G4 feed as it is in seconds
        if row != 'G4':
            #laser_coord['feed'][k] = laser_coord['feed'][k]/60#*(25.4/60)
            laser_coord.loc[k,'feed'] = laser_coord['feed'][k]/60
        k+=1
        
    return laser_coord, linspeed, travspeed

#gcode_coords = get_laser_coords()
#gcodetest = gcode_coords[74:78]
#gcode_coords = gcodetest


#------------------------Gcode position discretization array-------------------
#chops up g-code command into x-y-z position of laser depending on timestep
#and scanning speed


x = 0
y = 0
import sys

timestep = 0.005 #[s]
elsize = 0.05 #element size [mm]
gcode_coords = []
start_line = 0
# sys

def laser_pos(timestep, elsize,gcode_coords,start_line,linspeed,travspeed):
    global t_step
    t_step = timestep
    time_t = 0

    x=[]
    y=[]
    z=[]
    t=[]
    p=[]

    #check if input speed and timestep are invalid
    timestep_max = elsize/(linspeed)

    if timestep <= timestep_max:
        length_p_inc = timestep*linspeed
        print("Travel length per timestep: " + str(round(length_p_inc,5)) + " [mm]\n\
              Element size = " + str(elsize) + " [mm]")
            
    else:
        print("Error: Specified speed greater than maximum allowable speed at specified timestep.\nDecrease time step to increase maximum speed\n")
        print("max timestep = " + str(timestep_max))


    #start with num
    x.append(gcode_coords['x'][start_line])
    y.append(gcode_coords['y'][start_line])
    z.append(gcode_coords['z'][start_line])
    t.append(0)
    p.append(gcode_coords['power'][start_line])
    
    time_t+= t_step

    for row_gcode in np.arange(start_line+1,len(gcode_coords)): #len(gcode_coords)
        #print(row_gcode)
        #row_gcode = 5
        power = gcode_coords['power'][row_gcode]
        
        
        if gcode_coords['command'][row_gcode] == 'G0':
            
            speed = travspeed
            
            xy = [x[-1],y[-1]]
            #d_i = bare_numpy_mat(xy,gcode_coords.iloc[row_gcode,1:3])
            #gcode_coords[row_gcode]
            d_ix = bare_numpy_mat(float((xy[0])),gcode_coords.iloc[row_gcode,1:2][0])
            d_iy = bare_numpy_mat(float((xy[1])),gcode_coords.iloc[row_gcode,2:3][0])
            
            if round(d_ix,5) != 0:
                theta = math.atan(d_iy/d_ix)
            else:
                theta = math.pi/2
            
            vx = round(speed*math.cos(theta),4)
            vy = round(speed*math.sin(theta),4)
            
            time_1 = t[-1]
            
            if vx!= 0:
                time_2x = t[-1]+ d_ix/vx
            else:
                time_2x = time_1
            
            if vy!= 0:
                time_2y = t[-1]+ d_iy/vy
            else:
                time_2y = time_1
                
            dist_tot = math.sqrt(d_ix**2 + d_iy**2)
            
            tot_time_len = dist_tot/speed
            
            
            num_inc_x = math.ceil((time_2x-time_1)/timestep)
            num_inc_y = math.ceil((time_2y-time_1)/timestep)
            if num_inc_x*t_step > tot_time_len or num_inc_y*t_step > tot_time_len:
                num_inc_x -= 1
                num_inc_y -= 1

            
            if num_inc_x != 0:
                num_inc = num_inc_x
                time_2 = time_2x
            else:
                num_inc = num_inc_y
                time_2 = time_2y


            if num_inc == 0 or (round(d_ix,5)==0 and round(d_iy,5)==0):
                y.append(round(y[-1],4))
                x.append(round(x[-1],4))
                z.append(gcode_coords['z'][row_gcode])
                t.append(t[-1]+timestep)
                p.append(0)
                time_t += t_step
                
            else:
                
                t_step = abs((time_2-time_1)/num_inc)
                
                for row in np.arange(0,num_inc):
                
                
                    if round(y[-1],4) == gcode_coords['y'][row_gcode]:
                        y.append(round(y[-1],4))

                    elif y[-1] < gcode_coords['y'][row_gcode]:
                        
                        y.append(y[-1] + vy*t_step)

                    elif y[-1] > gcode_coords['y'][row_gcode]:
                        y.append(y[-1] - vy*t_step)

                
                    if round(x[-1],4) == gcode_coords['x'][row_gcode]:
                        x.append(round(x[-1],4))

                    elif x[-1] < gcode_coords['x'][row_gcode]:
                        x.append(x[-1] + vx*t_step)
                
                    elif x[-1] > gcode_coords['x'][row_gcode]:
                        x.append(x[-1] - vx*t_step)
                        
                    
                    z.append(gcode_coords['z'][row_gcode])
                    t.append(t[-1]+t_step)
                    p.append(0)
                    time_t += t_step
        
        if gcode_coords['command'][row_gcode] == 'G1':
            
            
            speed = linspeed

            xy = [x[-1],y[-1]]
            #d_i = bare_numpy_mat(xy,gcode_coords.iloc[row_gcode,1:3])
            d_ix = bare_numpy_mat(float(xy[0]),gcode_coords.iloc[row_gcode,1:2][0])
            d_iy = bare_numpy_mat(float(xy[1]),gcode_coords.iloc[row_gcode,2:3][0])
            
            if d_ix != 0:
                theta = math.atan(d_iy/d_ix)
            else:
                theta = math.pi/2
            
            vx = round(speed*math.cos(theta),4)
            vy = round(speed*math.sin(theta),4)
            
            time_1 = t[-1]
            
            if vx!= 0:
                time_2x = t[-1]+ d_ix/vx
            else:
                time_2x = time_1
            
            if vy!= 0:
                time_2y = t[-1]+ d_iy/vy
            else:
                time_2y = time_1
            
            dist_tot = math.sqrt(d_ix**2 + d_iy**2)
            
            tot_time_len = dist_tot/speed
            
            
            num_inc_x = math.ceil((time_2x-time_1)/timestep)
            num_inc_y = math.ceil((time_2y-time_1)/timestep)
         
            if num_inc_x*t_step > tot_time_len or num_inc_y*t_step > tot_time_len:
                num_inc_x -= 1
                num_inc_y -= 1
                
            if num_inc_x > 0:
                num_inc = num_inc_x
                time_2 = time_2x
            else:
                num_inc = num_inc_y
                time_2 = time_2y
            
            #print(num_inc)
            
            if num_inc == 0:
                y.append(round(y[-1],4))
                x.append(round(x[-1],4))
                z.append(gcode_coords['z'][row_gcode])
                t.append(t[-1]+timestep)
                p.append(power)
                time_t += t_step
                
            else:
               
                t_step = abs((time_2-time_1)/num_inc)
                
                for row in np.arange(0,num_inc):
                
                
                    if round(y[-1],4) == gcode_coords['y'][row_gcode]:
                        y.append(round(y[-1],4))

                    elif y[-1] < gcode_coords['y'][row_gcode]:
                        
                        y.append(y[-1] + vy*t_step)

                    elif y[-1] > gcode_coords['y'][row_gcode]:
                        y.append(y[-1] - vy*t_step)

                
                    if round(x[-1],4) == gcode_coords['x'][row_gcode]:
                        x.append(round(x[-1],4))

                    elif x[-1] < gcode_coords['x'][row_gcode]:
                        x.append(x[-1] + vx*t_step)
                
                    elif x[-1] > gcode_coords['x'][row_gcode]:
                        x.append(x[-1] - vx*t_step)
                        
                    z.append(gcode_coords['z'][row_gcode])
                    t.append(t[-1]+t_step)
                    p.append(power)
                    time_t += t_step  
         
        if gcode_coords['command'][row_gcode] == 'G4':

            x.append(x[-1])
            y.append(y[-1])
            z.append(z[-1])
            p.append(gcode_coords['power'][row_gcode])
            t.append(t[-1]+timestep)
            x.append(x[-1])
            y.append(y[-1])
            z.append(z[-1])
            t.append(t[-1] + gcode_coords['feed'][row_gcode]-timestep)
            p.append(gcode_coords['power'][row_gcode])
            time_t += t_step
            if t[-1] == time_t:
                print(t[-1])
        '''
        if 0 < t[-1]-t[-2] < timestep:
            print('command: ' + str(gcode_coords['command'][row_gcode])\
                  + 'x1 :' + str(x[-2]) + ' x2 :' + str(x[-1]))
        '''    
    #plt.plot(x,y)
    #plt.xlabel('X position')
    #plt.ylabel('Y position')
    #print(p[-1])
            
    laser_pos_array = pd.DataFrame(zip(t,x,y,z,p),columns = ['t','x','y','z','p'])
    
    #laser_pos_array['x'] = laser_pos_array['x'] #in to mm
    #laser_pos_array['y'] = laser_pos_array['y']
    #laser_pos_array['z'] = laser_pos_array['z'] #layer height = 0.3mm
    #laser_pos_array['p'] = laser_pos_array['p']

    return laser_pos_array

#time_toprint2 = []

#laser_position = laser_pos(0.001,0.05)

#las_end = laser_position[laser_position['p']>0]

#endtime = las_end['t'].to_numpy()

#time_toprint2.append(endtime[-1])

#if negative:
#laser_position['y'] = -1*laser_position['y']
#laser_position['x'] = -1*laser_position['x']

#laser_position.to_csv("C:\\Users\\Shaun\\Documents\\ABAQUS_FILES\\fastbeam\\laser_pos.txt",index = False, header = None)




