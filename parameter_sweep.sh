#!/bin/bash

# set up venv and talib library paths
source bin/activate
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# make results folder if it doesn't exist
RESULTS_FOLDER="results"
mkdir $RESULTS_FOLDER

# make a folder for the current time
OUTPUT_FOLDER="$RESULTS_FOLDER/$(date +%d)th-$(date +%T)"
echo "saving output in: $OUTPUT_FOLDER"
mkdir $OUTPUT_FOLDER

OUTPUT_NAME="output.txt"
OUTPUT_PATH="$OUTPUT_FOLDER/$OUTPUT_NAME"

touch $OUTPUT_PATH

# the maximum value for the lookback window of the LONG moving average
MAX_LONG=4

# the number of configuations is the sum of the first n triangle numbers
NUM_CONFIGS=$((((MAX_LONG-2)*(MAX_LONG-1)*(MAX_LONG))/6))

echo "running the program and generating results"

COUNT=1
for LONG in $(seq 3 $MAX_LONG)
do
	for MID in $(seq 2 $[LONG-1])
	do
		for SHORT in $(seq 1 $[MID-1])
		do
			# uses temp files to store intermediate results
			FILENAME=$(printf "%02d-%02d-%02d" $SHORT $MID $LONG)
			FILEPATH="$OUTPUT_FOLDER/$FILENAME"

			# print progress
			# not relevant rn since all are in parallel
			# echo -en $(printf "%3d/%3d\r" $COUNT $NUM_CONFIGS)

			# run the program and output to a file
			python3 example.py $SHORT $MID $LONG > $FILEPATH &

			# iterate count
			COUNT=$((COUNT+1))
		done
	done
done

wait

echo "filtering the data"

COUNT=1
for LONG in $(seq 3 $MAX_LONG)
do
	for MID in $(seq 2 $[LONG-1])
	do
		for SHORT in $(seq 1 $[MID-1])
		do
			# uses temp files to store intermediate results
			FILENAME=$(printf "%02d-%02d-%02d" $SHORT $MID $LONG)
			FILEPATH="$OUTPUT_FOLDER/$FILENAME"

			# print progress
			echo -en $(printf "%3d/%3d\r" $COUNT $NUM_CONFIGS)

			# Does the following:
			# 1. removes non-numeric characters
			# 2. removes banners with the minus sign
			# 3. removes empty lines
			# 4. append output to the output file
			cat $FILEPATH \
			 | sed 's/[^-.%0-9]*//g'  \
			 | sed '/--/d' \
			 | sed '/^[[:space:]]*$/d' \
			 >> $OUTPUT_PATH

			# iterate count
			COUNT=$((COUNT+1))
		done
	done
done

echo "removing temporary files"

rm $OUTPUT_FOLDER/[0-9]*

spd-say "script finished"