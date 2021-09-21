import math
from plotnine import *
import pandas
import numpy
import h5py

f = h5py.File('sim3d.out')

plot_pds = []
plot_pds2 = []
widths = numpy.arange(1,502,10)
dt = f.attrs['dt']

for key, tl in f['tls'].items():
  #Ex = [x for x in tl['Ex']]
  #Ey = [y for y in tl['Ey']]
  #Ez = [z for z in tl['Ez']]
  #E = [math.sqrt(x*x + y*y) for x,y in zip(Ex, Ey)]
  #E = [math.sqrt(x*x + y*y +z*z) for x,y,z in zip(Ex, Ey, Ez)]
  E = [x for x in tl['Vtotal']]
  
  #name = tl.attrs['Name']
  position = tl.attrs['Position']

  #print(f'tl {name}: {position}')
  #print('\n')
  #print(dir(position))
  #print('\n')
  #print(position.T[0])
  #print(position.T[1])
  #print('\n')

  plot_pd = pandas.DataFrame()
  plot_pd['time'] = [dt*i for i in range(len(E))]
  plot_pd['Vtotal'] = E
  #plot_pd['tl'] = f'{name}'
  #plot_pd['tl'] = f'{tl._id}'
  plot_pd['tl'] = f'{position}'

  if position.T[0] == 0.0205 and (position.T[1] == 0.0206 or position.T[1] == 0.0204):
    print('\n')
    print('Found transmitter at ')
    print(position)
    #print('ID:')
    #print(tl)
    print('\n')
    plot_pds2.append(
      plot_pd
    )
  else:
    print('Found transmission line at ')
    print(position)
    #print('ID:')
    #print(tl)
    #print('\n')
    plot_pds.append(
      plot_pd
    )
    plot_pds2.append(
      plot_pd
    )

plot_pd = pandas.concat(plot_pds)
plot_pd2 = pandas.concat(plot_pds2)

(
  ggplot(plot_pd[plot_pd['time'] >= 2e-10])
  + aes(x='time',y='Vtotal',color='tl',group='tl')
  + geom_line()
  + theme_light()
).save('plot_voltage.png')

(
  ggplot(plot_pd2[plot_pd2['time'] >= 2e-10])
  + aes(x='time',y='Vtotal',color='tl',group='tl')
  + geom_line()
  + theme_light()
).save('plot_voltage2.png')
