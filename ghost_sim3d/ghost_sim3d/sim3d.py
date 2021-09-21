from gprMax.input_cmd_funcs import *
from dataclasses import dataclass
import math
import numpy

def geometry_objects_write(x, y, z, max_x, max_y, max_z, basefile):
    """Prints the #geometry_objects_write command.
    #geometry_objects_write: f1 f2 f3 f4 f5 f6 file1
    """

    cmin = Coordinate(x, y, z)
    cmax = Coordinate(max_x, max_y, max_z)
    command('geometry_objects_write', str(cmin), str(cmax), basefile)
    return basefile


def define_material(
    name,
    permittivity,
    conductivity,
    permeability=1,
    magconductivity=0,
):
    material(
        permittivity=permittivity,
        conductivity=conductivity,
        permeability=permeability,
        magconductivity=magconductivity,
        name=name,
    )
    return name

def define_materials():
    define_material(
        permittivity=50,
        conductivity=0.65,
        name='skin',
    )

    define_material(
        permittivity=13,
        conductivity=0.1,
        name='skull',
    )

    define_material(
        permittivity=50,
        conductivity=1.0,
        name='dura',
    )

    define_material(
        permittivity=70,
        conductivity=2.5,
        name='CSF',
    )

    # command('add_dispersion_debye',1,75.2,9.231e-12,'CSF')

    define_material(
        permittivity=50,
        conductivity=1.0,
        name='grey_matter',
    )

    define_material(
        permittivity=38,
        conductivity=0.7,
        name='white_matter',
    )

    define_material(
        permittivity=1.0,
        conductivity=0.0,
        name='device',
    )

    define_material(
        permittivity=1.0,
        conductivity=59600000,
        name='copper',
    )


@dataclass
class Position:
    """Class for keeping track of an item in inventory."""
    x: float
    y: float
    z: float


def define_array_positions(
    pmax,
    N_array,
    array_separation,
    phantom_start,
):
    return [
        Position(
            array_separation*(i - (N_array-1)/2) + pmax.x/2,
            phantom_start,
            0.0,
        )
        for i in range(N_array)
    ]

def define_array_positions_3d(
    pmax,
    N_array,
    array_separation,
    phantom_start,
):
    return [
        Position(
            array_separation*(i - (N_array-1)/2) + pmax.x/2,
            array_separation*(j - (N_array-1)/2) + pmax.y/2,
            phantom_start,
        )
        for i in range(N_array)
        for j in range(N_array)
    ]


