#!/usr/bin/env python3

import sys

nums = sys.argv[1].split(",")
total = 0
for num in nums:
    total += int(num)
print("total: {} average: {} number: {}".format(total, total / len(nums), len(nums)))
