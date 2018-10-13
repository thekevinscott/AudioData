import pytest
from ..AudioData.AudioData import AudioData
# import os

# import pydub
from pydub.generators import Sine
# from pydub.generators import Sine, Square, Triangle, Pulse, Sawtooth, WhiteNoise

# @pytest.fixture(scope="session")
# def audio_fixture(tmpdir_factory):
#     fn = tmpdir_factory.mktemp("data").join('tmp.wav')
#     Sine(440).to_audio_segment().export(str(fn), format='wav')
#     return fn

def test_add_data_requires_args():
    """Ensure data gets added correctly"""
    audioData = AudioData()

    with pytest.raises(Exception):
        audioData.add_data()

    with pytest.raises(Exception):
        audioData.add_data(type='train')

def test_add_data_can_read_files_and_discovers_label(tmpdir_factory):
    label = 'foo'
    file = tmpdir_factory.mktemp(label).join('tmp.wav')
    Sine(440).to_audio_segment().export(str(file), format='wav')
    file2 = tmpdir_factory.mktemp(label).join('tmp.wav')
    Sine(440).to_audio_segment().export(str(file2), format='wav')

    audioData = AudioData()
    audioData.add_data(type='train', data=[str(file), str(file2)])
    assert len(audioData._files['train']) == 2
    assert audioData._files['train'][0] == {
        'file': file,
        'label': str(file).split('/')[-2:-1][0]
    }
    assert audioData._files['train'][1] == {
        'file': file2,
        'label': str(file2).split('/')[-2:-1][0]
    }

def test_add_data_can_read_directories(tmpdir_factory):
    file1 = tmpdir_factory.mktemp('dir1').join('tmp.wav')
    Sine(440).to_audio_segment().export(str(file1), format='wav')
    file2 = tmpdir_factory.mktemp('dir2').join('tmp.wav')
    Sine(440).to_audio_segment().export(str(file2), format='wav')

    dir1 = '/'.join(str(file1).split('/')[:-1])
    dir2 = '/'.join(str(file2).split('/')[:-1])

    audioData = AudioData()
    audioData.add_data(type='train', data=[dir1, dir2])
    assert len(audioData._files['train']) == 2
    assert audioData._files['train'][0]['label'] == str(dir1).split('/')[-1:][0]
    assert audioData._files['train'][1]['label'] == str(dir2).split('/')[-1:][0]

def test_add_data_can_read_directories_and_files(tmpdir_factory):
    file1 = tmpdir_factory.mktemp('dir1').join('tmp.wav')
    Sine(440).to_audio_segment().export(str(file1), format='wav')
    file2 = tmpdir_factory.mktemp('dir2').join('tmp.wav')
    Sine(440).to_audio_segment().export(str(file2), format='wav')

    dir1 = '/'.join(str(file1).split('/')[:-1])

    audioData = AudioData()
    audioData.add_data(type='train', data=[dir1, str(file2)])
    assert len(audioData._files['train']) == 2
    assert audioData._files['train'][0]['label'] == str(dir1).split('/')[-1:][0]
    assert audioData._files['train'][1]['file'] == str(file2)
    assert audioData._files['train'][1]['label'] == str(file2).split('/')[-2:-1][0]

def test_add_data_can_accept_a_label(tmpdir_factory):
    file = tmpdir_factory.mktemp('dir').join('tmp.wav')
    Sine(440).to_audio_segment().export(str(file), format='wav')

    audioData = AudioData()
    audioData.add_data(type='train', data=[str(file)], label='foo')
    assert len(audioData._files['train']) == 1
    assert audioData._files['train'][0] == {
        'file': file,
        'label': 'foo',
    }

def test_add_data_can_accept_a_label_for_mixed_files_and_directories(tmpdir_factory):
    file1 = tmpdir_factory.mktemp('dir1').join('tmp.wav')
    Sine(440).to_audio_segment().export(str(file1), format='wav')
    file2 = tmpdir_factory.mktemp('dir2').join('tmp.wav')
    Sine(440).to_audio_segment().export(str(file2), format='wav')

    dir1 = '/'.join(str(file1).split('/')[:-1])

    audioData = AudioData()
    audioData.add_data(type='train', data=[dir1, str(file2)], label='foo')
    assert len(audioData._files['train']) == 2
    assert audioData._files['train'][0]['label'] == 'foo'
    assert audioData._files['train'][1]['file'] == str(file2)
    assert audioData._files['train'][1]['label'] == 'foo'