def define_geometry_sim3d(
    pmin,
    pmax,
    dp,
    bowtie_length,
    phantom_start,
    array_positions,
    skin_thickness,
    skull_thickness,
    dura_thickness,
    csf_thickness,
    grey_matter_thickness,
    white_radius,
    shift,
    smooth_materials = False,
):
    smooth_materials_txt = 'y' if smooth_materials else 'n'
    resdiv = 2.5

    box(
        pmin.x, pmin.y, pmin.z + phantom_start,
        pmax.x, pmax.y, pmax.z,
        'device',
        smooth_materials_txt,
    )

    for i, p in enumerate(array_positions):
        triangle(
            p.x, p.y + (0.0 + 2*dp.y), p.z,
            p.x + (bowtie_length*2)/3, p.y + (bowtie_length + 2*dp.y), p.z,
            p.x - (bowtie_length*2)/3, p.y + (bowtie_length + 2*dp.y), p.z,
            dp.z,
            'copper',
            smooth_materials_txt,
        )
        triangle(
            p.x, p.y - (0.0 + 0*dp.y), p.z,
            p.x - (bowtie_length*2)/3, p.y - (bowtie_length + 2*dp.y), p.z,
            p.x + (bowtie_length*2)/3, p.y - (bowtie_length + 2*dp.y), p.z,
            dp.z,
            'copper',
            smooth_materials_txt,
        )
        box(
            p.x, p.y + (0.0 + 1*dp.y), p.z,
            p.x+dp.x, p.y + (0.0 + 2*dp.y), pmax.z-dp.z*11,
            'copper',
            smooth_materials_txt,
        )
        box(
            p.x, p.y - (0.0 + 1*dp.y), p.z,
            p.x+dp.x, p.y - (0.0 + 0*dp.y), pmax.z-dp.z*11,
            'copper',
            smooth_materials_txt,
        )

    skin = phantom_start - skin_thickness
    skull = skin - skull_thickness
    dura = skull - dura_thickness
    csf = dura - csf_thickness
    grey_matter = csf - grey_matter_thickness
    white_center = grey_matter - white_radius

    box(
        0, 0, skin,
        pmax.x, pmax.y, phantom_start,
        'skin',
        smooth_materials_txt,
    )

    box(
        0, 0, skull,
        pmax.x, pmax.y, skin,
        'skull',
        smooth_materials_txt,
    )

    box(
        0, 0, dura,
        pmax.x, pmax.y, skull,
        'dura',
        smooth_materials_txt,
    )

    box(
        0, 0, 0,
        pmax.x, pmax.y, dura,
        'CSF',
        smooth_materials_txt,
    )

    grey_radius = (grey_matter / 2.0) + (csf - grey_matter)
    white_radius = grey_matter / 2.0
    curr_x = 0.2*white_radius
    curr_z = white_radius

    #while curr_x <= pmax.x:
        #cylinder(
            #curr_x, 0, curr_z,
            #curr_x, pmax.y, curr_z,
            #grey_radius,
            #'grey_matter',
            #smooth_materials_txt,
        #)
        #curr_x += 2*white_radius

    #curr_x = 0.2*white_radius
    #while curr_x <= pmax.x:
        #cylinder(
            #curr_x, 0, curr_z,
            #curr_x, pmax.y, curr_z,
            #white_radius,
            #'white_matter',
            #smooth_materials_txt,
        #)
        #curr_x += 2*white_radius

    #box(
        #0, 0, 0,
        #pmax.x, pmax.y, curr_z,
        #'white_matter',
            #smooth_materials_txt,
    #)

    max_Z = 140
    dim_X = 1296 #from file(z)
    dim_Y = 800 #from file(x)
    dim_Z = 1871 #from file(y)
    range_X = int(pmax.x/dp.x)
    range_Y = int(pmax.y/dp.y)
    range_Z = int(pmax.z/dp.z)
    #range_X = int(range_X / 2)
    #range_Y = int(range_Y / 2)
    #range_Z = int(range_Z / 2)
    if range_X > dim_X:
        range_X = dim_X
    if range_Y > dim_Y:
        range_Y = dim_Y
    if range_Z > dim_Z:
        range_Z = dim_Z
    if range_Z > max_Z:
        range_Z = max_Z
    print('\n')
    print('ranges:')
    print(range_X)
    print(range_Y)
    print(range_Z)
    print('\n')
    countwhite = 0
    countgrey = 0
    countother = 0
    countother2 = 0

    file = open("brain.raw", "rb")
    read_data = file.read()
    file.close()
    header = 12

    print('dp.x is')
    print(dp.x)
    print('dp.y is')
    print(dp.y)
    print('dp.z is')
    print(dp.z)

    print('pmax.x is')
    print(pmax.x)
    print('pmax.y is')
    print(pmax.y)
    print('pmax.z is')
    print(pmax.z)

    offset_X = 500
    offset_Y = 550
    #offset_Z = 180 #180 for .1 resolution
    offset_Z = 80 #90 for .25 resolution

    for z in range(range_Z):
        #print(z)
        #print(z*dp.z)
        zdpz = round(z*dp.z,4)
        zdpz1 = round((z+1)*dp.z,4)
        print(zdpz)
        print(zdpz1)

        for y in range(range_Y):
            ydpy = round(y*dp.y,4)
            ydpy1 = round((y+1)*dp.y,4)
            for x in range(range_X):
                xdpx = round(x*dp.x,4)
                xdpx1 = round((x+1)*dp.x,4)
                index = ((offset_Z-z)*1296*1871)+((y+offset_Y)*1296)+(x+offset_X)+header
                if read_data[index] == 123:
                    #print('123 ')
                    countgrey+=1
                    box(
                        xdpx,ydpy,zdpz,
                        xdpx1,ydpy1,zdpz1,
                        'grey_matter',
                        smooth_materials_txt,
                    )
                elif read_data[index] == 124:
                    #print('124 ')
                    countwhite+=1
                    box(
                        xdpx,ydpy,zdpz,
                        xdpx1,ydpy1,zdpz1,
                        'white_matter',
                        smooth_materials_txt,
                    )
                else:
                    countother+=1
                    if read_data[index]!=255:
                        countother2+=1
                        if read_data[index]!=127:
                            print(read_data[index])
                if z>=90/resdiv and z<110/resdiv and x>=290/resdiv and x<310/resdiv and y>=290/resdiv and y<330/resdiv:
                    box(
                        xdpx,ydpy,zdpz,
                        xdpx1,ydpy1,zdpz1,
                        'grey_matter',
                        smooth_materials_txt,
                    )
                if z>=90/resdiv and z<110/resdiv and x>=590/resdiv and x<630/resdiv and y>=590/resdiv and y<610/resdiv:
                    box(
                        xdpx,ydpy,zdpz,
                        xdpx1,ydpy1,zdpz1,
                        'grey_matter',
                        smooth_materials_txt,
                    )

    print('number of elements in file:')
    print('\n')
    print('white:')
    print(countwhite)
    print('\n')
    print('grey:')
    print(countgrey)
    print('\n')
    print('other:')
    print(countother)
    print('\n')
    print('other2:')
    print(countother2)
    print('\n')



