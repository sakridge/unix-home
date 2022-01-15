#!/bin/bash

#cppfilt install:
# cargo install cpp_demangle --example cppfilt
# from https://github.com/gimli-rs/cpp_demangle

# src/FlameGraph from github: https://github.com/brendangregg/FlameGraph

# rust-unmangle from github:
# https://github.com/Yamakaky/rust-unmangle

sudo perf script > perf-script.out
cat perf-script.out | ~/src/FlameGraph/stackcollapse-perf.pl > perf-folded.out
cat perf-folded.out | cppfilt > perf-cppfilt.out
cat perf-cppfilt.out | rust-unmangle > perf-cppfilt-rust.out
~/src/FlameGraph/flamegraph.pl perf-cppfilt-rust.out > flame.svg
