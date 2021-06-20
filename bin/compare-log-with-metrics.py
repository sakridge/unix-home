#!/usr/bin/env python3
#from dateutil import parser
from datetime import datetime
from datetime import timedelta
from operator import itemgetter, attrgetter


import csv
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

def update_histogram(value, histogram, precision):
    histogram_bin = int(value / precision)
    if len(histogram) <= histogram_bin:
        histogram.extend([0 for x in range(len(histogram), histogram_bin + 1)])
    histogram[histogram_bin] += 1

def print_sorted_validator_map(validator_map, reverse):
    validator_tuples = list(validator_map.items())
    validator_tuples.sort(key=itemgetter(1), reverse=reverse)

    for (validator, count) in validator_tuples:
        print("{} {:,.1f}".format(validator[:10], count))

slots_a = {}

input_file_a = sys.argv[1]
input_file_b = sys.argv[2]

use_replay_time = True
use_is_full = False
use_replay_full = False
use_replay_details = False

num_shreds = {}
roots = {}
is_full_times = {}
with open(input_file_a) as fh:
    for line in fh.readlines():
        if 'replay-slot-stats' in line:
            m = re.search(r'total_shreds=(\d+)', line)
            total_shreds = m.group(1)
            m = re.search(r'slot=(\d+)', line)
            slot = m.group(1)
            num_shreds[slot] = total_shreds

        if use_is_full:
            if 'shred_insert_is_full' in line:
                time = get_time(line)
                m = re.search(r'slot=(\d+)', line)
                slot = m.group(1)
                slots_a[slot] = time

                m = re.search(r'total_time_ms=(\d+)', line)
                is_full_times[slot] = int(m.group(1))
        else:
            if 'replay-slot-stats' in line:
                if use_replay_time:
                    m = re.search(r'replay_time=(\d+)', line)
                    time = int(m.group(1))
                    if time == 0:
                        continue
                elif use_replay_full:
                    m = re.search(r'execute_us=(\d+)', line)
                    #m = re.search(r'load_us=(\d+)', line)
                    #m = re.search(r'store_us=(\d+)', line)
                    time = int(m.group(1))
                    if time == 0:
                        continue
                elif use_replay_details:
                    #m = re.search(r'deserialize_us=(\d+)', line)
                    #m = re.search(r'serialize_us=(\d+)', line)
                    #m = re.search(r'execute_inner_us=(\d+)', line)
                    m = re.search(r'create_vm_us=(\d+)', line)
                    time = int(m.group(1))
                    if time == 0:
                        continue
                else:
                    time = get_time(line)

                m = re.search(r'slot=(\d+)', line)
                slot = m.group(1)
                slots_a[slot] = time
        if 'new root' in line:
            m = re.search(r'root (\d+)', line)
            slot = m.group(1)
            roots[slot] = True

insert_times_b = {}
slots_b = {}
with open(input_file_b) as fh:
    csv_reader = csv.reader(fh, delimiter=',')
    line = 0
    for row in csv_reader:
        if line != 0:
            #if row[1] == "E7XYctP5NiZE2nE5LzJpGoWVC14kaxjna1DXubTVSmf4" or \
            #   row[1] == "9jJBQ3y8AwubAFBrJrnTnA8Dq2Kd5fXSiLN1RKyTEoQy":
            #    continue
            if use_is_full:
                time = datetime.strptime(row[0][:23], "%Y-%m-%dT%H:%M:%S.%f")
                slot = row[2]
                insert_time = int(row[3])
                if slot in insert_times_b:
                    insert_times_b[slot] += insert_time
                else:
                    insert_times_b[slot] = insert_time
            elif use_replay_time:
                time = int(row[2])
                slot = row[4]
                if time == 0:
                    continue
            elif use_replay_full:
                time = int(row[2]) # execute_us
                #time = int(row[3]) # load_us
                #time = int(row[4]) # store_us
                slot = row[5]
                if time == 0:
                    continue
            elif use_replay_details:
                time = int(row[2]) # create_vm_us
                #time = int(row[3]) # deserialize_us
                #time = int(row[4]) # execute_inner_us
                #time = int(row[5]) # serialize_us
                slot = row[6]
                if time == 0:
                    continue
            else:
                time = datetime.strptime(row[0][:23], "%m/%d/%Y %H:%M:%S.%f")
                #adjust for local time
                time -= timedelta(hours=2)
                #print(time)
                #time = datetime.strptime(row[0], "%m/%d/%Y %H:%M:%S.%f %p")
                slot = row[2]
            if slot in slots_b:
                slots_b[slot].append((time, row[1]))
            else:
                slots_b[slot] = [(time, row[1])]
        line += 1

validator_hist = {}
validator_hist_total = {}
for (slot, validator_list) in slots_b.items():
    validator_list.sort(key=itemgetter(0), reverse=False)

    #sanity check [0] should be the earliest/fastest
    if len(validator_list) > 1:
        assert(validator_list[0][0] <= validator_list[1][0])

        #print("{} {}".format(slot, validator_list))
        validator = validator_list[0][1]
        if not validator in validator_hist:
            validator_hist[validator] = 0
        validator_hist[validator] += 1

    # Update total time list
    for (time, validator) in validator_list:
        if not validator in validator_hist_total:
            validator_hist_total[validator] = [0, 0]
        validator_hist_total[validator][0] += time
        validator_hist_total[validator][1] += 1

print("validator winners:")
print_sorted_validator_map(validator_hist, True)

print("validator avg times:")
validator_hist_avg = {}
for (validator, total) in validator_hist_total.items():
    validator_hist_avg[validator] = total[0] / total[1]

