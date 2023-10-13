import sys
import re
from collections import defaultdict
import matplotlib.pyplot as plt

def main():
    previous_line = ""
    operation_counts = defaultdict(lambda: defaultdict(int))

    for line in sys.stdin.buffer:
        line = line.decode('utf-8', 'ignore').strip()

        match = re.search(r'^### (INSERT INTO|UPDATE|DELETE FROM) `([^`]+)`', line)
        if match:
            operation, _ = match.groups()
            timestamp = re.search(r'^#(\d{6} \d{2}:\d{2}:\d{2})', previous_line)

            if timestamp:
                time_key = timestamp.group(1)[:15]  # Precision up to the second
                operation_counts[time_key][operation] += 1

        previous_line = line

    # Generate chart
    timestamps = sorted(operation_counts.keys())
    insert_values = [operation_counts[time_key]["INSERT INTO"] for time_key in timestamps]
    update_values = [operation_counts[time_key]["UPDATE"] for time_key in timestamps]
    delete_values = [operation_counts[time_key]["DELETE FROM"] for time_key in timestamps]

    plt.figure(figsize=(10, 6))

    plt.bar(timestamps, insert_values, label='INSERT', color='green')
    plt.bar(timestamps, update_values, bottom=insert_values, label='UPDATE', color='blue')
    plt.bar(timestamps, delete_values, bottom=[i + u for i, u in zip(insert_values, update_values)], label='DELETE', color='red')

    # Adjust xticks for better visibility
    total_points = len(timestamps)
    interval = total_points // 20  # Show a label every 5%
    plt.xticks(timestamps[::interval], rotation=45)

    plt.xlabel('Timestamps')
    plt.ylabel('Operation Count')
    plt.title('Operation Count over Time')
    plt.tight_layout()
    plt.legend()
    plt.grid(True, axis='y')
    plt.show()

if __name__ == "__main__":
    main()
