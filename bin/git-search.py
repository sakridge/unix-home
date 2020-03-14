#!/usr/bin/env python3

import subprocess
import re
import sys

if len(sys.argv) != 2:
    print("Usage: gb.py <branch>")
    exit(1)

def update_lines(num, lines, line):
    if not num in lines:
        lines[num] = []
    lines[num].append(line)

branch = subprocess.check_output(["git", "branch"])
lines = {}
for branch_line in branch.splitlines():
    branch_line = branch_line.decode("utf-8")
    branch_line = branch_line.strip('\*')
    branch = branch_line.strip()
    log_lines = subprocess.check_output(["git", "log", "-p", branch + "@{u}.." + branch])
    for log_line in log_lines.splitlines():
        log_line = log_line.decode("utf-8")
        if sys.argv[1] in log_line:
            print(branch + "  :  " + log_line)
