#!/usr/bin/env python3

import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Sort and display metrics queries')
parser.add_argument('metrics_file', type=str, help='Path to the metrics json file')
parser.add_argument('validators_file', type=str, help='Path to the json file as a result of solana validators --output=json command')
parser.add_argument('--print-sql', action='store_true', help='Print the sql for the validators')
parser.add_argument('--verbose', action='store_true', help='Print the validator and stake list')
parser.add_argument('--limit-num-validators', type=int, help='Only consider the first <n> validators')

args = parser.parse_args()

metrics_file = args.metrics_file
validators_file = args.validators_file

with open(validators_file) as fh:
    validators_json = json.load(fh)

total_stake = 0
with open(metrics_file) as fh:
    metrics_json = json.load(fh)

num_delinquent = 0
num_missing = 0
validators_and_stakes = []
total_found = 0
validator_limit = args.limit_num_validators
print_sql = args.print_sql
first_sql = True
for validator in metrics_json:
    found = False
    for entry in validators_json['validators']:
        if entry['identityPubkey'] == validator:
            validators_and_stakes.append((validator, entry['activatedStake']))
            if entry['delinquent']:
                num_delinquent += 1
            found = True
            break
    if found:
        #print("found {}".format(validator))
        total_found += 1
    else:
        num_missing += 1
        print("not found! {}".format(validator))

validators_and_stakes.sort(key=lambda x: x[1], reverse=True)
if print_sql:
    print("(")
for (validator, stake) in validators_and_stakes[:validator_limit]:
    if args.verbose:
        print("{} {:>15,.1f}".format(validator.ljust(45), stake / 1000000000))
    total_stake += stake
    if print_sql:
        if not first_sql:
            print(" OR")
        else:
            first_sql = False
        print("\"host_id\"=\'{}\'".format(validator), end="")
if print_sql:
    print("\n)")

if validator_limit:
    considered = min(validator_limit, total_found)
else:
    considered = total_found
print("total metrics: {} considered {} total validators: {}".format(len(metrics_json), considered, len(validators_json['validators'])))
print("delinquent: {} missing: {}".format(num_delinquent, num_missing))
print("total stake: {:,.2f} sol {:.2f}%".format(total_stake / 1000000000, 100 * total_stake/validators_json['totalActiveStake']))

