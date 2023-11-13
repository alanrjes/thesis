# located in gem5/configs/IBLP

from m5.objects import Cache, SystemXBar

# Note to self: are the values of these constant class properties correct/necessary?
# They're just what was in the tutorial
# Maybe some of them should be parameters?

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
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class ItemCache(L2Cache):
    # how to specify granularity?

    def __init__(self, size="256kB"):
        super(L2Cache, self).__init__()
        self.size = size

class BlockCache(L2Cache):
    def __init__(self, size="256kB"):
        super(L2Cache, self).__init__()
        self.size = size

class IBLPCache(ItemCache):
    # Block cache is wrapped in Item cache so that there's one thing to hand to System,
    # but since the bus ports are connected appropriately, I don't *think* it should matter.

    def __init__(self, itemLayerSize="128kB", blockLayerSize="128kB"):
        super(ItemCache, self).__init__()
        self.size = itemLayerSize
        self.blockLayer = BlockCache(blockLayerSize)
        self.bus = SystemXBar()
        self.mem_side = self.bus.cpu_side_ports
        self.blockLayer.cpu_side = self.bus.mem_side_ports

    def connectCPUSideBus(self, cpuBus):
        self.cpu_side = cpuBus.mem_side_ports
    
    def connectMemSideBus(self, memBus):
        self.blockLayer.mem_side = memBus.cpu_side_ports
