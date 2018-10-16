import pytest
import random
from ..AudioData.AudioData import AudioData
from pydub.generators import Sine
audioData = AudioData()

def test_it_returns_chunks():
    audio = Sine(440).to_audio_segment()
    files = [{
        'audio': audio[0:960],
        'file': 'foo',
        'label': 'foo',
        'start_index': 0,
    }]

    chunks = audioData.slice_into_chunks(files)
    assert len(chunks) == 1

def test_it_returns_chunks_despite_channels():
    audio = Sine(440).to_audio_segment()
    audio = audio.set_channels(2)
    files = [{
        'audio': audio[0:960],
        'file': 'foo',
        'label': 'foo',
        'start_index': 0,
    }]

    chunks = audioData.slice_into_chunks(files)
    assert len(chunks) == 1

def test_it_returns_chunks_despite_bytes():
    audio = Sine(440).to_audio_segment()
    audio = audio.set_sample_width(4)
    files = [{
        'audio': audio[0:960],
        'file': 'foo',
        'label': 'foo',
        'start_index': 0,
    }]

    chunks = audioData.slice_into_chunks(files)
    assert len(chunks) == 1

def test_it_returns_chunks_despite_frame_width():
    audio = Sine(440).to_audio_segment()
    audio = audio.set_frame_rate(44100 * 2)
    files = [{
        'audio': audio[0:960],
        'file': 'foo',
        'label': 'foo',
        'start_index': 0,
    }]

    chunks = audioData.slice_into_chunks(files)
    assert len(chunks) == 1

def test_it_returns_one_chunk_for_excess_audio():
    audio = Sine(440).to_audio_segment() * 2
    files = [{
        'audio': audio[0:1500],
        'file': 'foo',
        'label': 'foo',
        'start_index': 0,
    }]

    chunks = audioData.slice_into_chunks(files)
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

    chunks = audioData.slice_into_chunks(files)
    assert len(chunks) == 5
