import argparse

parser = argparse.ArgumentParser(description="Makes copy pasting file contents for chatGPT easier")
parser.add_argument('--tree', '-t', action='store_true', help='Creates a tree diagram of the file structure.')

### Java specific functions
parser.add_argument('--cache', '-c', action='store_true', help='Caches files to make traversing files faster')
parser.add_argument('--clear-cache', action='store_true', help='Clears the cache')

# File traversing for files specifically,