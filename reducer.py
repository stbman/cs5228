#!/usr/bin/python

import sys

sum = 0
count = 0
for line in sys.stdin:
    predicted, actual = line.strip().split(" ")
    count += 1
    sum += (float(actual) - float(predicted))**2

print sum/count
