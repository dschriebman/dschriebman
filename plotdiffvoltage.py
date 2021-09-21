import math
from plotnine import *
import pandas
import numpy
import h5py

f = h5py.File('sim3d.out')

plot_pds = []
plot_pds2 = []
dt = f.attrs['dt']

rxs = {}
#names = {}
#positions = {}

for key, rx in f['rxs'].items():
  v = int(key[2:])-1
  print('key,v')
  print(key, v)
  rx_id = int(int(v) / 2)
  rx_terminal = int(v) % 2
  Ex = [x for x in rx['Ex']]
  Ey = [y for y in rx['Ey']]
  E = [math.sqrt(x*x + y*y) for x,y in zip(Ex, Ey)]
  if rx_id not in rxs:
    rxs[rx_id] = {}
    #names[rx_id] = {}
    #positions[rx_id] = {}

  rxs[rx_id][rx_terminal] = numpy.array(Ey)
  #print('array IDs:')
  #print(rx_id)
  #print(rx_terminal)
  #print(rxs[rx_id][rx_terminal])
  name = rx.attrs['Name']
  position = rx.attrs['Position']
  #names[rx_id][rx_terminal] = rx.attrs['Name']
  #positions[rx_id][rx_terminal] = rx.attrs['Position']
  #print('name')
  #print(f'rx {name}')
  #print('name')
  print('position')
  print(f'rx {position}')
  #print('position')
  
print('\n')

for rx_id, rx in rxs.items():
  difference = rx[1] - rx[0]
  key = f'rx{rx_id}'
  plot_pd = pandas.DataFrame()
  plot_pd['time'] = [dt*i for i in range(len(E))]
  plot_pd['Ey'] = difference
  plot_pd['rx'] = key
  print('key:')
  print(key)
  if (key=='rx4'):
    print('transmitter')
    plot_pds.append(
      plot_pd
    )
  else:
    plot_pds2.append(
      plot_pd
    )
    plot_pds.append(
      plot_pd
    )

plot_pd = pandas.concat(plot_pds)
plot_pd2 = pandas.concat(plot_pds2)

(
  ggplot(plot_pd[plot_pd['time'] >= 0e-10])
  + aes(x='time',y='Ey',color='rx',group='rx')
  + geom_line()
  + theme_light()
).save('interpreted_diff_voltage.png')

(
  ggplot(plot_pd2[plot_pd2['time'] >= 0e-10])
  + aes(x='time',y='Ey',color='rx',group='rx')
  + geom_line()
  + theme_light()
).save('interpreted_diff_voltage2.png')
