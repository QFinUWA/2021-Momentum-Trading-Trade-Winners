#!/bin/bash

# make results folder if it doesn't exist
RESULTS_FOLDER="results"
mkdir $RESULTS_FOLDER

# make a folder for the current time
OUTPUT_FOLDER="$RESULTS_FOLDER/$(date +%d)th-$(date +%T)"
echo "saving output in: $OUTPUT_FOLDER"
mkdir $OUTPUT_FOLDER

# the maximum value for the lookback window of the long moving average
MAX_LONG=4

NUM_CONFIGS=$((((MAX_LONG-2)*(MAX_LONG-1)*(MAX_LONG))/6))
COUNT=1

for long in $(seq 3 $MAX_LONG)
do
	for mid in $(seq 2 $[long-1])
	do
		for short in $(seq 1 $[mid-1])
		do
			FILENAME=$(printf "%02d-%02d-%02d" $short $mid $long)
			FILEPATH="$OUTPUT_FOLDER/$FILENAME"

			echo -en $(printf "%3d/%3d\r" $COUNT $NUM_CONFIGS)
			python3 example.py $short $mid $long > $FILEPATH
			COUNT=$((COUNT+1))
		done
	done
done

# spd-say "script finished"