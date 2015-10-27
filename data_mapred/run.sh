#!/bin/bash

#20419 is ave num of flights per day
#5m is 80%
for i in $(seq 10 100 500)
	do
		echo $i
		python mapper.py $i | python reducer.py
	done