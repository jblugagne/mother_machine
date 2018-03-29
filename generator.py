# Python version:

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
    
def writetext(text, layout, size):

  blib = pya.Library.library_by_name("Basic")
  pid = blib.layout().pcell_declaration("TEXT")
  tempcell = layout.create_cell(text)
  param = { 
    "text": text, 
    "layer": pya.LayerInfo(1, 0),  # target layer of the text: layer 17, datatype 5 
    "mag": size/700
  }
  pv = []
  for p in pid.get_parameters():
    if p.name in param:
      pv.append(param[p.name])
    else:
      pv.append(p.default)
  
  # create the PCell variant cell
  pcell_var = layout.add_pcell_variant(blib, pid.id(), pv)
  pcell_inst = tempcell.insert(pya.CellInstArray(pcell_var, pya.Trans()))
  return tempcell

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
channels = layout.create_cell("channels")
l1 = layout.layer(1, 0)


## MAIN CHANNELS
num_channels = 8
max_width = 12e6
max_length =  35e6
obs_spacing = 530e3
inlets_spacing = max_width/(num_channels-1)
chan_width = 400e3

## Get one middle channel to know the path length:(I'm removing this part for now, there isn't that much change)
#midchan = buildchannel(inlet_y=inlets_spacing/2,inlet_x=-max_length/2,obs_y=obs_spacing/2)
#channels_length = midchan.length()
#print(midchan.length())
channels_length = max_length

for indChan in range(0,num_channels/2):
    inlet_y = (indChan + 0.5)*inlets_spacing
    obs_y = (indChan + 0.5)*obs_spacing
    newchan = buildchannel(inlet_y=inlet_y, obs_y=obs_y, chan_length=channels_length, chan_width=chan_width)
    channels.shapes(l1).insert(newchan)
    newchan = buildchannel(inlet_y=-inlet_y, obs_y=-obs_y, chan_length=channels_length, chan_width=chan_width)
    channels.shapes(l1).insert(newchan)
# Add big numbers:
bignumberssize = 2e6
chnum = writetext("ch1l25w1.3",layout, bignumberssize)
numbers = pya.CellInstArray(chnum.cell_index(),
    pya.Trans(pya.Vector(-(3*num_chambers+6)*spacing_chambers/2 - (bignumberssize + 1.5e6),
        -(num_channels/2)*obs_spacing - (bignumberssize + 100e3))))
channels.insert(numbers)

## Chambers:

# 25 um chambers
chamber_1_25e3 = layout.create_cell("chamber_1_25e3")
chamber = makechamber(0, 0, width=1300, length=25e3 )
chamber_1_25e3.shapes(l1).insert(chamber)

chamber_2_25e3 = layout.create_cell("chamber_2_25e3")
chamber = makechamber(0, 0, width=1500, length=25e3 )
chamber_2_25e3.shapes(l1).insert(chamber)

chamber_3_25e3 = layout.create_cell("chamber_3_25e3")
chamber = makechamber(0, 0, width=1800, length=25e3 )
chamber_3_25e3.shapes(l1).insert(chamber)

# 35 um chambers
chamber_1_35e3 = layout.create_cell("chamber_1_35e3")
chamber = makechamber(0, 0, width=1300, length=35e3)
chamber_1_35e3.shapes(l1).insert(chamber)

chamber_2_35e3 = layout.create_cell("chamber_2_35e3")
chamber = makechamber(0, 0, width=1500, length=35e3 )
chamber_2_35e3.shapes(l1).insert(chamber)

chamber_3_35e3 = layout.create_cell("chamber_3_35e3")
chamber = makechamber(0, 0, width=1800, length=35e3 )
chamber_3_35e3.shapes(l1).insert(chamber)

# Xi's short chambers:
chamber_Xi1 = layout.create_cell("chamber_Xi1")
chamber = makechamber(0, 0, width=1300, length=8e3 )
chamber_Xi1.shapes(l1).insert(chamber)
chamber_Xi2 = layout.create_cell("chamber_Xi2")
chamber = makechamber(0, 0, width=1500, length=8e3 )
chamber_Xi2.shapes(l1).insert(chamber)


## Instantiate arrays of mother machines:
spacing_chambers = 5e3
num_chambers = 1000

