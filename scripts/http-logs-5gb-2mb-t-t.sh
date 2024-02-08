#!/bin/bash

host="" # Ensure that port is provided for opensource OpenSearch clusters
workload="http_logs"
tasks="delete-index,create-index,check-cluster-health,index-append,desc_sort_size,asc_sort_size,desc_sort_timestamp,asc_sort_timestamp,desc_sort_with_after_timestamp,asc_sort_with_after_timestamp,desc-sort-timestamp-after-force-merge-1-seg,asc-sort-timestamp-after-force-merge-1-seg,desc-sort-with-after-timestamp-after-force-merge-1-seg,asc-sort-with-after-timestamp-after-force-merge-1-seg"
id="http_logs_5gb_2mb_t_t_$(date +"%Y_%m_%d_%I_%M_%p")"
daily_snapshot_name="traditional_http_logs_runs_$(date +"%Y_%m_%d_%I_%M")"
#workload_params_raw='{"snapshot_repo_name":"benchmark-workloads-repo","snapshot_bucket_name":"benchmark-data-snapshots","snapshot_region":"us-west-2","snapshot_base_path":"workload-snapshots","snapshot_name":"temporary_name"}'
workload_params_raw='{"snapshot_repository_name":"benchmark-workloads-repo","snapshot_name":"temporary_name"}'
workload_params="${workload_params_raw//\"temporary_name\"/\"$daily_snapshot_name\"}"

sudo docker run -v /home/ec2-user/benchmark-data/:/opensearch-benchmark/.benchmark/ opensearchproject/opensearch-benchmark:latest execute-test --workload=$workload --pipeline=benchmark-only --target-hosts=$host --telemetry=node-stats --test-execution-id=$id --user-tag=test-type:http-logs-5gb-2mb-t-t --workload-params=$workload_params --workload-repository=hoangia  > /home/ec2-user/benchmark-data/"http-logs-$(date +"%Y_%m_%d_%I_%M_%p").log"
