#!/usr/bin/env python3
import re
import sys
README = """
This program reads a planning text file and looks for occurences of any of the following:
    - (\d days) -- essential work, no work range.
    - (\d - \d days) -- essential work, variable range.
    - (\d NTHdays) -- nice to have work, no range.
    - (\d - \d NTHdays) -- nice to have work, variable range.
"""

# input validation
if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help", "-help"):
    print(README)
    print("{} <planning_file.md>".format(sys.argv[0]))
    exit(1)

# regex to extract day estimates of out text file.
days_regex = re.compile(
    "(?P<min>\\d+)(?:-(?P<max>\\d+))? (?P<day_type>(?:NTH)?days)")

# counters
min_days = 0
max_days = 0

min_nth_days = 0
max_nth_days = 0

with open(sys.argv[1], "r") as planning_file:
    for line in planning_file:
        days_match = days_regex.search(line)

        if days_match:
            mind = int(days_match.group("min"))
            maxd = days_match.group("max")

            # normalize max to equal min if it isn't set.
            if not maxd:
                maxd = mind
            maxd = int(maxd)

            # sort by days and "Nice To Have (NTH)" days.
            day_type = days_match.group("day_type")
            if day_type == "days":
                min_days += mind
                max_days += maxd
            elif day_type == "NTHdays":
                min_nth_days += mind
                max_nth_days += maxd

# convert to week estimates
min_weeks = round(min_days / 5)
max_weeks = round(max_days / 5)
min_months = round(min_days / 20)
max_months = round(max_days / 20)

min_nth_weeks = round(min_nth_days / 5)
max_nth_weeks = round(max_nth_days / 5)
min_nth_months = round(min_nth_days / 20)
max_nth_months = round(max_nth_days / 20)


# print it all
print()
print("Project Estimate For One Developer:")
print("\t{} - {} days".format(
    min_days, max_days))
print("\t{} - {} weeks(5 days / week)".format(min_weeks, max_weeks))
print("\t{} - {} months(20 days / month)".format(min_months, max_months))

print("Nice To Have:")
print("\t{} - {} days".format(min_nth_days, max_nth_days))
print("\t{} - {} weeks".format(min_nth_weeks, max_nth_weeks))
print("\t{} - {} months(20 days / month)".format(min_nth_months, max_nth_months))
print()
