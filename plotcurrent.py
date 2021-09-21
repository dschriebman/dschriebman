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

for key, rx in f['rxs'].items():
  Ix = [x for x in rx['Ix']]
  Iy = [y for y in rx['Iy']]
  Iz = [z for z in rx['Iz']]
  #E = [math.sqrt(x*x + y*y +z*z) for x,y,z in zip(Ex, Ey, Ez)]

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
  plot_pd['time'] = [dt*i for i in range(len(Ix))]
  plot_pd['Ix'] = Ix
  plot_pd['rx'] = f'{name}'

  if position.T[0] != 0.0325 or position.T[1] != 0.0325:
    plot_pds.append(
      plot_pd
    )
    plot_pds2.append(
      plot_pd
    )
  else:
    print('Found transmitter at ')
    print(position)
    print('ID:')
    print(rx)
    print('\n')
    plot_pds2.append(
      plot_pd
    )

plot_pd = pandas.concat(plot_pds)
plot_pd2 = pandas.concat(plot_pds2)

(
  ggplot(plot_pd[plot_pd['time'] >= 2e-10])
  + aes(x='time',y='Ey',color='rx',group='rx')
  + geom_line()
  + theme_light()
).save('plot_current.png')

(
  ggplot(plot_pd2[plot_pd2['time'] >= 2e-10])
  + aes(x='time',y='Ey',color='rx',group='rx')
  + geom_line()
  + theme_light()
).save('plot_current2.png')
