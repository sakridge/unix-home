#!/usr/bin/env python3
#from dateutil import parser
from datetime import datetime

import sys
import re

def get_time(line):
    split = line.split(" ")
    time_str = split[0].strip("[")
    #parser.parse(time_str)
    # datetime doesn't support ns, so remove those
    time_str = time_str[:-4]
    return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")

slots_full = {}
slots_frozen = {}
slots_voted = {}
slots_new_fork = {}
slots_retransmit = {}
retransmit_time = None
with open(sys.argv[1]) as fh:
    for line in fh.readlines():
        if "is full" in line:
            time = get_time(line)
            m = re.search(r"slot (\d+) is full", line)
            slot = int(m.group(1))
            slots_full[slot] = time
        elif "bank frozen" in line:
            m = re.search(r"bank frozen: (\d+)", line)
            slot = int(m.group(1))
            time = get_time(line)
            slots_frozen[slot] = time
        elif "voting:" in line:
            m = re.search(r"voting: (\d+)", line)
            slot = int(m.group(1))
            time = get_time(line)
            slots_voted[slot] = time
        elif "new fork:" in line:
            m = re.search(r"new fork:(\d+)", line)
            slot = int(m.group(1))
            time = get_time(line)
            slots_new_fork[slot] = time
        elif "packets_by_slot" in line:
            if not "}" in line:
                retransmit_time = get_time(line)
        elif "}" in line and retransmit_time is not None:
            retransmit_time = None
        elif retransmit_time is not None:
            line = line.strip(" ")
            m = re.search("(\d+): ", line)
            if m:
                slot = int(m.group(1))
                if not slot in slots_retransmit:
                    slots_retransmit[slot] = retransmit_time
            else:
                retransmit_time = None

def pretty_time_delta(time_delta):
    seconds = time_delta.total_seconds()
    if seconds > 1 or seconds < -1:
        return '{:.1f}s'.format(seconds)
    millis = seconds * 1000
    if millis > 1 or millis < -1:
        return '{:.1f}ms'.format(millis)
    micros = millis * 1000
    if micros > 1 or micros < -1:
        return '{:.1f}us'.format(micros)
    nanos = micros * 1000
    return '{:.1f}ns'.format(nanos)

for (slot, time) in slots_full.items():
    print("{} full: {}".format(slot, datetime.strftime(time, "%d %H:%M:%S.%f")))
    if slot in slots_retransmit:
        time_retransmit = slots_retransmit[slot]
        diff = slots_full[slot] - time_retransmit
        print("   retransmit: {}".format(pretty_time_delta(diff)))
    if slot in slots_new_fork:
        time_new_fork = slots_new_fork[slot]
        diff = time_new_fork - slots_full[slot]
        print("   new_fork: {}".format(pretty_time_delta(diff)))
    if slot in slots_frozen:
        time_frozen = slots_frozen[slot]
        if slot in slots_new_fork:
            diff = time_frozen - slots_new_fork[slot]
        elif slot in slots_retransmit:
            diff = time_frozen - slots_retransmit[slot]
        else:
            diff = time_frozen - slots_full[slot]
        print("   frozen: {}".format(pretty_time_delta(diff)))
    if slot in slots_voted:
        time_voted = slots_voted[slot]
        diff = time_voted - slots_frozen[slot]
        print("   voted: {}".format(pretty_time_delta(diff)))
    #print("{} full: {} frozen: {} voted: {}".format(time, slots_frozen[slot], slots_voted[slot]))
