import csv
from datetime import datetime
from collections import defaultdict

# Function to parse the log and aggregate data
def parse_log(file_name):
    # Dictionary to hold the aggregated data
    func_data = defaultdict(lambda: {'calls': 0, 'total_time': 0})

    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        temp_start_times = {}

        for row in reader:
            func_name = row['function_name']
            event = row['event']
            timestamp = datetime.fromisoformat(row['timestamp'])

            # Check for start event
            if event == 'start':
                temp_start_times[func_name] = timestamp
            elif event == 'stop':
                # Calculate the time difference
                time_diff = timestamp - temp_start_times[func_name]
                func_data[func_name]['calls'] += 1
                func_data[func_name]['total_time'] += time_diff.total_seconds() * 1000  # Convert to milliseconds

    # Calculate average time
    for name, data in func_data.items():
        data['average_time'] = data['total_time'] / data['calls']

    return func_data

# Function to print the report table
def print_report(data):
    # Find the longest function name for alignment
    longest_name = max(len(name) for name in data.keys())

    header_format = "| {:<" + str(longest_name) + "} | {:^13} | {:^16} | {:^19} |"
    row_format = "| {:<" + str(longest_name) + "} | {:^13} | {:^16.3f} | {:^19.3f} |"

    print(header_format.format("Function Name", "Num. of calls", "Total Time (ms)", "Average Time (ms)"))
    print("|" + "-" * (longest_name + 2) + "+" + "-" * 16 + "+" + "-" * 19 + "+" + "-" * 22 + "|")

    for func_name, func_data in data.items():
        print(row_format.format(func_name, func_data['calls'], func_data['total_time'], func_data['average_time']))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python reporting.py trace_file.log")
        sys.exit(1)

    log_file = sys.argv[1]
    aggregated_data = parse_log(log_file)
    print_report(aggregated_data)
