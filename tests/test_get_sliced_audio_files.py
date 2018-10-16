import pytest
import random
from ..AudioData.utils import get_sliced_audio_files
from pydub.generators import Sine

random.seed(1)

audio = Sine(440).to_audio_segment()
def test_it_returns_files_if_false():
    files = [{
        'audio': audio,
        'file': 'foo',
        'label': 'foo',
    }]

    assert get_sliced_audio_files(files, False) == files

def test_it_returns_parsed_files_if_true():
    files = [{
        'audio': audio,
        'file': 'foo',
        'label': 'foo',
    }]

    new_files = get_sliced_audio_files(files, True)
    assert len(new_files[0]['audio']) < len(audio)
    assert len(new_files[0]['audio']) == 132
