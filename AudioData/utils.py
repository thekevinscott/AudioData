import os
import subprocess
import re

def getLabelFromFile(file: str):
    path = os.path.abspath(file)
    return path.split('/')[-2:-1][0]

def getFilesFromDir(folder, ext=None):
    escaped_folder = '\\ '.join(folder.split(' '))
    cmd = 'ls %s' % escaped_folder
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    files = []
    for line in pipe.stdout:
        line = line.strip().decode('ascii')
        file = '%s/%s' % (folder, line)

        if os.path.isdir(file):
            files = files + getFilesFromDir(file, ext)
        elif ext is None or re.match(ext,file):
            files.append(file)

    return files
