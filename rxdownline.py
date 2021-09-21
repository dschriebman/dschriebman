import math
from plotnine import *
import pandas
import numpy
import h5py

f = h5py.File('sim3d.out')

plot_pds = []
plot_pds2 = []
dt = f.attrs['dt']

for key, rx in f['rxs'].items():
  Ex = [x for x in rx['Ex']]
  Ey = [y for y in rx['Ey']]
  Ez = [z for z in rx['Ez']]
  #E = [math.sqrt(x*x + y*y) for x,y in zip(Ex, Ey)]
  E = [math.sqrt(x*x + y*y +z*z) for x,y,z in zip(Ex, Ey, Ez)]

  name = rx.attrs['Name']
  position = rx.attrs['Position']

  print(f'rx {name}: {position}')
  #print('\n')
  #print(dir(position))
  #print('\n')
  #print(position.T[0])
  print(position.T[1])
  #print('\n')

  plot_pd = pandas.DataFrame()
  plot_pd['time'] = [dt*i for i in range(len(E))]
  plot_pd['Ey'] = E
  plot_pd['rx'] = f'{name}'

  if position.T[0] == 0.0205 and position.T[1] == 0.0206:
    print('Found receiver at ')
    print(position)
    print('ID:')
    print(rx)
    print('\n')
    plot_pds.append(
      plot_pd
    )
    if position.T[2]!= 0.0235:
      plot_pds2.append(
        plot_pd
      )
  #else:
    #plot_pds.append(
      #plot_pd
    #)
    #plot_pds2.append(
      #plot_pd
    #)

plot_pd = pandas.concat(plot_pds)
plot_pd2 = pandas.concat(plot_pds2)

(
  ggplot(plot_pd[plot_pd['time'] >= 0e-10])
  + aes(x='time',y='Ey',color='rx',group='rx')
  + geom_line()
  + theme_light()
).save('rxdownline_voltage.png')

(
  ggplot(plot_pd2[plot_pd2['time'] >= 0e-10])
  + aes(x='time',y='Ey',color='rx',group='rx')
  + geom_line()
  + theme_light()
).save('rxdownline_voltage2.png')
