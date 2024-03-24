#!/usr/bin/env python3

import json
import sys

if len(sys.argv) < 3:
    print("Error:! Too few arguments: Usage: find-stake-account.py <stakes-json-file> [<list of pubkeys>]")
    exit(1)

target_keys = {}
for key in sys.argv[2:]:
    target_keys[key] = True
with open(sys.argv[1]) as fh:
    json = json.load(fh)

def pretty_bs58(key):
    return "{:<44}".format(key)
    digits_to_print = 8
    return key[:digits_to_print] + "..." + key[len(key) - digits_to_print:]

lines_to_print = []
for entry in json:
    do_print = None
    target_key = ""
    if entry['staker'] in target_keys:
        do_print = 'staker'
        target_key = entry['staker']
    if 'delegatedVoteAccountAddress' in entry and entry['delegatedVoteAccountAddress'] in target_keys:
        do_print = 'delegated vote'
        target_key = entry['delegatedVoteAccountAddress']
    if entry['withdrawer'] in target_keys:
        do_print = 'withdrawer'
        target_key = entry['withdrawer']
    if do_print:
        lines_to_print.append("{:<45} {:<20} {:<45} {:<45} {:,.3f}".format(pretty_bs58(target_key), do_print, pretty_bs58(entry['staker']), pretty_bs58(entry['stakePubkey']), entry['accountBalance'] / 1000000000))

if len(lines_to_print) > 0:
    print("target keys:")
    for key in target_keys:
        print("  {}".format(key))
    print("{:<45} {:<20} {:<45} {:<45} {:<10}".format('target-key', 'type', 'special-key', 'account-key', 'balance'))
    for line in lines_to_print:
        print(line)
