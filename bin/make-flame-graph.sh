#!/bin/bash

sudo perf script > perf-script.out
cat perf-script.out | ~/src/FlameGraph/stackcollapse-perf.pl > perf-folded.out
cat perf-folded.out | cppfilt > perf-cppfilt.out
cat perf-cppfilt.out | rust-unmangle > perf-cppfilt-rust.out
~/src/FlameGraph/flamegraph.pl perf-cppfilt-rust.out > flame.svg
