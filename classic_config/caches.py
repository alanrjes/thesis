# located in gem5/configs/IBLP

from m5.objects import Cache, SystemXBar

# L1, instruction & data caches-->
class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def connectCPU(self, cpu):
        # need to define this in a base class!
        raise NotImplementedError

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class DataCache(L1Cache):
    size = '16kB'

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class InstructionCache(L1Cache):
    size = '64kB'

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

# L2, block & item cache layers-->
class L2Cache(Cache):
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self, options, cache_type="standard"):
        super(L2Cache, self).__init__()
        self.assoc = options["associativity"]
        if cache_type in ["block_layer, item_layer"]:
            self.size = str(options[cache_type]["proportion"]*options["cache_size"])+"kB"
        else:
            self.size = str(options["cache_size"])+"kB"

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class IBLPCache(L2Cache):
    def __init__(self, options):
        super(IBLPCache, self).__init__(options, "item_layer")
        self.blockLayer = L2Cache(options, "block_layer")
        self.bus = SystemXBar()
        self.mem_side = self.bus.cpu_side_ports
        self.blockLayer.cpu_side = self.bus.mem_side_ports
    
    def connectMemSideBus(self, memBus):
        self.blockLayer.mem_side = memBus.cpu_side_ports
