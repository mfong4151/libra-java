from utils.open_json import open_json, save_json
from utils.walk_folder import  walk_folder
from file_parsing.extract import stringify_file 
from re import sub

PACKAGE_LITERAL = "package"
PACKAGE_SEMICOLON_REGEX= r'\bpackage \b|;'
DOT_JAVA_LITERAL = ".java"


def _strip_file_postfix(full_path: str):
  
  class_name = full_path.split("/")[-1]
  return class_name.strip(DOT_JAVA_LITERAL)

def _append_package_name(cwd, full_path: str, class_name: str):
  file_contents:str = stringify_file(cwd, full_path, is_file_path_included = False).split("\\n")
  
  for contents in file_contents:
    for line in contents.split("\n"):
      if PACKAGE_LITERAL in line.strip():
        cleaned_line = sub(PACKAGE_SEMICOLON_REGEX, '', line)
        return ".".join([cleaned_line, class_name])
      
  return class_name
  
def _get_packaged_class(cwd: str, full_path:str):
   
  class_name = _strip_file_postfix(full_path)
  if DOT_JAVA_LITERAL in full_path:
    return _append_package_name(cwd, full_path, class_name)
  
  else:
    return class_name
  
  

def cache_file_paths(cwd, ignored_files, ignored_folders):
  """
  1. Greps through the folders
  2. Finds terminal file names
  3. Creates a hashmap of class name -> full file path
  4. Saves it to the configs
  """  
  
  files = walk_folder(cwd, ignored_files, ignored_folders)
  config = open_json("./libra-config.json")
  config["file_cache"] = { _get_packaged_class(cwd, pathed_file): pathed_file for pathed_file in files}
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