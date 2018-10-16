import pytest
import random
from ..AudioData.utils import get_transformed_files
from pydub.generators import Sine

random.seed(1)

audio = Sine(440).to_audio_segment()
def test_it_returns_files_for_no_transforms():
    files = [{
        'audio': audio,
        'file': 'foo',
        'label': 'foo',
    }]

    assert get_transformed_files(files, []) == files

def test_it_transforms_files():
    new_audio = Sine(550).to_audio_segment()
    files = [{
        'audio': audio,
        'file': 'foo',
        'label': 'foo',
    }]

    transformed = get_transformed_files(files, [
        lambda audio: new_audio,
    ])

    assert len(transformed[0]['audio']) == len(files[0]['audio'])
    assert transformed[0]['audio'].get_array_of_samples() == new_audio.get_array_of_samples()
