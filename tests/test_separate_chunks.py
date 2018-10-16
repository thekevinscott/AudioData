import pytest
import random
from ..AudioData.utils import separate_chunks

random.seed(1)

files = [{
    'audio': 'one',
    'file': 'foo',
    'label': 'foo',
    'start_index': 0,
}, {
    'audio': 'two',
    'file': 'bar',
    'label': 'bar',
    'start_index': 0,
}]

def test_it_returns_nothing_for_no_separations():
    results = separate_chunks(files, [])
    assert results == ()

def test_it_can_return_based_on_a_single_separation():
    audio, = separate_chunks(files, [
        'audio',
    ])
    assert audio == ['one', 'two']

def test_it_can_return_based_on_multiple_separations():
    audio, labels, = separate_chunks(files, [
        'audio',
        'label',
    ])
    assert audio == ['one', 'two']
    assert labels == ['foo', 'bar']

def test_it_returns_all_parts():
    audio, labels, refs = separate_chunks(files, [
        'audio',
        'label',
        [
            'file',
            'start_index',
        ],
    ])
    assert audio == ['one', 'two']
    assert labels == ['foo', 'bar']
    assert refs == [{
        'file': 'foo',
        'start_index': 0,
    }, {
        'file': 'bar',
        'start_index': 0,
    }]
