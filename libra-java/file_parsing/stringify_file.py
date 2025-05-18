from os.path import splitext

TWO_BACKSLASH = set(['.js', '.tsx', '.ts' , '.css', '.cpp', '.java'])
HASHTAGS = set(['.py', '.rs'])

def clean_file_path(shortened_cwd: str, file_path: str) -> str:
    loc_cwd = file_path.rfind(shortened_cwd)
    return file_path[loc_cwd:]

def file_attrs(shortened_cwd, file_path: str, file_body: str, is_file_path_included = True):
    displayed_file_path = clean_file_path(shortened_cwd, file_path)
    _, ext = splitext(file_path)
    comment = '#' if ext in HASHTAGS else '//'
    contents_to_write = []
    
    if is_file_path_included:
      contents_to_write.append(f"{comment}{displayed_file_path}")
    
    contents_to_write.append(file_body)
    
    return '\n'.join(contents_to_write)


def stringify_file(cwd: str, file_path: str, is_file_path_included = True) -> str:
    try:
        with open(file_path, 'r') as file:
            return file_attrs(cwd, file_path, file.read(), is_file_path_included)
    except FileNotFoundError:
        return ''
    except Exception as e:
        return ''

