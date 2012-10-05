#!/usr/bin/python

import subprocess

proc = subprocess.Popen(['p4','client', '-o'], shell=False, stdout=subprocess.PIPE)
stdo, stde = proc.communicate()
p4_client = ""
for line in stdo.splitlines():
    if ("Client:" in line):
        p4_client = line.split(":")[1].strip()

subprocess.call(['p4', 'changes', '-m1', '...@' + p4_client])