# 25:
Multi_chamber_1_25e3 = layout.create_cell("Multi_chamber_1_25e3")
Mach_array = pya.CellInstArray(chamber_1_25e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_1_25e3.insert(Mach_array)

Multi_chamber_2_25e3 = layout.create_cell("Multi_chamber_2_25e3")
Mach_array = pya.CellInstArray(chamber_2_25e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_2_25e3.insert(Mach_array)

Multi_chamber_3_25e3 = layout.create_cell("Multi_chamber_3_25e3")
Mach_array = pya.CellInstArray(chamber_3_25e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_3_25e3.insert(Mach_array)

# 35:
Multi_chamber_1_35e3 = layout.create_cell("Multi_chamber_1_35e3")
Mach_array = pya.CellInstArray(chamber_1_35e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_1_35e3.insert(Mach_array)

Multi_chamber_2_35e3 = layout.create_cell("Multi_chamber_2_35e3")
Mach_array = pya.CellInstArray(chamber_2_35e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_2_35e3.insert(Mach_array)

Multi_chamber_3_35e3 = layout.create_cell("Multi_chamber_3_35e3")
Mach_array = pya.CellInstArray(chamber_3_35e3.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_chambers, 1)
Multi_chamber_3_35e3.insert(Mach_array)

#Xi:
num_Xi = 400

Multi_chamber_Xi1 = layout.create_cell("Multi_chamber_Xi1")
Mach_array = pya.CellInstArray(chamber_Xi1.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_Xi, 1)
Multi_chamber_Xi1.insert(Mach_array)

Multi_chamber_Xi2 = layout.create_cell("Multi_chamber_Xi2")
Mach_array = pya.CellInstArray(chamber_Xi2.cell_index(),pya.Trans(),pya.Vector(spacing_chambers,0),pya.Vector(0,0),num_Xi, 1)
Multi_chamber_Xi2.insert(Mach_array)


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


## Instantiate into assembled "sides"
spacing_crosses = 20e3
num_crosses = (3*(num_chambers+3)+num_Xi)*spacing_chambers/spacing_crosses

# 25:
crosses_shift = 30e3 + cross_size/2
AssembleSide_25e3 = layout.create_cell("AssembleSide_25e3")
Mach_array = pya.CellInstArray(Multi_chamber_1_25e3.cell_index(),pya.Trans())
AssembleSide_25e3.insert(Mach_array)
Mach_array = pya.CellInstArray(Multi_chamber_2_25e3.cell_index(),pya.Trans((num_chambers+3)*spacing_chambers,0))
AssembleSide_25e3.insert(Mach_array)
Mach_array = pya.CellInstArray(Multi_chamber_3_25e3.cell_index(),pya.Trans(2*(num_chambers+3)*spacing_chambers,0))
AssembleSide_25e3.insert(Mach_array)
Mach_array = pya.CellInstArray(Multi_chamber_Xi1.cell_index(),pya.Trans(3*(num_chambers+3)*spacing_chambers,0))
AssembleSide_25e3.insert(Mach_array)
cross_array = pya.CellInstArray(focuscross.cell_index(),pya.Trans(pya.Vector(0,-crosses_shift)), pya.Vector(spacing_crosses,0),pya.Vector(0,0),num_crosses, 1)
AssembleSide_25e3.insert(cross_array)

# 35:
crosses_shift = 40e3 + cross_size/2
AssembleSide_35e3 = layout.create_cell("AssembleSide_35e3")
Mach_array = pya.CellInstArray(Multi_chamber_1_35e3.cell_index(),pya.Trans())
AssembleSide_35e3.insert(Mach_array)
Mach_array = pya.CellInstArray(Multi_chamber_2_35e3.cell_index(),pya.Trans((num_chambers+3)*spacing_chambers,0))
AssembleSide_35e3.insert(Mach_array)
Mach_array = pya.CellInstArray(Multi_chamber_3_35e3.cell_index(),pya.Trans(2*(num_chambers+3)*spacing_chambers,0))
AssembleSide_35e3.insert(Mach_array)
Mach_array = pya.CellInstArray(Multi_chamber_Xi2.cell_index(),pya.Trans(3*(num_chambers+3)*spacing_chambers,0))
AssembleSide_35e3.insert(Mach_array)
cross_array = pya.CellInstArray(focuscross.cell_index(),pya.Trans(pya.Vector(0,-crosses_shift)), pya.Vector(spacing_crosses,0),pya.Vector(0,0),num_crosses, 1)
AssembleSide_35e3.insert(cross_array)


## Put the two sides together:
Assemble_2sides = layout.create_cell("Assemble_2sides")
Mach_25 = pya.CellInstArray(AssembleSide_25e3.cell_index(),pya.Trans(pya.Vector(-(3*num_chambers + 6)*spacing_chambers/2,-chan_width/2)))
Assemble_2sides.insert(Mach_25)
Mach_35 = pya.CellInstArray(AssembleSide_35e3.cell_index(),pya.Trans(0, True, pya.Vector(-(3*num_chambers + 6)*spacing_chambers/2,chan_width/2)))
Assemble_2sides.insert(Mach_35)


## Make an array of assembled sides:
Multi_assembled = layout.create_cell("Multi_assembled")
Mach_array = pya.CellInstArray(Assemble_2sides.cell_index(),
  pya.Trans(pya.Vector(0,-(num_channels-1)*obs_spacing/2)),
  pya.Vector(0,obs_spacing),
  pya.Vector(0,0),
  num_channels,
  0)
Multi_assembled.insert(Mach_array)
# Add numbers:
numberssize = 15e3
for i in range(0,num_channels):
  chnum = writetext(str(i+1),layout, numberssize)
  chnum.flatten(True)
  numbers = pya.CellInstArray(chnum.cell_index(),
    pya.Trans(pya.Vector(-(3*num_chambers+6)*spacing_chambers/2,-(num_channels/2-i)*obs_spacing)),
    pya.Vector(spacing_crosses,0),
    pya.Vector(0,0),
    num_crosses,
    1)
  Multi_assembled.insert(numbers)


## Instantiate & add alignment crosses:
spacing_machines = max_width + 4.5e6
num_machines = 4
cross_size = 5e6
cross1_x = max_length/2 + cross_size + 5e6
cross1_y = 0
cross2_x = -(max_length/2 + cross_size + 5e6)
cross2_y = 0

#Load from file:
layout.read("/home/jeanbaptiste/bu/wafers/align_crosses/maincross_tri.gds")
layout.move_layer(2L,0L) # Put all on the same layer
layout.clear_layer(2L)
alignment_cross = layout.cell("alignment_cross")

# Chambers:
Multi_assembled_withCrosses = layout.create_cell("Multi_assembled_withCrosses")
chambers = pya.CellInstArray(Multi_assembled.cell_index(),
    pya.Trans(pya.Vector(0,-spacing_machines*(num_machines-1)/2)),
    pya.Vector(0,spacing_machines),
    pya.Vector(0,0),
    num_machines,
    1)
Multi_assembled_withCrosses.insert(chambers)

cross1 = pya.CellInstArray(alignment_cross.cell_index(),pya.Trans(pya.Vector(cross1_x,cross1_y)))
cross2 = pya.CellInstArray(alignment_cross.cell_index(),pya.Trans(pya.Vector(cross2_x,cross2_y)))
Multi_assembled_withCrosses.insert(cross1)
Multi_assembled_withCrosses.insert(cross2)
# Channels:
channels_withCrosses = layout.create_cell("channels_withCrosses")
chans = pya.CellInstArray(channels.cell_index(),
    pya.Trans(pya.Vector(0,-spacing_machines*(num_machines-1)/2)),
    pya.Vector(0,spacing_machines),
    pya.Vector(0,0),
    num_machines,
    1)
channels_withCrosses.insert(chans)
channels_withCrosses.insert(cross1)
channels_withCrosses.insert(cross2)

## Form the final mask:
spacing_layers = spacing_machines/4
#spacing_layers = 0
mask = layout.create_cell("mask")
final = pya.CellInstArray(channels_withCrosses.cell_index(),pya.Trans(pya.Vector(0,-spacing_layers)))
mask.insert(final)
final = pya.CellInstArray(Multi_assembled_withCrosses.cell_index(),pya.Trans(pya.Vector(0,spacing_layers)))
mask.insert(final)


layout.write("/home/jeanbaptiste/bu/wafers/mother_machine.gds")