import hashlib
import os
import json


def read_file(file):
    with open(file, 'rb') as f:
        return f.read()


def hash_object(data, object_type='blob'):
    """ Simplified object hashing. 
        Hashed files are saved in objects folder.
        This feature allows add later improved commit system and
        other features like branches
    """

    ready_data = object_type.encode()+b'\x00' + data  
    hash = hashlib.sha1(ready_data).hexdigest() 

    # Set hash in hex system as filename

    with open (f'.mygit/objects/{hash}', 'wb') as f:
        f.write(ready_data)
    return hash


def read_index(commit=False):
    # Read json file with index - staged files

    index = {}
    file_path = '.mygit/objects/object' if commit else '.mygit/index' 

    # If file doesn't exist, create new

    if os.path.isfile (file_path):
        with open (file_path) as f:
            index =json.load(f)
    else:
        with open (file_path, 'w') as f:
            json.dump(index, f)

    return index


def working_dir():
    # Get hashed data of working tree files

    files = {}
    for root, _, filenames in os.walk('.'):
        for filename in filenames:
            path = os.path.relpath (f'{root}/{filename}')
            if '.mygit' in path.split('/') or not os.path.isfile(path):
                continue  # Don't scan .mygit files 

            filename = os.path.relpath (path)
            with open (filename, 'rb') as f:  # Hash files data
                hash = hash_object(f.read())
                files.update({filename:hash})
    return files


def add_file (filename):
    # Add files to staged index 

    commited = read_index(True)
    filename = os.path.relpath (filename)

    with open (filename, 'rb') as f:
        hash = hash_object(f.read())
        index = {filename:hash}

        # Check if file is changed 

        if (filename, hash) not in commited.items():
            data = read_index()
            data.update(index)    
            with open('.mygit/index', 'w') as f:
                json.dump(data,f)


def commit_files(message):
    # Add files from staged index to commit index

    files = read_index()
    if os.path.isfile('.mygit/index'):
        with open ('.mygit/index', 'r') as f:
            staged =json.load(f)

        # Check if file doesn't change before commit
        
        for data in staged:
            if (data,staged[data]) in files.items():    
                commit = read_index(True)
                commit.update(staged)

                with open('.mygit/objects/object','w') as file:
                    json.dump(commit,file)

        os.remove('.mygit/index')  # Remove staged index
