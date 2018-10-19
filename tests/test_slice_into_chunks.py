import pytest
import random
from ..AudioData.AudioData import AudioData
from pydub.generators import Sine
audioData = AudioData()

def test_it_returns_chunks():
    audio = Sine(440).to_audio_segment()
    files = [{
        'audio': audio[0:1000],
        'file': 'foo',
        'label': 'foo',
        'start_index': 0,
    }]

    chunks = audioData.slice_into_single_sample_chunks(files)
    print(len(chunks))
    assert len(chunks) == 1

def test_it_returns_one_chunk_for_excess_audio():
    audio = Sine(440).to_audio_segment() * 2
    files = [{
        'audio': audio[0:1500],
        'file': 'foo',
        'label': 'foo',
        'start_index': 0,
    }]

    chunks = audioData.slice_into_single_sample_chunks(files)
    assert len(chunks) == 1

def test_it_returns_multiple_chunks():
    audio = Sine(440).to_audio_segment() * 5
    files = [{
        'audio': audio,
        'file': 'foo',
        'label': 'foo',
        'start_index': 0,
        'samples': [],
    }]

    chunks = audioData.slice_into_single_sample_chunks(files)
    assert len(chunks) == 5
