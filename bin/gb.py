#!/usr/bin/env python3

import subprocess
import re
import sys

def update_lines(num, lines, line):
    if not num in lines:
        lines[num] = []
    lines[num].append(line)

branch = subprocess.check_output(["git", "branch", "-vv"])
lines = {}
for line in branch.splitlines():
    line = line.decode("utf-8")
    if sys.argv[1] in line:
        m = re.search(r'behind ([0-9]+)', line);
        if m:
            #print(m.group(1))
            line_num = int(m.group(1))
            update_lines(-line_num, lines, line)
        else:
            m = re.search(r'ahead ([0-9]+)', line);
            if m:
                line_num = int(m.group(1))
                update_lines(line_num, lines, line)
            else:
                update_lines(0, lines, line)

for key in sorted(lines.keys()):
    for line in lines[key]:
        print(line)

