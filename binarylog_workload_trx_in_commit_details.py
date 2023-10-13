import sys
import re

def extract_timestamp(s):
    pattern = r'^#(\d{6} \d{2}:\d{2}:\d{2})'
    match = re.search(pattern, s)
    if match:
        return match.group(1)
    return None

def clean_string(s):
    return s.strip('#').strip()

def update_stmt_comparison(list_where, list_set):
    differences = []
    for item1, item2 in zip(list_where, list_set):
        if item1 != item2:
            # Extract the @number from the differing item
            at_num = item1.split('=')[0]
            differences.append(at_num)
    return differences



def main():
    try:
        in_transaction = False
        update_where = []
        update_set = []
        in_update = False
        in_update_where = False
        in_update_set = False

        for line in sys.stdin.buffer:
            try:
                decoded_line = line.decode('utf-8').strip()

                if in_update_set and not decoded_line.startswith("###   @"):
                    in_update = False
                    in_update_where = False
                    in_update_set = False
                    #print(update_where)
                    #print(update_set)
                    print( update_stmt_comparison(update_where, update_set))
                    update_where = []
                    update_set = []

                if decoded_line.startswith("###   @"):
                    if in_update_where:
                        update_where.append(clean_string(decoded_line))
                    if in_update_set:
                        update_set.append(clean_string(decoded_line))
                
                if in_transaction:
                    if decoded_line.startswith("### INSERT INTO"):
                        print(decoded_line)
                    elif decoded_line.startswith("### UPDATE"):
                        in_update = True
                        print(decoded_line)
                    elif decoded_line.startswith("### DELETE FROM"):
                        print(decoded_line)
                    elif in_update and decoded_line.startswith("### WHERE"):
                        in_update_where = True
                        in_update_set = False
                    elif in_update and decoded_line.startswith("### SET"):
                        in_update_set = True
                        in_update_where = False

                if decoded_line.startswith("START TRANSACTION"):
                    in_transaction = True
                    print(decoded_line)

                elif decoded_line.startswith("COMMIT"):
                    in_transaction = False
                    print("COMMIT")
                    
                # Check for GTID
                elif "GTID" in decoded_line:
                    raw_ts, gtid = decoded_line.split("\t")
                    timestamp = extract_timestamp(raw_ts)
                                        
                    print(f"[{timestamp}] {gtid.ljust(45)}")
                   
                    

            except UnicodeDecodeError:
                # Simply ignore utf-8 decoding errors and continue with the next line
                continue

    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C and exit
        sys.exit()

if __name__ == "__main__":
    main()
