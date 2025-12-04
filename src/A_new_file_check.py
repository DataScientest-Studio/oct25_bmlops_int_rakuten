## 0_new_file_check.py 
# imports
# import os



import utils.file_helper as fh 


# main function

def new_file_check(files, path):
    
    if not files:
        print("No new files found")
        return None
    
    files_new = []
    for f in files:
        # check for columns
        # to be added
        f_moved = fh.move_file(f, path)
        files_new.append(f_moved)

    print(f"Found {len(files)} files in 'data_input' folder and moved them to folder 'data_lake'")
    return files_new


if __name__ == "__main__":
    new_file_check()