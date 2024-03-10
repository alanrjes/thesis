import sys
import os
import argparse
import shutil
import linecache
import subprocess

# args for running tests
parser = argparse.ArgumentParser(description="")
parser.add_argument("binary",
                    nargs="?",
                    type=str,
                    help="Path to the binary to execute.",
                    default="tests/test-progs/hello/bin/x86/linux/hello")
parser.add_argument("--trials", "-t",
                    type=int,
                    help="Number of trials to run per cache type.",
                    default=1)

options = parser.parse_args()

here = os.getcwd()
local_config = "/classic_config"
run_file = "/config.py"

# copy files to draft and config subdirectories
def push_files():
    # check gem5 configs subdirectory for appropriate folder
    if not os.path.isdir(here + "/gem5/configs" + local_config):
        os.mkdir(here + "/gem5/configs" + local_config)

    files = os.listdir(here + local_config)
    for fname in files:
        # copy to Gem5 configs subdirectory
        shutil.copy(here + local_config + "/" + fname, here + "/gem5/configs" + local_config)
        # copy to draft subdirectory
        shutil.copy(here + local_config + "/" + fname, here + "/draft/code" + local_config)

# run gem5 config for some particular cache model
def run_config(binary, cacheType):
    cmd = "build/X86/gem5.opt configs/classic_config/config.py "+binary+" -c "+cacheType
    out = subprocess.check_output(cmd, shell=True, cwd="./gem5")
    return out.decode('utf-8').split("\n")[-1]

push_files()

# execution & analysis
options = parser.parse_args()
trials = int(options.trials)
results = {"Item": {"Miss rate":0},
           "Block": {"Miss rate":0},
           "IBLP": {"Item layer miss rate":0, "Block layer miss rate":0}}

for cache in ["Item", "Block", "IBLP"]:
    for i in range(trials):
        run_config(options.binary, cache)
        # check gem5/m5out/stats.txt result
        f = open("/home/alan/Documents/thesis/gem5/m5out/stats.txt")
        lines = f.readlines()
        if cache == "IBLP":
            # item layer:
            results[cache]["Item layer miss rate"] += float(lines[411].split()[1])   # line 412, system.l2cache.overallMissRate::total
            l = lines[519].split() # line 520, system.l2cache.blockLayer.overallMissRate::total
            assert l[0] == "system.l2cache.blockLayer.overallMissRate::total", "Stats.txt did not record block cache correctly"
            results[cache]["Block layer miss rate"] += float(l[1])
        else:
            results[cache]["Miss rate"] += float(lines[411].split()[1])   # line 412, system.l2cache.overallMissRate::total
    results[cache] = {k : results[cache][k]/trials for k in results[cache].keys()}

print()
for k in results:
    print(k, ":", results[k])
