from os import walk
from os.path import join


## TODO  I'm sure there are edge cases here, look into them
def _is_ignored_folder(path: str, ignored_folders: set[str]):
  path_set = set(path.split("/"))
  
  for ignored_folder in ignored_folders:
    if ignored_folder in path_set:
      return True
  return False

def walk_folder(ignored_files: set[str], ignored_folders: set[str]):
    pathed_files = []  
  
    for root, _, filenames in walk():
        is_ignored_folder = _is_ignored_folder(root, ignored_folders)  
        for filename in filenames:
            if is_ignored_folder or filename in ignored_files:
              continue
            
            pathed_files.append(join(root, filename))
            
    return pathed_files
