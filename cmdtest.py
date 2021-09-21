import math
from plotnine import *
import pandas
import numpy
import h5py

f = h5py.File('sim3d.out')

plot_pds = []
plot_pds2 = []
dt = f.attrs['dt']

PpositionX = 0;
PpositionY = 0;
PpositionZ = 0;
for key, src in f['srcs'].items():
  position = src.attrs['Position']
  type = src.attrs['Type']
  print('\n')
  print(position)
  print(type)
  print('\n')
  print(position.T[0])
  print(position.T[1])
  print(position.T[2])
  PpositionX = position.T[0]
  PpositionY = position.T[1]
  PpositionZ = position.T[2]
  print('\n')

middle = 3
firstborder = 0.0085
increment = 0.012
DirString = "tmp_" + str((round((PpositionX-firstborder)/increment))-middle) + "_" + str((round((PpositionY-firstborder)/increment))-middle) + "/"
DirString2 = "tmp_" + str((round((PpositionX-firstborder)/increment))-middle) + "_" + str((round((PpositionY-firstborder)/increment))-middle)

for key, rx in f['rxs'].items():
  Ex = [x for x in rx['Ex']]
  Ey = [y/4000 for y in rx['Ey']]
  Ez = [z for z in rx['Ez']]
  #E = [math.sqrt(x*x + y*y) for x,y in zip(Ex, Ey)]
  #E = [math.sqrt(x*x + y*y +z*z)/10000 for x,y,z in zip(Ex, Ey, Ez)]
  E = Ey

  name = rx.attrs['Name']
  position = rx.attrs['Position']

  print(f'rx {name}: {position}')
  #print('\n')
  #print(dir(position))
  #print('\n')
  #print(position.T[0])
  #print(position.T[1])
  #print('\n')

  plot_pd = pandas.DataFrame()
  plot_pd['time'] = [dt*i for i in range(len(E))]
  plot_pd['V'] = E
  plot_pd['rx'] = f'{name}'

  if position.T[0] == PpositionX and position.T[1] == PpositionY: # and position.T[2] == PpositionZ:
  #if position.T[0] == 0.0565 and position.T[2] < 0.057:
    print('\nFound transmitter at ')
    print(position)
    print('ID:')
    print(rx)
    print('\n')
    plot_pds2.append(
      plot_pd
    )
  else:
    plot_pds.append(
      plot_pd
    )
  #plot_pds2.append(
    #plot_pd
  #)

  #
  #FileString = DirString + "utL_" + str(round((position.T[0]-PpositionX)/0.012)) + "_" + str(round((position.T[1]-PpositionY)/0.012))
  #print('\n')
  #print(FileString)
  #print('\n')
  #File = open(FileString,"w")
  #for i in range (4):
    #File.write("header\n")
  #array_length = len(E)
  #array_length = int(array_length / 25)
  #for i in range (array_length):
    #File.write(str(dt*i*25))
    #File.write("\t")
    #File.write(str(E[i*25]))
    #File.write("\n")

  #File.close()
  #

plot_pd = pandas.concat(plot_pds)
plot_pd2 = pandas.concat(plot_pds2)

(
  ggplot(plot_pd[plot_pd['time'] >= 0e-10])
  + aes(x='time',y='V',color='rx',group='rx')
  + geom_line()
  + theme_light()
  + theme(figure_size=(20,10))
).save('interpreted_plot_voltage_' + DirString2 + '.png')

(
  ggplot(plot_pd2[plot_pd2['time'] >= 0e-10])
  + aes(x='time',y='V',color='rx',group='rx')
  + geom_line()
  + theme_light()
  + theme(figure_size=(20,10))
).save('interpreted_plot_voltage2_' + DirString2 + '.png')

f.close()
#toggle this print statement on off to create 2nd image due to python buffer overflow
print('\nfinished\n')
print('\nfinished\n')
print('\nfinished\n')
