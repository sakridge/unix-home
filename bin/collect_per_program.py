import sys
import re

timings = {}
with open(sys.argv[1]) as fh:
    for line in fh.readlines():
        if "per_program_timings" in line:
            m = re.search(r'pubkey=\"(.+)\"', line)
            if m:
                pubkey = m.group(1)
            else:
                print(line)
            m = re.search(r'execute_us=(\d+)', line)
            if m:
                execute_us = int(m.group(1))
            m = re.search(r'count=(\d+)', line)
            if m:
                count = int(m.group(1))
            if not pubkey in timings:
                timings[pubkey] = [0, 0]
            timings[pubkey][0] += count
            timings[pubkey][1] += execute_us

timings_as_list = []
for pubkey in timings:
    timings_as_list.append([pubkey, timings[pubkey][0], timings[pubkey][1]])
timings_as_list.sort(key=lambda tup: tup[1])

for e in timings_as_list:
    print("{} execute_us: {} count: {}".format(e[0], e[1], e[2]))
