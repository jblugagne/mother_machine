# Python version: 2.7

import pya
from  math import sqrt

def makecircle( center_x, center_y, radius, vertices=40):
    
    circle = pya.Box(pya.Point(center_x-radius,center_y-radius),pya.Point(center_x+radius,center_y+radius))
    circle = pya.SimplePolygon(circle)
    circle = circle.round_corners(radius,radius,vertices)
    return circle
    
def makechamber( x, y, width=1.5e3, length=25e3,overlap=5e3,funnel=True, roundends=True,funnel_radius=10e3,funnel_depth=5e3):
    
    chamber = pya.Box(pya.Point(x-width/2,y-length),pya.Point(x+width/2,y+overlap))
    chamber = pya.SimplePolygon(chamber)
    if roundends:
        chamber = chamber.round_corners(width,width,30)
    chamber = pya.Region(chamber)
    if funnel:
        funnel = pya.Box(pya.Point(x-(width/2+funnel_radius),y-funnel_depth),pya.Point(x+(width/2+funnel_radius),y+overlap))
        disk = makecircle(x-(width/2+funnel_radius),y-funnel_depth, funnel_radius, 200)
        funnel = pya.Region(funnel)
        disk = pya.Region(disk)
        funnel -= disk
        disk = makecircle(x+(width/2+funnel_radius),y-funnel_depth, funnel_radius, 200)
        disk = pya.Region(disk)
        funnel -= disk
        chamber += funnel
        chamber = chamber.merge()
    return chamber

def buildchannel( inlet_y, obs_y, obs_length=23e6, bend_radius=2e6, chan_width = 400e3, chan_length=0.0, inlet_x=0.0, inlet_radius=500e3):
    if inlet_x == 0 :
        arm_length = (chan_length-obs_length)/2
        inlet_x = -(sqrt((arm_length)**2 - (inlet_y - obs_y)**2) + obs_length/2)
    # Start
    currpoint = pya.Point(inlet_x, inlet_y)
    points = [currpoint]
    # First elbow
    currpoint = pya.Point(-obs_length/2, obs_y)
    points.append(currpoint)
    #Second elbow
    currpoint = pya.Point(obs_length/2, obs_y)
    points.append(currpoint)
    #End
    currpoint = pya.Point(-inlet_x, inlet_y)
    points.append(currpoint)
    
    # Create, bend corners, transform into polygon:
    chan = pya.Path(points, chan_width)
    chan = chan.round_corners(bend_radius,100)
    chan = chan.simple_polygon()
    
    # Add the disks for the inlets:
    inlet = makecircle( inlet_x, inlet_y, inlet_radius)
    outlet = makecircle( -inlet_x, inlet_y, inlet_radius)
    
    # Make a region out of the different elements, and merge it:
    chan = pya.Region(chan)
    chan.insert(inlet)
    chan.insert(outlet)
    chan = chan.merge()
    
    return chan

layout = pya.Layout()
top = layout.create_cell("mask")
Cchan = layout.create_cell("channels")
l1 = layout.layer(1, 0)


## MAIN CHANNELS
num_channels = 10
max_width = 15e6
max_length =  35e6
obs_spacing = 500e3
inlets_spacing = max_width/(num_channels-1)

## Get one middle channel to know the path length:(I'm removing this part for now, there isn't that much change)
#midchan = buildchannel(inlet_y=inlets_spacing/2,inlet_x=-max_length/2,obs_y=obs_spacing/2)
#channels_length = midchan.length()
#print(midchan.length())
channels_length = max_length

for indChan in range(0,num_channels/2):
    inlet_y = (indChan + 0.5)*inlets_spacing
    obs_y = (indChan + 0.5)*obs_spacing
    newchan = buildchannel(inlet_y=inlet_y, obs_y=obs_y, chan_length=channels_length)
    Cchan.shapes(l1).insert(newchan)
    newchan = buildchannel(inlet_y=-inlet_y, obs_y=-obs_y, chan_length=channels_length)
    Cchan.shapes(l1).insert(newchan)


## Chambers:

# 25 um chambers
chamber_1500_25e3 = layout.create_cell("chamber_1500_25e3")
chamber = makechamber(0, 0, width=1500, length=25e3 )
chamber_1500_25e3.shapes(l1).insert(chamber)

chamber_1800_25e3 = layout.create_cell("chamber_1800_25e3")
chamber = makechamber(0, 0, width=1800, length=25e3 )
chamber_1800_25e3.shapes(l1).insert(chamber)

chamber_2100_25e3 = layout.create_cell("chamber_2100_25e3")
chamber = makechamber(0, 0, width=2100, length=25e3 )
chamber_2100_25e3.shapes(l1).insert(chamber)

# 35 um chambers
chamber_1500_35e3 = layout.create_cell("chamber_1500_35e3")
chamber = makechamber(0, 0, width=1500, length=35e3)
chamber_1500_35e3.shapes(l1).insert(chamber)

