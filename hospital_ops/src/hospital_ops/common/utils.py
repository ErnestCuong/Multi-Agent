from os import listdir
from os.path import isfile, join

def get_all_file_names(folder_path):
    return [f for f in listdir(folder_path) if isfile(join(folder_path, f))]