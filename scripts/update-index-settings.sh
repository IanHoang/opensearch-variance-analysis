#!/bin/bash

host=$1
id=$2

echo "Running update on $host for $id"

echo "Updating max merged segment"

response=$(curl --write-out '%{http_code}' --silent --output /dev/null \
  -XPUT "${host}/logs-241998/_settings" \
  -H 'Content-Type: application/json' \
  -d '{
    "index" : {
      "merge.policy.max_merged_segment": "2gb"
    }
  }')

if [ "$response" -eq 200 ]; then
    echo "Success! The response code was 200 (OK)."
else
    echo "Error: The response code was $response."
    exit 1
fi

echo "Updating floor segment"
response_2=$(curl --write-out '%{http_code}' --silent --output /dev/null \
  -XPUT "${host}/logs-241998/_settings" \
  -H 'Content-Type: application/json' \
  -d '{
    "index" : {
      "merge.policy.floor_segment": "500mb"
    }
  }')

if [ "$response_2" -eq 200 ]; then
    echo "Success! The response code was 200 (OK)."
else
    echo "Error: The response code was $response_2."
    exit 1
fi

echo "Checking Settings"
check_settings=$(curl -XGET "${host}/logs-241998/_settings?pretty")
echo $check_settings > $id-index-settings.json

echo "Finished checking settings"
