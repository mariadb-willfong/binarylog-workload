import sys
import re
from collections import defaultdict
import matplotlib.pyplot as plt

def sort_timestamps(timestamp):
    date, time = timestamp.split()
    return (date, [int(i) for i in time.split(':')])

def main():
    previous_line = ""
    table_time_counts = defaultdict(lambda: defaultdict(int))  # Nested defaultdict

    for line in sys.stdin.buffer:
        line = line.decode('utf-8', 'ignore').strip()

        # Match operations and table names
        match = re.search(r'^### (INSERT INTO|UPDATE|DELETE FROM) `([^`]+)\`.`([^`]+)`', line)
        if match:
            operation, dbname, tablename = match.groups()
            table = f"`{dbname}`.`{tablename}`"

            timestamp = re.search(r'^#(\d{6} \d{2}:\d{2}:\d{2})', previous_line)
            if timestamp:
                time_key = timestamp.group(1)[:15]  # Precision up to the second
                table_time_counts[table][time_key] += 1

        previous_line = line

    # Compute the global set of timestamps
    all_timestamps = set()
    for table in table_time_counts:
        all_timestamps.update(table_time_counts[table].keys())

    all_timestamps = sorted(list(all_timestamps), key=sort_timestamps)

    for table in table_time_counts:
        for timestamp in all_timestamps:
            if timestamp not in table_time_counts[table]:
                table_time_counts[table][timestamp] = 0

    # Sort tables by total queries and get the top 5
    sorted_tables = sorted(table_time_counts.keys(), key=lambda k: sum(table_time_counts[k].values()), reverse=True)[:5]

    # Determine the number of subplots
    num_tables = len(sorted_tables)

    fig, axs = plt.subplots(num_tables, 1, figsize=(12, 3 * num_tables), sharex=True)

    if num_tables == 1:  # Handle the case of a single subplot
        axs = [axs]

    for idx, table in enumerate(sorted_tables):
        times = all_timestamps
        qps_values = [table_time_counts[table][time] for time in times]

        axs[idx].plot(times, qps_values, label=table)
        axs[idx].set_title(table)
        axs[idx].grid(True)
        axs[idx].legend()

    # Adjusting x-labels for the last plot (they are shared)
    n_times = len(times)
    step = int(0.05 * n_times)
    if step == 0: step = 1  # Avoid zero
    axs[-1].set_xticks(times[::step])
    plt.setp(axs[-1].get_xticklabels(), rotation=45, ha='right', fontsize=10)

    plt.tight_layout(pad=2.5)

    plt.show()

if __name__ == "__main__":
    main()
