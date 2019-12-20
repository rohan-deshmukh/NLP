import os
import glob

ALLOWED_EXTENSIONS = {'xlsx'}


def allowed_file(filename):
    """Returns True if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def remove_files(directory):
    """Deletes all excel files in the directory"""
    for f in glob.glob(os.path.join(directory, '*.json')):
        os.remove(f)
    for f in glob.glob(os.path.join(directory, '*.xlsx')):
        os.remove(f)

def isempty(directory):
    """Checks if directory is empty and returns boolean"""
    if not os.listdir(directory):
        return True
    else:
        return False


if __name__ == '__main__':
    remove_files("/Users/rohandeshmukh/Desktop/Rohan/Xoro/ensemble-service/data/prev_q_data")
    isempty("/Users/rohandeshmukh/Desktop/Rohan/Xoro/ensemble-service/data/prev_q_data")