"""
This script correlates with the slides on MemCtrl() and MemCtrlInterface().
to run this script, use the following command:
$ gem5/build/NULL/gem5.opt /workspaces/2024/materials/using-gem5/ \
    06-memory-models/completed/blank_memory.py


"""

# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *
from m5.util.convert import *

import math


# Helper Functions
def createLinearTraffic(tgen):
    yield tgen.createLinear(1_000_000_000,
                            0,
                            512_000_000,
                            64,
                            12000,
                            12000,
                            60, 0)
    yield tgen.createExit(0)

# create the system we are going to simulate
system = System()

# Set the clock fequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')] # Create an address range
addr_range = system.mem_ranges[0]

system.tgen = PyTrafficGen() # Create a traffic generator

system.membus = SystemXBar(width = 64, max_routing_table_size = 16777216)

system.tgen.port = system.membus.cpu_side_ports

## insert memory controller and interface here

# memory controller parameters
system.mem_ctrl = MemCtrl()
system.mem_ctrl.mem_sched_policy = "fcfs"

# memory interface parameters
system.mem_ctrl.dram = DDR4_2400_16x4()
system.mem_ctrl.dram.range = AddrRange('512MB')
system.mem_ctrl.dram.read_buffer_size = 32
system.mem_ctrl.dram.write_buffer_size = 64
system.mem_ctrl.dram.device_size = '512MB'

system.mem_ctrl.port = system.membus.mem_side_ports


##


root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

system.tgen.start(createLinearTraffic(system.tgen))


print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))










