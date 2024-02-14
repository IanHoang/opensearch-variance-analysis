import re
import datetime

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
text = "0 [897249601000,897762353000] - 25846743"


def main():
    file_lines = read_file("/Users/hoangia/Desktop/Development/segments-experiment-3.txt")
    converted_lines = []

    print(file_lines)
    for line in file_lines:
        if "[" in line:
            # Find iterations
            search_results = re.finditer(r'\[(.*?)\]', line)

            raw_results = (search_results.__next__()).group(0)
            # Convert to list
            results = raw_results.lstrip("[]").rstrip("]").split(",")

            # Convert times to UTC
            start_date = (datetime.datetime.utcfromtimestamp(int(results[0][0:-3])).strftime('%m-%d-%Y %H:%M:%S')).split(" ")
            end_date = (datetime.datetime.utcfromtimestamp(int(results[1][0:-3])).strftime('%m-%d-%Y %H:%M:%S')).split(" ")

            start_date = f"{convert_date_to_human_readable_format(start_date[0])} {start_date[1]}"
            end_date = f"{convert_date_to_human_readable_format(end_date[0])} {end_date[1]}"
            converted_dates = f"[{start_date}, {end_date}]"

            # Substitute times
            converted_line = re.sub(r'\[(.*?)\]', converted_dates, line)
            converted_lines.append(converted_line)
        else:
            converted_lines.append(line)

    with open("converted-segments-experiment-3.txt", "w") as file:
        for line in converted_lines:
            file.write(line)

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
    main()