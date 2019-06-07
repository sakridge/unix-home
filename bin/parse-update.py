#!/usr/bin/env python

import re
import sys

total = 0
num = 0
with open(sys.argv[1]) as fh:
    for line in fh:
        if re.search('txs_len: 240', line):
            split = re.search('update_index: (\d+)', line)
            print(split.group(1))
            #total += int(split[5])
            num += 1
            #print split[1]
print("total: {} average: {}".format(num, total / num)) 
