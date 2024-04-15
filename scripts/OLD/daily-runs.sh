#!/bin/bash

host="" # Ensure host number is provided if it's an opensource cluster
workload="http_logs"

sudo docker run -v /home/ec2-user/benchmark-data/:/opensearch-benchmark/.benchmark/ opensearchproject/opensearch-benchmark:latest execute-test --workload=$workload --pipeline=benchmark-only --target-hosts=$host > /home/ec2-user/benchmark-data/"$(date +"%Y_%m_%d_%I_%M_%p").log"

