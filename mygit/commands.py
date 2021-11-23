import os

from . import base


def init(repo):
    # Create a new repo, add .mygit folder

    if not os.path.isdir('.mygit'):
        os.mkdir('.mygit')
        for file in ['objects','refs','refs/heads']:
            os.mkdir(os.path.join('.mygit',file))
        print("new repository created")
    else:
        raise ValueError('mygit repository already exists')


def commit(message):
    # Commit files
    
    base.commit_files(message)


def add (filename):
    
    for name in filename.files:
        if os.path.isfile(name):
            base.add_file(name)
        
        # Check if filename is directory
        elif os.path.isdir(name):            
            for root, _, filenames in os.walk(name):
                for filename in filenames:
                    path = os.path.relpath (f'{root}/{filename}')
                    if '.mygit' in path.split('/') or not os.path.isfile (path):
                        continue
                    base.add_file(path)


def status(arg):
    # Get status of files

    files = base.working_dir()
    staged = base.read_index()
    commited = base.read_index(True)

    # This part should be improved
    for file in files:  
        if (file,files[file]) in commited.items():
            continue
        elif (file,files[file]) in staged.items():
            print(file,"staged")
        elif file in staged or file in commited:
            print(file, "modified file")
        else:
            print(file, "new file")

        
    