validator_tuples = list(validator_hist_avg.items())
validator_tuples.sort(key=itemgetter(1), reverse=False)

a_total = 0
for time in slots_a.values():
    a_total += time
a_average = a_total / len(slots_a)

a_rank = None
for (i, (validator, count)) in enumerate(validator_tuples):
    if count > a_average and a_rank is None:
        a_rank = i - 1
    print("{:4} {} {:10,.1f}  {}".format(i, validator[:10], count, validator_hist_total[validator][1]))

print("a avg: {:,.1f} total slots: {} rank: {} / {}".format(a_average, len(slots_a), a_rank, len(validator_tuples)))

sorted_slots = list(slots_a.keys())
sorted_slots.sort()

avg_behind_first = 0.0

ahead_count = 0
behind_count = 0

only_roots = False

diff_from_average = 0.0
diff_from_best = 0.0
diff_slots = 0
total_slots = 0

avg_behind_hist = []
avg_behind_hist_precision = 50000

all_histogram = []
all_histogram_precision = 50000

total_num_validators = 0
total_rank = 0
for slot in sorted_slots:
    if only_roots and not (slot in roots):
        continue
    if slot in slots_b:
        total_slots += 1
        time_a = slots_a[slot]
        number_validator = 0
        total_time = 0.0
        rank = None
        using_time = isinstance(time_a, datetime)
        time_b = slots_b[slot][0][0]
        for (time, validator) in slots_b[slot]:
            if not using_time:
                total_time += time
                update_histogram(time, all_histogram, all_histogram_precision)
            else:
                total_time += (time - time_b).total_seconds()
            #if slot == "82058855":
            #    print("{} {} {} rank: {}".format(time_a, time, number_validator, rank))
            if time_a < time and rank is None:
                rank = number_validator
            number_validator += 1
        if rank is None:
            rank = len(slots_b[slot])
        if number_validator > 5:
            total_rank += rank
            total_num_validators += number_validator
            total_num_validators += 1
        average = total_time / number_validator

        update_histogram(average, avg_behind_hist, avg_behind_hist_precision)

        total_validators = len(slots_b[slot])
        if slot in num_shreds:
            slot_shreds = int(num_shreds[slot])
            if slot_shreds > 0:
                sec_per_shred = 100 * average / slot_shreds
            else:
                sec_per_shred = 0
        else:
            slot_shreds = -1
            sec_per_shred = 0
        if number_validator >= 5:
            if using_time:
                diff_from_average += ((time_a - time_b).total_seconds() - average)
            else:
                diff_from_average += (time_a - average)
            diff_slots += 1
        if time_a < time_b:
            #print("{} {} {}".format(slot, time_a, time_b))

            if using_time:
                print("{} ({:8,.1f}ms)  a ahead {} by {} {:4}/{:4}  b: {} ({:6.1f}ms)  average: {:8,.2f}  num_shreds: {:4}  shreds/s: {:7.2f}".format(time_a.strftime("%H:%M:%S"), is_full_times[slot], slot, time_b - time_a, rank, total_validators, time_b.strftime("%H:%M:%S"), insert_times_b[slot] / number_validator, average, slot_shreds, sec_per_shred), end="")
            else:
                print("{:9,}  a ahead {} by {:9,} {:4}/{:4} b: {:9,} avg: {:12,.2f} diff_from_avg: {:11,.2f}".format(time_a, slot, time_b - time_a, rank, total_validators, time_b, average, time_a - average), end="")

            #exit(0)
            ahead_count += 1
        else:
            if use_replay_time or use_replay_full or use_replay_details:
                avg_behind_first += time_a - time_b
            else:
                avg_behind_first += (time_a - time_b).total_seconds()
            behind_count += 1

            if using_time:
                behind_seconds = (time_a - time_b).total_seconds()
                behind_avg = behind_seconds - average
                print("{} ({:8,.1f}ms)  b ahead {} by {} {:4}/{:4}  a: {} ({:6.1f}ms)  average: {:8,.2f} diff_avg: {:8,.2f}  num_shreds: {:4}  shreds/s: {:7.2f}".format(time_b.strftime("%H:%M:%S"), insert_times_b[slot] / number_validator, slot, time_a - time_b, rank, total_validators, time_a.strftime("%H:%M:%S"), is_full_times[slot], average, behind_avg, slot_shreds, sec_per_shred), end='')
            else:
                print("{:9,}  b ahead {} by {:9,} {:4}/{:4} a: {:9,} avg: {:12,.2f} diff_from_avg: {:11,.2f}".format(time_b, slot, time_a - time_b, rank, total_validators, time_a, average, time_a - average), end="")
        if slot in roots:
            print(" R")
        else:
            print(" NR")

    else:
        #print("slot {} not in b".format(slot))
        pass

print("avg histogram:")
for (i, x) in enumerate(avg_behind_hist):
    if x > 0:
        print("{:10,} {:,}".format(i * avg_behind_hist_precision, x))

print("all histogram:")
for (i, x) in enumerate(all_histogram):
    if x > 0:
        print("{:10,} {:,}".format(i * all_histogram_precision, x))


print("behind average: {:,.1f} diff_slots: {} total_slots: {}".format(diff_from_average, diff_slots, total_slots))
print("a ahead: {} b ahead: {}".format(ahead_count, behind_count))
if behind_count > 0:
    print("behind best total:{:,.2f}s average: {:,.2f}s".format(avg_behind_first, avg_behind_first / behind_count))
print("avg rank: {:.2f}".format(100 - 100 * total_rank / total_num_validators))

