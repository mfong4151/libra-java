import argparse

STORE_TRUE = 'store_true'
STORE_CONST = 'store_const'
parser = argparse.ArgumentParser(description="Makes copy pasting file contents for chatGPT easier")
parser.add_argument('--tree', '-t', action=STORE_TRUE, help='Creates a tree diagram of the file structure.')

### Java specific functions
parser.add_argument('--cache', "-c", action=STORE_TRUE, help='Caches files to make traversing files faster')
parser.add_argument('--clear-cache', action=STORE_TRUE, help='Clears the cache')
parser.add_argument("--clazz", "-cls", help= "Starts a search on a java class, takes the capitalized name of the class, e.g. 'MyClass' from 'MyClass.java'")
parser.add_argument("--method", "-m", help= "Searches the method of the java class, should match the private method name verbatim.")

# File traversing for files specifically,