def define_tx_rx(
    array_positions,
    dp,
    pmax,
    i_tx,
    resistance,
    pulseplus,
    pulseminus,
    nopulse,
    resolution
):
    resdiv = 2.5
    for i, p in enumerate(array_positions):
        #print('dp.y:')
        #print(dp.y)
        #testval = p.y-dp.y
        #print(testval)
        #testval = p.y+dp.y
        #print(testval)
        #print('\n i,i_tx')
        #print(i)
        #print(',')
        #print(i_tx)
        #print('\n')
        if i == i_tx-1:
            voltage_source(
                'y',
                p.x,
                p.y,
                pmax.z-dp.z*12,
                100,
                pulseplus,
            )
        rx(
            p.x,
            p.y,
            pmax.z-dp.z*12,
        )
        if i == i_tx+7:
            for j in range (14):
                rx(
                    p.x,
                    p.y,
                    pmax.z-dp.z*(12+(j*10)),
                )
        if i == i_tx-1:
            for j in range (14):
                rx(
                    p.x,
                    p.y,
                    pmax.z-dp.z*(12+(j*10)),
                )


def sim3d(
    current_model_run,
    number_model_runs,
    tsim = 1e-9,
    frequency=1e10,
    resistance=40,
    skin_thickness = 0.0015, #was 0.002
    skull_thickness = 0.0055, #was 0.0066
    dura_thickness = 0.0004, #was 0.002
    csf_thickness = 0.0015,
    grey_matter_thickness = 0.004,
    white_radius = 0.007,
    bowtie_length = 0.0054,
    array_separation = 0.012,
    resolution = 2.5e-4,
    shift = 0.2,
    smooth_materials = False,
    snapshots=True,
):
    command('title', 'Phantom Experiment for Brain Imaging')
    command('messages', 'n')

    dim = 3
    N_array = math.ceil(math.pow(number_model_runs, 1/(dim-1)))
    N2_array = math.pow(N_array, (dim-1))

    length = math.ceil(1000*(array_separation * (N_array-1) + 3*bowtie_length))/1000.0
    print('proposed length: ', length)

    pmin = Position(0.0, 0.0, 0.0)
    pmax = Position(
        length,
        length,
        0.060,
    )
    #pmax = Position(
        #0.1296,
        #0.0800,
        #0.1871,
    #)

    #dim_X = 1296 #from file(z)
    #dim_Y = 800 #from file(x)
    #dim_Z = 1871 #from file(y)


    dp = Position(resolution, resolution, resolution)
    N_t = 900

    phantom_start = pmax.z - 0.008 #was0.004 for 0.1res
    phantom_start = pmax.z - 0.038 #was0.004 for 0.1res

    domain(
        x = pmax.x,
        y = pmax.y,
        z = pmax.z,
    )
    dx_dy_dz(dp.x, dp.y, dp.z)
    time_window(tsim)

    define_materials()

    pulseplus = waveform(
        'gaussian',
        amplitude=12.0,
        frequency=frequency,
        identifier='pulseplus',
    )

    pulseminus = waveform(
        'gaussian',
        amplitude=-6.0,
        frequency=frequency,
        identifier='pulseminus',
    )

    nopulse = waveform(
        'gaussian',
        amplitude=0.0,
        frequency=frequency,
        identifier='nopulse',
    )

    array_positions = define_array_positions_3d(
        pmax,
        N_array,
        array_separation,
        phantom_start,
    )

    define_geometry_sim3d(
        pmin,
        pmax,
        dp,
        bowtie_length,
        phantom_start,
        array_positions,
        skin_thickness,
        skull_thickness,
        dura_thickness,
        csf_thickness,
        grey_matter_thickness,
        white_radius,
        shift,
        smooth_materials,
    )

    define_tx_rx(
        array_positions,
        dp,
        pmax,
        current_model_run,
        resistance,
        pulseplus,
        pulseminus,
        nopulse,
        resolution,
    )

    geometry_objects_write(
        pmin.x, pmin.y, pmin.z,
        #pmax.x, phantom_start, pmax.z,
        pmax.x, pmax.y, pmax.z,
        'sim3d_geometry_obj',
    )

    if snapshots:
        geometry_view(
            pmin.x, pmin.y, pmin.z,
            pmax.x, pmax.y, pmax.z,
            #2.5*dp.x, 2.5*dp.y, 2.5*dp.z,
            dp.x, dp.y, dp.z,
            'sim3d_geometry',
            'n',
        )
        for i in range(1, 2):
            snapshot(
                pmin.x, pmin.y, pmin.z,
                pmax.x, pmax.y, pmax.z,
                #5*dp.x, 5*dp.y, 5*dp.z,
                dp.x, dp.y, dp.z,
                i*(tsim/(N_t-1)),
                'sim3d_snapshot' + str(i),
            )


def main():
    sim3d(2,math.pow(7,2))

if __name__ == '__main__':
    main()