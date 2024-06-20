#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Error, please provide comma-separated list of numbers: 1,2,3")
    exit(1)

nums = sys.argv[1].split(",")
total = 0
for num in nums:
    total += int(num)
print("total: {} average: {} number: {}".format(total, total / len(nums), len(nums)))
