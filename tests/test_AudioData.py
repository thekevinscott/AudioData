import pytest
from ..AudioData.AudioData import AudioData

def test_AudioData_defaults():
    """Ensure audioData has reasonable defaults"""
    audioData = AudioData()
    assert audioData.channels == 1
    assert audioData.bytes == 2
    assert audioData.frame_rate == 44100

def test_AudioData_init():
    audioData = AudioData(channels = 2)
    assert audioData.channels == 2
    assert audioData.bytes == 2
    assert audioData.frame_rate == 44100

    audioData = AudioData(bytes = 4)
    assert audioData.channels == 1
    assert audioData.bytes == 4
    assert audioData.frame_rate == 44100

    audioData = AudioData(frame_rate = 48000)
    assert audioData.channels == 1
    assert audioData.bytes == 2
    assert audioData.frame_rate == 48000

def test_set_channels():
    audioData = AudioData(channels = 2)
    assert audioData.channels == 2

    audioData.set_channels(1)
    assert audioData.channels == 1

    with pytest.raises(Exception):
        audioData.set_channels(0)

    with pytest.raises(Exception):
        audioData.set_frame_rate(-2)

    with pytest.raises(Exception):
        audioData.set_channels(3)

    with pytest.raises(Exception):
        audioData.set_channels(None)

def test_set_bytes():
    audioData = AudioData(bytes = 2)
    assert audioData.bytes == 2

    audioData.set_bytes(1)
    assert audioData.bytes == 1

    with pytest.raises(Exception):
        audioData.set_bytes(0)

    with pytest.raises(Exception):
        audioData.set_bytes(-2)

def test_set_frame_rate():
    audioData = AudioData(frame_rate = 44100)
    assert audioData.frame_rate == 44100

    audioData.set_frame_rate(48000)
    assert audioData.frame_rate == 48000

    with pytest.raises(Exception):
        audioData.set_frame_rate(0)

    with pytest.raises(Exception):
        audioData.set_frame_rate(-44100)

    with pytest.raises(Exception):
        audioData.set_frame_rate(None)
