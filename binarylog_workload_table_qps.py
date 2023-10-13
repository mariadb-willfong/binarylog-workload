import sys
import re
from collections import defaultdict

def main():
    previous_line = ""
    table_operation_counts = defaultdict(int)
    first_timestamp = None
    last_timestamp = None

    for line in sys.stdin.buffer:
        line = line.decode('utf-8', 'ignore').strip()

        # Match operations and table names
        match = re.search(r'^### (INSERT INTO|UPDATE|DELETE FROM) `([^`]+)\`.`([^`]+)`', line)
        if match:
            operation, dbname, tablename = match.groups()
            table = f"`{dbname}`.`{tablename}`"

            timestamp = re.search(r'^#(\d{6} \d{2}:\d{2}:\d{2})', previous_line)
            if timestamp:
                time_key = timestamp.group(1)
                
                # Check and store the first timestamp
                if first_timestamp is None:
                    first_timestamp = time_key
                
                # Always update the last timestamp
                last_timestamp = time_key

                table_operation_counts[table] += 1

        previous_line = line

    # Generate the text report
    print(f"First Timestamp: {first_timestamp}")
    print(f"Last Timestamp: {last_timestamp}")
    print("="*50)
    print("Table Name\t\t\tQuery Count")
    print("="*50)
    for table, count in sorted(table_operation_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{table}\t\t\t{count}")

if __name__ == "__main__":
    main()
