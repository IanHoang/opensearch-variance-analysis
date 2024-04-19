# Segment Tuning Scenario Variance Analysis

### Prerequisites
1. Setup an opensearch cluster from the [OpenSearch-Cluster-Cdk Repository](https://github.com/opensearch-project/opensearch-cluster-cdk) and also set up an EC2 instance (if not running this locally).
2. Copy over `segment-tuning-scenario-v2.sh` and `update-index-settings-v2.sh` over to the place where the tests will be run (if not running locally, insert into EC2 instance). Ensure to provide the cluster endpoint url, workload params, and test names to the `segment-tuning-scenario-v2.sh` script.
3. Where you are running the scripts, ensure that PyPi OSB was installed. If using an official workload, modify the workload in `~/.benchmark/benchmarks/workloads/default` repository as needed. For example, if your experiment requires only using a specific index from a workload, delete the other index references in the `workload.json` file in the corresponding workload directory. Also, if you need to create `log_byte_size` merge policy indices, OpenSearch only allows these to be created on index creation at the index level and not the cluster level. Therefore, you'll need to add the following to the index.json file for the corresponding workload directory:
```
"index.merge.policy": "log_byte_size"
```

### Run Tests
1. Start a screen session and run the `segment-tuning-scenario-v2.sh`. This will run the test 3 times with ingestion and search.

### Average Results from All Test Executions
1. Copy scripts from [this repository](https://github.com/IanHoang/opensearch-scripts) over to where you ran the tests.
2. Ensure that you have set up a virtual env, activated it, and run `python3 -m pip install -r requirements.txt` to install all dependencies.
3. Run `python3 average-test-execution-results.py -f <folder containing all test execution runs that you want averaged> -i <output file name>`. If you want to ensure that service time and latency values across all runs are the same, you can rerun the same script with a different output file name and `-l` flag. This will produce a new file but with the aggregations of the latency fields instead of service time. You can do a diff to compare them and ensure service time and latency values are the same.
4. To convert the file into a CSV format, use the `python3 convert-results-to-csv.py -f <file outputted from average-test-execution-results.py>`.

### Get Timestamp Ranges for All Segments
This is only applicable for timeseries data.
1. SSH into the cluster and run the following steps:
```
wget https://corretto.aws/downloads/latest/amazon-corretto-21-x64-linux-jdk.rpm
sudo yum localinstall amazon-corretto-21-x64-linux-jdk.rpm -y
java --version
export JAVA_HOME=/usr/lib/jvm/java-21-amazon-corretto/

sudo yum install git -y
git clone https://github.com/IanHoang/lucene-university.git
cd lucene-university/
git checkout update-visualize-point-tree-program
rm src/main/java/example/basic/BottomUpIndexReader.java
```
2. In the `src/main/java/example/points/VisualizePointTree.java` file, update the line with `tmpDir`, specifically remove the index ID with the index ID from your cluster's experiments (you can get this from `_cat/indices?v`).
3. Run `./gradlew build` to compile and then run `./gradlew run -PclassToExecute=example.points.VisualizePointTree` to produce the segment timestamp ranges.
4. Copy the output from the previous step into a file and run `python3 lucene-segment-timestamp-parser.py --file <file with output>`. This should produce a file of the same name but with `converted` pre-apppended to it that contains the timestamps but in human-readable format.
