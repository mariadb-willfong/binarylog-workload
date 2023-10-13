import sys
import re


def short_strings(s):
    # Check if the string contains an '='
    if '=' not in s:
        return s

    key, value = s.split('=', 1)  # Split string at the first '='

    # If the value starts with a single quote
    if value.startswith("'"):
        n = value.strip('\'"')
        if len(value) > 20:  # Check if there's room to replace the middle
            return f"{key}='{n[0:9]}...{n[-9:]}'"
        return s

    # Return the full value otherwise
    return s


def process_input_line(line):
    a = line.replace("###", "").strip()
    if a.startswith("@"):
        return short_strings(a)
    return a


def process_query(q):
    query = q.pop(0)
    return f"{query} SET " + ', '.join(q) + ';'

def main():
    output = []
    query_builder = []
    is_insert_block = False
    for line in sys.stdin.buffer.read().decode('utf-8', 'ignore').splitlines():
        line = line.strip()

        if line.startswith("### INSERT INTO"):
            is_insert_block = True
            query_builder.append(process_input_line(line))

        # If inside an insert block, process the line
        elif is_insert_block and line.startswith("###") and not line == '### SET':
            processed_line = process_input_line(line)
            query_builder.append(processed_line)

        elif is_insert_block and not line.startswith("###"):
            is_insert_block = False
            query = process_query(query_builder)
            output.append(query)
            query_builder = []

    tables = {}

    for query in output:
        table_match = re.search(r'INSERT INTO `[a-z]*`\.`(.*?)`', query)  # Corrected regex
        if not table_match:
            continue

        table_name = table_match.group(1)
        if table_name not in tables:
            tables[table_name] = {}

        column_values = re.findall(r'@(\d+)=(.*?)(,|;)', query)
        for col, value, _ in column_values:
            col_name = f'@{col}'
            if col_name not in tables[table_name]:
                tables[table_name][col_name] = {'distinct': set(), 'total': 0}
            
            tables[table_name][col_name]['distinct'].add(value)
            tables[table_name][col_name]['total'] += 1

    # Step 2 and 3: Group by table and calculate ratios for each column
    for table_name, columns in tables.items():
        print(f"Table: {table_name}")
        for col_name, data in columns.items():
            print(f"  Column {col_name}: {len(data['distinct'])} / {data['total']}")
        print("")


    

if __name__ == "__main__":
    main()
