#!/usr/bin/python3
from file_parsing.extract import extract_file_bodies, extract_file_tree, unpack_config
from file_parsing.estimate_tokens import estimate_tokens, warn_excession
from file_parsing.copy_to_clipboard import copy_to_clipboard, get_from_clipboard
from caching.caching import cache_file_paths, clear_cache
from utils.colorize import colorize, CYAN, BOLD
from arg_parser import parser
from utils.open_json import open_json
from os import getcwd
from dotenv import load_dotenv
from java_extractor.java_extractor import extract_method_chain
load_dotenv()


CONFIG_PATH =  './libra-config.json'

if __name__ == "__main__":
    args = parser.parse_args()
    entry = getcwd()
    ignored_files, ignored_folders = set(), set()  
    config = open_json(CONFIG_PATH)
    ignored_files, ignored_folders =  unpack_config(config)

    
    # Flags
    


    # Cache clearing, if both flags for cache and clearing cache are given, clear the cache anyways
    if args.clear_cache:
      clear_cache()
      exit(0)

    elif args.cache:
      cache_file_paths(entry, ignored_files, ignored_folders)
      exit(0)

    elif args.clazz and args.method:
      print(args.clazz)
      extract_method_chain(args.clazz, args.method)
      
      exit(0)
      
    else:  
      # Gets the child most file path for use in file path namings, we assume the last item is the cwd
      full_file_path = getcwd()
      
      # Gets the file contents of all the files, copies them to the clipboard
      file_contents = extract_file_bodies(full_file_path, ignored_files, ignored_folders )
      copy_to_clipboard(file_contents)
      num_tokens = estimate_tokens(file_contents)
      warn_excession(num_tokens)
      num_tokens = colorize(f"{CYAN}{BOLD}", num_tokens)
      print(f"Estimated tokens: {num_tokens}")
    
    # Handle tree arguments
    if args.tree:
        file_tree = extract_file_tree(config, entry)
        print(file_tree)