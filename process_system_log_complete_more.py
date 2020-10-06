#!/usr/bin/env python

import sys, re, csv, operator
from collections import OrderedDict

logfile = sys.argv[1]


per_user = {}
error = {}

with open(logfile) as f:
    for line in f:
        pattern = r"ticky: (?P<logtype>INFO|ERROR) (?P<logmessage>[\w].*)? \((?P<username>[\w]*)\)$"  # Named Capture Groups
        inf = re.findall(pattern, line, re.MULTILINE)
        for logtype, logmessage, username in inf:
            if username not in per_user:
                per_user[username] = {'Username':username, 'INFO':0, 'ERROR':0}

            per_user[username][logtype] += 1   # Sum one to INFO or ERROR counters

        if "ERROR" not in line:
            continue
        pattern = r"ERROR ([\w+ \.]*) \(?"
        result = re.search(pattern, line)
        if result is None:
            continue
        error_name = result[1]
        error[error_name] = error.get(error_name, 0) + 1


per_user =  OrderedDict(sorted(per_user.items(), key=lambda k: k[0]))
for data in per_user.values():
    print(data)

for data in error.items():
    print(data)

error = sorted(error.items(), key = operator.itemgetter(1), reverse=True)
print(error)




with open('user_statistics.csv', 'w') as csvfile:
    fieldnames = ['Username', 'INFO', 'ERROR']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader() # Writes the field names
    for user_data in per_user.values():
      writer.writerow(user_data)

with open('error_message.csv', 'w') as csvfile:
    fieldnames = ['Error', 'Count']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    writer.writerows(error)
