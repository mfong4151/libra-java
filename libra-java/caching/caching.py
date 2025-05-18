from utils.open_json import open_json, save_json
from utils.walk_folder import  walk_folder

def strip_file_postfix(full_path: str):
  class_name = full_path.split("/")[-1]
  return class_name.strip(".java") 

def cache_file_paths(cwd, ignored_files, ignored_folders):
  """
  1. Greps through the folders
  2. Finds terminal file names
  3. Creates a hashmap of class name -> full file path
  4. Saves it to the configs
  """  
  
  files = walk_folder(cwd, ignored_files, ignored_folders)
  config = open_json("./libra-config.json")
  config["file_cache"] = { strip_file_postfix(pathed_file): pathed_file for pathed_file in files}
  save_json("./libra-config.json",  config)
  return

def clear_cache():
  """
  Clears the file cache
  """  
  config = open_json("./libra-config.json")
  config["file_cache"] = {}
  save_json("./libra-config.json",  config)
  return