import pytest
import random
from ..AudioData.utils import shuffle_chunks

random.seed(1)

def test_it_does_not_shuffle():
    files = ['a', 'b', 'c']

    assert shuffle_chunks(files, False) == files

def test_it_shuffles():
    files = ['a', 'b', 'c']

    assert shuffle_chunks(files, True) == ['c','b','a']
