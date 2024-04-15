#!/bin/bash

for i in {0..10}; do
	echo "Iteration $i"
	bash ingestion-and-sorts-only.sh
	echo "Sleeping for 5 minutes"
	sleep 300
done
