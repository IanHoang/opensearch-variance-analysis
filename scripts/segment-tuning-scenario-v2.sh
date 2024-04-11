#!/bin/bash
host=""
workload="http_logs"
# No force merge
id="segment-tuning-scenario-5"
tag="test-type:segment-tuning-scenario-5"
workload_params="target_throughput:none,bulk_indexing_clients:1"

err_exit() {
    echo "${0##*/}: $1" >&2
    exit 1
}

mkdir ~/$id

for i in {1..3}
do
    echo "Creating Index"
    run_id="${id}-create-index-only-${i}"
    opensearch-benchmark execute-test --workload=$workload --pipeline=benchmark-only --target-hosts=$host --telemetry=node-stats --test-execution-id=$run_id --workload-params=$workload_params --include-tasks="delete-index,create-index,check-cluster-health"

    echo "Sleeping for 10 seconds"
    sleep 10

    echo "Updating index settings"
    ./update-index-settings-v2.sh -h $host -i $run_id -fst

    echo "Sleeping for 10 seconds"
    sleep 10

    echo "Running Test"
    run_id="${id}-run-${i}"
    opensearch-benchmark execute-test --workload=$workload --pipeline=benchmark-only --target-hosts=$host --telemetry=node-stats --test-execution-id=$run_id --workload-params=$workload_params --include-tasks="check-cluster-health,index-append,desc_sort_size,asc_sort_size,desc_sort_timestamp,asc_sort_timestamp,desc_sort_with_after_timestamp,asc_sort_with_after_timestamp"

    echo "Finished running iteration. Moving test execution file to home directory"
    cp ~/.benchmark/benchmarks/test_executions/$run_id/test_execution.json ~/$run_id.json || err_exit "Cannot cp file $run_id/test_execution.json over to home directory"
    mv ~/$run_id.json ~/$id || err_exit "Cannot move $run_id.json"

    echo "Sleeping for 10 seconds"
    sleep 10

done

echo "Finshed running tests for all iterations"
