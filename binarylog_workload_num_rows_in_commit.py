import sys
from collections import defaultdict

def main():
    counts = defaultdict(int)

    for line in sys.stdin:
        line = line.strip()
        match = line.split(": ")
        if len(match) == 2 and match[0] == "# Number of rows":
            count = int(match[1])
            counts[count] += 1

    # Print the occurrences
    for num, occ in sorted(counts.items()):
        print(f"{num} rows: {occ} times")

    # Print the maximum rows changed and how many times
    max_rows = max(counts.keys())
    print(f"\nMost rows changed: {max_rows}, occurred {counts[max_rows]} times")

if __name__ == "__main__":
    main()
