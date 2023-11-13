import sys
import argparse
import linecache
import subprocess

# args for running tests
parser = argparse.ArgumentParser(description="")
parser.add_argument("binary",
                    nargs="?",
                    type=str,
                    help="Path to the binary to execute.",
                    default="tests/test-progs/hello/bin/x86/linux/hello")
parser.add_argument("--item_layer_size", "-i",
                    help="Size of item-granularity layer of L2 cache (in kB).",
                    type=int,
                    default=128)
parser.add_argument("--block_layer_size", "-b",
                    help="Size of block-granularity layer of L2 cache (in kB).",
                    type=int,
                    default=128)
parser.add_argument("--cache_models", "-c",
                    help="Which cache models to test",
                    nargs="+",
                    type=str,
                    choices=["Item", "Block", "IBLP"],
                    default=["Item", "Block", "IBLP"])
parser.add_argument("--trials", "-t",
                    type=int,
                    help="Number of trials to run per cache type.",
                    default=1)

options = parser.parse_args()

# run gem5 config for some particular inputs
# gem5 config args are: binary --item_layer_size --block_layer_size --cache_model
def runConfig(cacheModel, binary, itemLayerSize, blockLayerSize):
    args = binary+" "+" -i "+str(itemLayerSize)+" -b "+str(blockLayerSize)+" -c "+cacheModel
    cmd = "build/X86/gem5.opt configs/IBLP/config.py "+args
    out = subprocess.check_output(cmd, shell=True, cwd="../gem5")
    return out.decode('utf-8').split("\n")[-1]

# execution & analysis
options = parser.parse_args()
trials = int(options.trials)
results = {k: {"Item layer miss rate":0, "Block layer miss rate":0} for k in ["Item", "Block", "IBLP"]}

for cache in options.cache_models:
    for i in range(trials):
        runConfig(cache, options.binary, options.item_layer_size, options.block_layer_size)
        # check stats.txt result
        f = open("/home/alan/Documents/thesis/gem5/m5out/stats.txt")
        lines = f.readlines()
        results[cache]["Item layer miss rate"] += float(lines[411].split()[1])   # line 412, system.l2cache.overallMissRate::total
        results[cache]["Block layer miss rate"] += float(lines[519].split()[1])  # line 520, system.l2cache.blockLayer.overallMissRate::total
    results[cache] = {k : results[cache][k]/trials for k in ["Item layer miss rate", "Block layer miss rate"]}

print("\n", results)