chamber_1800_35e3 = layout.create_cell("chamber_1800_35e3")
chamber = makechamber(0, 0, width=1800, length=35e3 )
chamber_1800_35e3.shapes(l1).insert(chamber)

chamber_2100_35e3 = layout.create_cell("chamber_2100_35e3")
chamber = makechamber(0, 0, width=2100, length=35e3 )
chamber_2100_35e3.shapes(l1).insert(chamber)


## Focusing cross:
cross_size = 15e3
cross_thickness = 2e3
focuscross = layout.create_cell("focuscross")
cross1 = pya.Box(pya.Point(-cross_thickness/2, -cross_size/2), pya.Point(cross_thickness/2, cross_size/2))
cross2 = pya.Box(pya.Point(-cross_size/2, -cross_thickness/2), pya.Point(cross_size/2, cross_thickness/2))
cross = pya.Region(cross1)
cross.insert(cross2)
cross = cross.merge()
focuscross.shapes(l1).insert(cross)


## Instantiate arrays of mother machines:
spacing_chambers = 5e3
num_chambers = 1000

# 25:
Multi_chamber_1500_25e3 = layout.create_cell("Multi_chamber_1500_25e3")
Mach_array = pya.CellInstArray(chamber_1500_25e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_1500_25e3.insert(Mach_array)

Multi_chamber_1800_25e3 = layout.create_cell("Multi_chamber_1800_25e3")
Mach_array = pya.CellInstArray(chamber_1800_25e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_1800_25e3.insert(Mach_array)

Multi_chamber_2100_25e3 = layout.create_cell("Multi_chamber_2100_25e3")
Mach_array = pya.CellInstArray(chamber_2100_25e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_2100_25e3.insert(Mach_array)

# 35:
Multi_chamber_1500_35e3 = layout.create_cell("Multi_chamber_1500_35e3")
Mach_array = pya.CellInstArray(chamber_1500_35e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_1500_35e3.insert(Mach_array)

Multi_chamber_1800_35e3 = layout.create_cell("Multi_chamber_1800_35e3")
Mach_array = pya.CellInstArray(chamber_1800_35e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_1800_35e3.insert(Mach_array)

Multi_chamber_2100_35e3 = layout.create_cell("Multi_chamber_2100_35e3")
Mach_array = pya.CellInstArray(chamber_2100_35e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_2100_35e3.insert(Mach_array)


## Instantiate into assembled "sides"
spacing_crosses = 20e3
num_crosses = 3*(num_chambers+3)*spacing_chambers/spacing_crosses

# 25:
crosses_shift = 30e3 + cross_size/2
AssembleSide_25e3 = layout.create_cell("AssembleSide_25e3")
Mach_array = pya.CellInstArray(Multi_chamber_1500_25e3.cell_index(),pya.Trans())
AssembleSide_25e3.insert(Mach_array)
Mach_array = pya.CellInstArray(Multi_chamber_1800_25e3.cell_index(),pya.Trans((num_chambers+3)*spacing_chambers,0))
AssembleSide_25e3.insert(Mach_array)
Mach_array = pya.CellInstArray(Multi_chamber_2100_25e3.cell_index(),pya.Trans(2*(num_chambers+3)*spacing_chambers,0))
AssembleSide_25e3.insert(Mach_array)
cross_array = pya.CellInstArray(focuscross.cell_index(),pya.Trans(pya.Vector(0,-crosses_shift)), pya.Vector(spacing_crosses,0),pya.Vector(0,0),num_crosses, 1)
AssembleSide_25e3.insert(cross_array)

# 25:
crosses_shift = 40e3 + cross_size/2
AssembleSide_35e3 = layout.create_cell("AssembleSide_35e3")
Mach_array = pya.CellInstArray(Multi_chamber_1500_35e3.cell_index(),pya.Trans())
AssembleSide_35e3.insert(Mach_array)
Mach_array = pya.CellInstArray(Multi_chamber_1800_35e3.cell_index(),pya.Trans((num_chambers+3)*spacing_chambers,0))
AssembleSide_35e3.insert(Mach_array)
Mach_array = pya.CellInstArray(Multi_chamber_2100_35e3.cell_index(),pya.Trans(2*(num_chambers+3)*spacing_chambers,0))
AssembleSide_35e3.insert(Mach_array)
cross_array = pya.CellInstArray(focuscross.cell_index(),pya.Trans(pya.Vector(0,-crosses_shift)), pya.Vector(spacing_crosses,0),pya.Vector(0,0),num_crosses, 1)
AssembleSide_35e3.insert(cross_array)

## Put the two sides together:


## Make an array of assembled sides:

## Add alignment crosses:

## Form the final mask

layout.write("/home/jeanbaptiste/bu/wafers/mother_machine.gds")
