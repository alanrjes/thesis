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

# run gem5 config for some particular cache model
def run_config(binary, cacheModel):
    args = binary+" "+" -c "+cacheModel
    cmd = "build/X86/gem5.opt configs/IBLP/ruby_config.py "+args
    out = subprocess.check_output(cmd, shell=True, cwd="../gem5")
    return out.decode('utf-8').split("\n")[-1]

# execution & analysis
options = parser.parse_args()
trials = int(options.trials)
results = {"Item": {"Miss rate":0},
           "Block": {"Miss rate":0},
           "IBLP": {"Item layer miss rate":0, "Block layer miss rate":0}}

for cache in options.cache_models:
    for i in range(trials):
        run_config(options.binary, cache)
        # check stats.txt result
        f = open("/home/alan/Documents/thesis/gem5/m5out/stats.txt")
        lines = f.readlines()
        if cache == "IBLP":
            results[cache]["Item layer miss rate"] += float(lines[411].split()[1])   # line 412, system.l2cache.overallMissRate::total
            results[cache]["Block layer miss rate"] += float(lines[519].split()[1])  # line 520, system.l2cache.blockLayer.overallMissRate::total
        else:
            results[cache]["Miss rate"] += float(lines[411].split()[1])   # line 412, system.l2cache.overallMissRate::total
    results[cache] = {k : results[cache][k]/trials for k in results[cache].keys()}

print()
for k in results:
    print(k, ":", results[k])
