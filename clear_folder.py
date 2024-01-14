import os
import shutil

def remove_folder(directory):
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                # Use shutil.rmtree to remove the directory and its contents
                shutil.rmtree(item_path)
                print(f'Directory {item_path} successfully deleted.')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    current_directory = os.getcwd()
    remove_folder(current_directory)
