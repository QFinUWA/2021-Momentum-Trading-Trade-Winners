#!/bin/bash

# the maximum value for the lookback window of the long moving average
MAX_LONG=7

for long in $(seq 3 $MAX_LONG)
do
	for mid in $(seq 2 $[long-1])
	do
		for short in $(seq 1 $[mid-1])
		do
			echo "$short-$mid-$long"
		done
	done
done