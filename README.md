# Thesis source code

## About

...

## File locations

Some files are located in various different subdirectories of the gem5 directory. This is what the overall file structure looks like (irrelevant directories excluded):

```
├── gem5
|   ├── configs
│   │   └── IBLP
|   |       ├── caches.py
|   |       ├── config.py
|   |       ├── options.json
|   |       └── system.py
|   ├── m5out
│   |   └── stats.txt
│   └── tests
│       └── test-progs
|           ├── hello
|           |   └── bin
|           |       └── x86
|           |           └── linux
|           |               └── hello
|           └── src
|               └── hello.c
└── sourcecode
    └── main.py
```

## Execution

Run `main.py`.

### `main.py`

This acts as a wrapper for gem5, to run the gem5 configuration and measure output as is given in the `stats.txt` file. This is partly to streamline testing, but is also necessary because gem5 doesn't write to `stats.txt` until all files in the config have terminated; therefore, it's impossible to access & print the resulting statistics from within the config files.

It takes three arguments:

- Path to the binary of the script to simulate (actual files TBC, for now a placeholder is default).
- [`--cache_models` / `-c`] The cache models to be tested, out of Block, Item, and IBLP (all three by default).
- [`--trials` / `-t`] The number of trials to run of each cache type (default 1).

`run_config(binary, cacheModel)` is defined to execute the gem5 simulation config (see next section for more about the gem5 config).

Then the cache types are iterated through and the resulting statistics collected for the requested number of trials, and the results printed.

TBC: the plan will be to graph the resulting statistics here in `main.py` as well, instead of just printing them.

## Config files

These are all located in a subdirectory of the gem5 build, `gem5/configs/IBLP`, and run using the command `build/X86/gem5.opt configs/IBLP/config.py` from within the `main.py` wrapper.

### `config.py`

The main config file which is run through gem5, and creates the system objects, sets up the system, and starts the simulation using the object & methods defined in `system.py` (see next section).

Takes two arguments:

- Path to the binary of the script to simulate.
- [`--cache_model` / `-c`] One cache type out of Block, Item, or IBLP to simulate.

### `system.py`

Contains the class `StreamlinedSystem` which inherits the gem5 `System` class, and adds methods which takes care of setting up the components of a typical system for simulation. Purely for the sake of streamlining & tidiness. The specifics of most of these steps, with the exception of `setup_caches`, are adapted from the gem5 tutorial.

`__init__(self)` sets up the system attributes that are needed for setting up other features: clock, voltage, memory mode & ranges, cpu, and busses for between L1 and L2 caches.

`setup_caches(self, cache_type)` sets up and connects busses to the caches: the L1 instruction and data caches, which have constant configurations, and the L2 cache, which is configured as either an Item, Block, or IBLP cache.

`setup_memory(self)` sets up the main memory and connects it to the L2 cache bus.

`run(self, binary)` sets the simulation up to run as a process, and runs it.

### `caches.py`

Contains classes for the various types of caches. Reads from `options.json` for some attribute values, so that the python file doesn't need to be modified in order to test different attributes (finding preferred values for these attributes is a WIP).

`L1Cache(Cache)`, `DataCache(L1Cache)`, and `InstructionCache(L1Cache)` are adapted from the gem5 basic caches tutorial, and are meant to mimic a typical system.

`L2Cache(Cache)` contains the attributes shared by both item and block caches.

`ItemCache(L2Cache)` and `BlockCache(L2Cache)` will set the attributes that differentiate granularity between item and block caches and layers (TBC).

`IBLPCache(ItemCache)` simulates an IBLP cache by using an item cache, connected on the memory-side to a block cache, with attributes set so that there is minimal latency between these two caches (TBC). The method `connectMemSideBus(self, bus)` is altered to connect the block layer to the memory bus, to imitate the way the memory connects to layers in the IBLP cache model.
