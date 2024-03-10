import shutil
import os
import subprocess

here = os.getcwd()
local_config = "/ruby_config"
run_file = "/simple_ruby.py"

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

def run_config():
    cmd = "build/X86_MSI/gem5.opt configs" + local_config + run_file
    out = subprocess.check_output(cmd, shell=True, cwd="./gem5")
    print(out.decode('utf-8').split("\n")[-1])

push_files()
run_config()
