# located in gem5/configs/IBLP

import m5
from m5.objects import *
from caches import DataCache, InstructionCache, ItemCache, BlockCache, IBLPCache

# most of this code is straight from the tutorial, just relocated to the System obj init to streamline things

class StreamlinedSystem(System):
    def __init__(self):
        super(System, self).__init__()
        self.clk_domain = SrcClockDomain()
        self.clk_domain.clock = '1GHz'
        self.clk_domain.voltage_domain = VoltageDomain()
        self.mem_mode = 'timing'
        self.mem_ranges = [AddrRange('512MB')]

        self.cpu = X86TimingSimpleCPU()
        self.cpubus = L2XBar()
        self.membus = SystemXBar()

    def setup_caches(self, cache_type):
        self.cpu.icache = InstructionCache()
        self.cpu.dcache = DataCache()
        # connect L1 caches to CPU
        self.cpu.icache.connectCPU(self.cpu)
        self.cpu.dcache.connectCPU(self.cpu)
        # connect L1 caches to L2 bus
        self.cpu.icache.connectBus(self.cpubus)
        self.cpu.dcache.connectBus(self.cpubus)

        if (cache_type == "Item"):
            self.l2cache = ItemCache()
        elif (cache_type == "Block"):
            self.l2cache = BlockCache()
        elif (cache_type == "IBLP"):
            self.l2cache = IBLPCache()
        else:
            raise ValueError("Should not be possible to get here...")
        # connect L2 cache to L2 & mem busses
        self.l2cache.connectCPUSideBus(self.cpubus)
        self.l2cache.connectMemSideBus(self.membus)

    def setup_memory(self):
        # create I/O controller & connect to memory bus
        self.cpu.createInterruptController()
        self.cpu.interrupts[0].pio = self.membus.mem_side_ports
        self.cpu.interrupts[0].int_requestor = self.membus.cpu_side_ports
        self.cpu.interrupts[0].int_responder = self.membus.mem_side_ports
        self.system_port = self.membus.cpu_side_ports
        # create memory controller & connect to mem bus
        self.mem_ctrl = MemCtrl()
        self.mem_ctrl.dram = DDR3_1600_8x8()
        self.mem_ctrl.dram.range = self.mem_ranges[0]
        self.mem_ctrl.port = self.membus.mem_side_ports

    def run(self, binary):
        # for gem5 V21 and beyond
        self.workload = SEWorkload.init_compatible(binary)
        process = Process()
        process.cmd = [binary]
        self.cpu.workload = process
        self.cpu.createThreads()

        root = Root(full_system = False, system = self)
        m5.instantiate()

        print("Beginning simulation...")
        exit_event = m5.simulate()
        print('Exiting @ tick {} because {}'
          .format(m5.curTick(), exit_event.getCause()))

