#!/usr/bin/env python3
#from dateutil import parser
from datetime import datetime

import json
import sys
import re

def get_time(line):
    split = line.split(" ")
    time_str = split[0].strip("[")
    #parser.parse(time_str)
    # datetime doesn't support ns, so remove those
    time_str = time_str[:-4]
    return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")

all_slots = {}
data = {}
for input_file in sys.argv[1:]:
    data[input_file] = {}
    data[input_file]['slots_full'] = {}
    data[input_file]['slots_frozen'] = {}
    data[input_file]['slots_voted'] = {}
    data[input_file]['slots_new_fork'] = {}
    data[input_file]['slots_retransmit'] = {}
    data[input_file]['slots_new_root'] = {}
    print("processing {}".format(input_file))
    with open(input_file) as fh:
        for line in fh.readlines():
            if "is full" in line:
                time = get_time(line)
                m = re.search(r"slot (\d+) is full", line)
                slot = int(m.group(1))
                all_slots[slot] = True
                data[input_file]['slots_full'][slot] = time
            elif "bank frozen" in line and "replay_stage" in line:
                m = re.search(r"bank frozen: (\d+)", line)
                slot = int(m.group(1))
                time = get_time(line)
                all_slots[slot] = True
                data[input_file]['slots_frozen'][slot] = time
            elif "voting:" in line:
                m = re.search(r"voting: (\d+)", line)
                slot = int(m.group(1))
                time = get_time(line)
                all_slots[slot] = True
                data[input_file]['slots_voted'][slot] = time
            elif "new fork:" in line:
                m = re.search(r"new fork:(\d+)", line)
                slot = int(m.group(1))
                time = get_time(line)
                all_slots[slot] = True
                data[input_file]['slots_new_fork'][slot] = time
            elif "packets_by_slot" in line:
                retransmit_time = get_time(line)
                line_split = line.split("packets_by_slot:")
                if "," in line_split[1]:
                    items = line_split[1].split(",")
                    for item in items:
                        item = item.strip(" \n")
                        item = item.strip("\{")
                        item = item.strip("\}")
                        #print(item)
                        #print(line)
                        slot_and_count = item.split(":")
                        slot = int(slot_and_count[0])
                        count = int(slot_and_count[1])
                        if not (slot in data[input_file]['slots_retransmit']):
                            data[input_file]['slots_retransmit'][slot] = retransmit_time
            elif "new root" in line:
                m = re.search(r"new root (\d+)", line)
                slot = int(m.group(1))
                time = get_time(line)
                all_slots[slot] = True
                data[input_file]['slots_new_root'][slot] = time

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

def pretty_time(time):
    #return datetime.strftime(time, "%d %H:%M:%S.%f")
    return datetime.strftime(time, "%H:%M:%S")

def print_time(time):
    print("{:10}".format(pretty_time(time)), end=" ")

for (file_name, entry) in data.items():
    print("{:88}".format(file_name[:5]), end=" | ")
print("")
for slot in sorted(all_slots.keys()):
    print("slot {}".format(slot), end=" ")
    for (file_name, entry) in data.items():
        if slot in entry['slots_full']:
            time = entry['slots_full'][slot]
            print("full: {:10}".format(pretty_time(time)), end=" ")
        else:
            print("no_full{:9}".format(""), end=" ")
        if slot in entry['slots_retransmit']:
            time_retransmit = entry['slots_retransmit'][slot]
            #if slot in entry['slots_full']:
            #    diff = entry['slots_full'][slot] - time_retransmit
            #    print("retransmit(d): {}".format(pretty_time_delta(diff)), end=" ")
            #else:
            #    print("retransmit: {}".format(pretty_time(time_retransmit)), end=" ")
            print_time(time_retransmit)
        else:
            print("no_retrans", end=" ")
        if slot in entry['slots_new_fork']:
            time_new_fork = entry['slots_new_fork'][slot]
            #if slot in entry['slots_full']:
            #    diff = time_new_fork - entry['slots_full'][slot]
            #    print("new_fork: {}".format(pretty_time_delta(diff)), end=" ")
            print_time(time_new_fork)
        else:
            print("no new_for", end=" ")
        if slot in entry['slots_frozen']:
            time_frozen = entry['slots_frozen'][slot]
            #if slot in entry['slots_new_fork']:
            #    diff = time_frozen - entry['slots_new_fork'][slot]
            #elif slot in entry['slots_retransmit']:
            #    diff = time_frozen - entry['slots_retransmit'][slot]
            #else:
            #    diff = time_frozen - entry['slots_full'][slot]
            #print("frozen: {}".format(pretty_time_delta(diff)), end=" ")
            print_time(time_frozen)
        else:
            print("no frozen ", end=" ")
        if slot in entry['slots_voted']:
            time_voted = entry['slots_voted'][slot]
            #diff = None
            #if slot in entry['slots_frozen']:
            #    diff = time_voted - entry['slots_frozen'][slot]
            #else:
            #    diff = time_voted - entry['slots_full'][slot]
            #print("voted: {}".format(pretty_time_delta(diff)), end=" ")
            print_time(time_voted)
        else:
            print("no voted  ", end=" ")
        if slot in entry['slots_new_root']:
            time_rooted = entry['slots_new_root'][slot]
            print_time(time_rooted)
        else:
            print("no root   ", end=" ")
        #print("{} full: {} frozen: {} voted: {}".format(time, slots_frozen[slot], slots_voted[slot]))
        print("   |   ", end=" ")
    print("")
