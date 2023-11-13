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
parser.add_argument("--item_layer_size", "-i",
                    help="Size of item-granularity layer of L2 cache (in kB).",
                    type=int,
                    default=128)
parser.add_argument("--block_layer_size", "-b",
                    help="Size of block-granularity layer of L2 cache (in kB).",
                    type=int,
                    default=128)
parser.add_argument("--cache_model", "-c",
                    nargs="?",
                    help="Which cache model to test",
                    type=str,
                    choices=["Item", "Block", "IBLP"],
                    default=["Item"])

options = parser.parse_args()

system = System()
system.setup_caches(options.cache_model)    # options.item_layer_size, options.block_layer_size
system.setup_memory()
system.run(options.binary)
