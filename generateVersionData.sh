#!/bin/sh
touch versionData.json

fullBranch="$3"

if [ "$fullBranch" = "dev" ]; then
    	fullBranch="$3 (build: $4)"
fi

{
    	echo "{"
    	echo "\"type\": \"$1\","
	echo "\"version\": \"$2\","
	echo "\"branch\": \"$fullBranch\""
    	echo "}"
} > versionData.json