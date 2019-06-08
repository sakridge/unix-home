#!/usr/bin/env python

from __future__ import print_function
import re
import sys

total = 0
num = 0
re_field_str = '{}: (\d+)'.format(sys.argv[1])
print(re_field_str)
field = re.compile(re_field_str)
re_filter = re.compile('recordable: (\d+)')
total_txs = 0
max_speed = 0
min_speed = 100000000
speeds = []
with open(sys.argv[2]) as fh:
    for line in fh:
        m = re_filter.search(line)
        if m:
            num_txs = int(m.group(1))
            if num_txs > 100:
                total_txs += num_txs
                split = field.search(line)
                #print(line)
                time = int(split.group(1))
                total += time
                num += 1
                #print split[1]
                speed = float(time) / num_txs
                if speed < min_speed:
                    min_speed = speed
                if speed > max_speed:
                    max_speed = speed
                speeds.append(speed)

print("total_txs: {:,} total: {:,} average: {:0,.2f}".format(total_txs, num, float(total) / total_txs)) 
print("  min: {} max: {}".format(min_speed, max_speed))
print_speeds = False
if print_speeds:
    speeds.sort()
    i = 0
    for speed in speeds:
        print("{:0,.2f}  ".format(speed), end='')
        i += 1
        if i % 10 == 0:
            print("")
