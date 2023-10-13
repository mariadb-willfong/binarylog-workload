import sys
import re

def extract_timestamp(s):
    # Regular expression pattern to match the date-time format
    pattern = r'^#(\d{6} \d{2}:\d{2}:\d{2})'
    match = re.search(pattern, s)
    if match:
        return match.group(1)
    return None


def main():
    try:
        in_transaction = False
        counts = {
            "### INSERT INTO": 0,
            "### UPDATE": 0,
            "### DELETE FROM": 0
        }

        # Reading from stdin
        for line in sys.stdin.buffer:
            try:
                # Attempt to decode the line with utf-8
                decoded_line = line.decode('utf-8').strip()

                # If we're in a transaction, count the occurrences and print the line if it starts with ###
                if in_transaction:
                    if decoded_line.startswith("### INSERT INTO"):
                        counts["### INSERT INTO"] += 1
                        #print(decoded_line)
                    elif decoded_line.startswith("### UPDATE"):
                        counts["### UPDATE"] += 1
                        #print(decoded_line)
                    elif decoded_line.startswith("### DELETE FROM"):
                        counts["### DELETE FROM"] += 1
                        #print(decoded_line)

                # Check for transaction start
                if decoded_line.startswith("START TRANSACTION"):
                    in_transaction = True
                    #print(decoded_line)

                # Check for transaction end and print the summary
                elif decoded_line.startswith("COMMIT"):
                    in_transaction = False
                    #print(f"  Summary: INSERT: {counts['### INSERT INTO']}, UPDATE: {counts['### UPDATE']}, DELETE: {counts['### DELETE FROM']}")
                    #print("COMMIT")
                    # Reset counts
                    
                # Check for GTID
                elif "GTID" in decoded_line:
                    raw_ts, gtid = decoded_line.split("\t")
                    timestamp = extract_timestamp(raw_ts)
                    sum = f"  INSERT: {counts['### INSERT INTO']}, UPDATE: {counts['### UPDATE']}, DELETE: {counts['### DELETE FROM']}"
                                        
                    print(f"[{timestamp}] {gtid.ljust(45)}: {sum}")
                    counts = {
                        "### INSERT INTO": 0,
                        "### UPDATE": 0,
                        "### DELETE FROM": 0
                    }
                    

            except UnicodeDecodeError:
                # Simply ignore utf-8 decoding errors and continue with the next line
                continue

    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C and exit
        sys.exit()

if __name__ == "__main__":
    main()
