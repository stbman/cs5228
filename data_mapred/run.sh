#!/bin/bash

for i in $(seq 20 20 10000)
	do
		echo $i
		python mapper.py $i | python reducer.py
	done