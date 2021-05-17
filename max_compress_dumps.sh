#!/bin/bash

for file in ./*.csv.gz
do
	checkstate=`file $file | grep max\ compression | wc -l`
	if [ $checkstate == 0 ]; then
		echo "re-compressing $file..."
		gunzip $file
		gzip -9 ${file%%.gz}
	fi
done
