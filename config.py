# located in gem5/configs/IBLP

import argparse
from system import StreamlinedSystem as System

# execution parameters
parser = argparse.ArgumentParser(description="Config for a simple model of an item-block layered cache.")
parser.add_argument("binary",
                    nargs="?",
                    type=str,
                    help="Path to the binary to execute.",
                    default="tests/test-progs/hello/bin/x86/linux/hello")
parser.add_argument("--cache_model", "-c",
                    nargs="?",
                    help="Which cache model to test",
                    type=str,
                    choices=["Item", "Block", "IBLP"],
                    default=["Item"])

args = parser.parse_args()

system = System()
system.setup_caches(args.cache_model)
system.setup_memory()
system.run(args.binary)
