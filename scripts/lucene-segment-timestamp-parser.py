import re
import datetime
import argparse

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def main(filename):
    file_lines = read_file(filename)
    converted_lines = parse_and_convert_lucene_segment_timestamps(file_lines)
    filename = filename.split(".")[0]
    with open(f"converted-{filename}.txt", "w") as file:
        for line in converted_lines:
            file.write(line)

    print(f"Finished converting lucene segment timestamps into human-readable formatted timestamps for {filename}")

def parse_and_convert_lucene_segment_timestamps(file_lines):
    converted_lines = []

    for line in file_lines:
        if "[" in line:
            # Find iterations
            search_results = re.finditer(r'\[(.*?)\]', line)
            raw_results = (search_results.__next__()).group(0)
            results = raw_results.lstrip("[]").rstrip("]").split(",")

            # Each segment has a start time and end time. Convert those times to UTC and store as a list, separating date and time
            start_date = (datetime.datetime.utcfromtimestamp(int(results[0][0:-3])).strftime('%m-%d-%Y %H:%M:%S')).split(" ")
            end_date = (datetime.datetime.utcfromtimestamp(int(results[1][0:-3])).strftime('%m-%d-%Y %H:%M:%S')).split(" ")

            reformatted_start_date = f"{convert_date_to_human_readable_format(start_date[0])} {start_date[1]}"
            reformatted_end_date = f"{convert_date_to_human_readable_format(end_date[0])} {end_date[1]}"

            converted_dates = f"[{reformatted_start_date}, {reformatted_end_date}]"

            # Substitute times
            converted_line = re.sub(r'\[(.*?)\]', converted_dates, line)
            converted_lines.append(converted_line)
        else:
            converted_lines.append(line)

    return converted_lines

def convert_date_to_human_readable_format(input_date):
    date_components = input_date.split("-")
    month, date, year = MONTHS[int(date_components[0])], int(date_components[1]), int(date_components[2])

    return f"{month} {date}, {year}"

def read_file(file):
    lines = []
    with open(file, "r") as segment_file:
        for line in segment_file:
            lines.append(line)

    return lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Lucene Segment Timestamp Parser", description="A tool to parse and convert lucene segment epoch timestamps to human-readable formatted timestamps")
    parser.add_argument("--file", "-f", required=True, help="File containing lucene segments timestamps. Usually outputted by executing VisualizePointTree.java from Lucene-University.")
    args = parser.parse_args()
    file = args.file
    main(file)