#!/usr/bin/env python3

import sys
import csv

versions = {}
ids = {}
with open(sys.argv[1]) as fh:
    csvreader = csv.reader(fh)
    first = None
    for row in csvreader:
        if not first:
            first = 1
            continue
        version = row[2]
        if not version in versions:
            versions[version] = 0
        versions[version] += 1
        the_id = row[1]
        if not the_id in ids:
            ids[the_id] = [0, version]
        ids[the_id][0] += 1

id_list = list(ids.items())
id_list.sort(key=lambda a: a[1][0])
for x in id_list:
    print(x)

#for (v, count) in versions.items():
#    print("{} : {}".format(v, count))
#for (v, count) in ids.items():
#    print("{} : {}".format(v, count))
