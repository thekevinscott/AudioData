import os
import subprocess
import re
import random
from typing import Dict, List

def get_label_from_file(file: str):
    path = os.path.abspath(file)
    return path.split('/')[-2:-1][0]

def get_files_from_dir(folder, ext=None):
    escaped_folder = '\\ '.join(folder.split(' '))
    cmd = 'ls %s' % escaped_folder
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    files = []
    for line in pipe.stdout:
        line = line.strip().decode('ascii')
        file = '%s/%s' % (folder, line)

        if os.path.isdir(file):
            files = files + get_files_from_dir(file, ext)
        elif ext is None or re.match(ext,file):
            files.append(file)

    return files

def get_starting_slice():
    r = random.randint(1, 960)
    return r

def get_sliced_audio_files(files, random_window):
    for file in files:
        starting_index = 0
        if random_window:
            starting_index = get_starting_slice()

        file['audio'] = file['audio'][get_starting_slice():]
        file['starting_index'] = starting_index

    return files

def get_transformed_files(files, transforms: List):
    for file in files:
        for transform in transforms:
            transformed_audio = transform(file['audio'])
            assert len(transformed_audio) == len(file['audio'])
            file['audio'] = transformed_audio

    return files

def shuffle_chunks(chunks, shuf: bool):
    if shuf:
        random.shuffle(chunks)

    return chunks

def get_chunk(chunk, separation):
    if isinstance(separation, list):
        d = {}
        for key in separation:
            d[key] = chunk[key]
        return d
    return chunk[separation]

def separate_chunks(chunks, separations):
    return tuple([get_chunk(chunk,sep) for chunk in chunks] for sep in separations)

def split_data(split, *args):
    if split is None:
        return (args)

    if len(args[0]) * split < 1:
        raise Exception('Not enough samples for split')

    length = len(args[0])
    for arg in args[1:]:
        if length != len(arg):
            raise Exception('Mismatch in length of arguments')

    cut = round(len(args[0])*(1-split))

    return (
        tuple(arg[0:cut] for arg in args),
        tuple(arg[cut:] for arg in args),
    )
