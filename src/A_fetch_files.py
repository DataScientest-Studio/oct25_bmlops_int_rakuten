# imports
from pathlib import Path
from utils.settings import session
import utils.file_helper as fh 

def fetch_files(src_path=None, dst_path=None, file_type=None):
    """
    Fetches files from a source folder and moves them to a destination folder.

    Parameters:
    - src_path: path to the folder containing input files (data_input)
    - dst_path: path to the folder where files should be moved (data_lake)
    - file_type: list of file extensions to filter, e.g., ['.csv', '.zip']

    Returns:
    - List of moved file paths (as strings)
    """

    # Check that both source and destination paths are provided
    if not src_path or not dst_path:
        print("At least one file path is not given.")

    # If file_type not provided, default to CSV and ZIP files
    if not file_type:
        file_type = [".csv", 
                    ".zip",
                     ]
        
    # Convert src_path to Path object for easier path operations
    folder = Path(src_path)

    # List all files in source folder with matching extensions
    files = [str(f) for f in folder.iterdir() \
             if f.suffix.lower() in file_type]
    
    # Return empty list if no files found
    if not files:
        print("No files found")
        return []
    
    # Move files to destination folder and store new paths
    files_new = []
    for f in files:
        f_moved = fh.move_file(f, Path(dst_path))
        files_new.append(str(f_moved))

    print(f"Found {len(files)} files in 'data_input' folder and moved them to folder 'data_lake'")
    return files_new


if __name__ == "__main__":
    fetch_files()