#!/bin/bash

usage() {
    echo "Usage: $0 -h HOST -i ID [-f flag for updating floor segment size] [-s flag for updating segment size] [-m flag for merge policy to log_byte_size] [-t flag for setting segments per tier to 5]"
}

err_exit() {
    echo "${0##*/}: $1" >&2
    exit 1
}

update_max_merged_segment() {
  echo "Updating max merged segment to 2gb"

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
}

update_floor_segment_size() {
  echo "Updating floor segment size to 500mb"

  response=$(curl --write-out '%{http_code}' --silent --output /dev/null \
    -XPUT "${host}/logs-241998/_settings" \
    -H 'Content-Type: application/json' \
    -d '{
      "index" : {
        "merge.policy.floor_segment": "500mb"
      }
    }')

  if [ "$response" -eq 200 ]; then
      echo "Success! The response code was 200 (OK)."
  else
      echo "Error: The response code was $response."
      exit 1
  fi
}

update_merge_policy_to_log_byte_size() {
  echo "Updating merge policy to log_byte_size"

  response=$(curl --write-out '%{http_code}' --silent --output /dev/null \
    -XPUT "${host}/_cluster/settings" \
    -H 'Content-Type: application/json' \
    -d '{
      "indices" : {
          "time_series_index.default_index_merge_policy": "log_byte_size"
      }
    }')

  if [ "$response" -eq 200 ]; then
      echo "Success! The response code was 200 (OK)."
  else
      echo "Error: The response code was $response."
      exit 1
  fi
}

update_segments_per_tier() {
  echo "Update segments per tier to 5"

  response=$(curl --write-out '%{http_code}' --silent --output /dev/null \
    -XPUT "${host}/logs-241998/_settings" \
    -H 'Content-Type: application/json' \
    -d '{
      "index" : {
        "merge.policy.segments_per_tier": "5"
      }
    }')

  if [ "$response" -eq 200 ]; then
      echo "Success! The response code was 200 (OK)."
  else
      echo "Error: The response code was $response."
      exit 1
  fi
}

# Initialize variables
host=""
id=""
floor_segment_size=false
segment_size=false
merge_policy=false
segments_per_tier=false

# Parse command-line options
while getopts ":h:i:fsmt" opt; do
    case $opt in
        h)
            host=$OPTARG
            ;;
        i)
            id=$OPTARG
            ;;
        f)
            floor_segment_size=true
            ;;
        s)
            segment_size=true
            ;;
        m)
            merge_policy=true
            ;;
        t)
            segments_per_tier=true
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            usage
            exit 1
            ;;
    esac
done

# Shift the argument pointer to skip the processed options
shift $((OPTIND - 1))

# Check if required options are provided
if [ -z "$host" ] || [ -z "$id" ]; then
    echo "The -h and -i options are required." >&2
    usage
    exit 1
fi

# Check if at least one of -f, -s, or -m is provided
if [ "$floor_segment_size" = false ] && [ "$segment_size" = false ] && [ "$merge_policy" = false ] && [ "$segments_per_tier" = false ]; then
    echo "At least one of -f, -s, -m, or -t must be provided." >&2
    usage
    exit 1
fi

echo "Running update on $host for $id."

# Check which flags were provided
if $floor_segment_size; then
    echo "Flag -f was provided."
    update_floor_segment_size
fi

if $segment_size; then
    echo "Flag -s was provided."
    update_max_merged_segment
fi

# Merge policy can only be set before creating index since it sets the cluster settings. Merge policy cannot be changed for already existing indices.
# This will give a 400 validation error: cluster setting is not updatable. This is because the documentation is incorrect and the log byte merge policy cannot be set on a cluster level settings. It must be set at index creation on the index level. Best way to do this is to use OSB and update the index.json to include the merge policy
if $merge_policy; then
    echo "Flag -m was provided."
    update_merge_policy_to_log_byte_size
fi

if $segments_per_tier; then
    echo "Flag -t was provided."
    update_segments_per_tier
fi

echo "Checking Settings"
check_settings=$(curl -XGET "${host}/logs-241998/_settings?pretty")
echo $check_settings > $id-index-settings.json

echo "Finished checking settings"
