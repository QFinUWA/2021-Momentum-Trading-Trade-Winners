#!/bin/bash

WEBHOOK_URL="https://discord.com/api/webhooks/880037779256533022/eE9LHFeC0UjulGThK_GJ4hk4SA3io32h5OuEufp7woQbgL42N9vKtseq0bLFdWIn_pBM"

PYTHON_SCRIPT="example.py"
ANALYSIS_SCRIPT="analysis.py"

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

# make a file for the analysis
ANALYSIS_NAME="analysis.txt"
ANALYSIS_PATH="$OUTPUT_FOLDER/$ANALYSIS_NAME"

# the maximum value for the lookback window of the LONG moving average
MAX_LONG=32
MIN_LONG=10

# the number of configuations is the sum of the first n triangle numbers
NUM_CONFIGS=$((((MAX_LONG-2)*(MAX_LONG-1)*(MAX_LONG))/6))

NUM_THREADS=3
NUM_BATCHES=$((($NUM_CONFIGS+$NUM_THREADS-1)/$NUM_THREADS))

echo "$NUM_BATCHES batches and $NUM_CONFIGS configurations to search..."
echo "using $NUM_THREADS threads"
echo ""
echo "SIGKILL the program to quit (don't cntrl+c)"
echo ""
echo "running the program and generating results"

COUNT=1
for LONG in $(seq $MIN_LONG $MAX_LONG)
do
	for MID in $(seq $[MIN_LONG-1] $[LONG-1])
	do
		for SHORT in $(seq $[MIN_LONG-2] $[MID-1])
		do
			# uses temp files to store intermediate results
			FILENAME=$(printf "%02d-%02d-%02d" $SHORT $MID $LONG)
			FILEPATH="$OUTPUT_FOLDER/$FILENAME"

			# ceil(count/6)
			BATCH_COUNT=$((($COUNT+$NUM_THREADS-1)/$NUM_THREADS))

			# run the program and output to a file
			python3 $PYTHON_SCRIPT $SHORT $MID $LONG > $FILEPATH &

			if [[ $(( COUNT % NUM_THREADS )) == 0 ]]; then
				echo -en $(printf "%3d/%3d\r" $BATCH_COUNT $NUM_BATCHES)
				sleep 1
				wait
			fi

			# iterate count
			COUNT=$(($COUNT+1))
		done
	done
done

# waits for 'left-over' processes
# in case number of thread isn't a factor of the configs
echo -en $(printf "%3d/%3d\r" $NUM_BATCHES $NUM_BATCHES)
wait

echo "filtering the data"

COUNT=1
for LONG in $(seq $MIN_LONG $MAX_LONG)
do
	for MID in $(seq $[MIN_LONG-1] $[LONG-1])
	do
		for SHORT in $(seq $[MIN_LONG-2] $[MID-1])
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

echo "running analysis"

python3 $ANALYSIS_SCRIPT $OUTPUT_PATH > $ANALYSIS_PATH

CONTENT="sweep finished\n swept from $MIN_LONG : $MAX_LONG"
curl \
-d '{"content": '"\"$CONTENT\""'}' \
-H "Content-Type: application/json" \
-X POST $WEBHOOK_URL
