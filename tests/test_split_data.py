import pytest
import random
from ..AudioData.utils import split_data

random.seed(1)

def test_it_raises_if_too_low_split():
    with pytest.raises(Exception):
        split_data(0.1, ['one', 'two'])

def test_it_raises_if_args_dont_match():
    with pytest.raises(Exception):
        split_data(0.5, ['one', 'two'], ['three'])

def test_it_returns_full_set_if_split_is_none():
    one, = split_data(None, ['one', 'two'])
    assert one == ['one', 'two']

def test_it_returns_full_set_with_tuple_if_split_is_none():
    split_one = split_data(None, ['one', 'two'], ['foo', 'bar'])
    one, two = split_one
    assert one == ['one', 'two']
    assert two == ['foo', 'bar']

def test_it_splits():
    a,b = split_data(0.5, ['one', 'two'])
    one, = a
    two, = b
    assert one == ['one']
    assert two == ['two']

def test_it_splits_tuple():
    a, b = split_data(0.5, ['one', 'two'], ['foo', 'bar'])
    one, foo = a
    two, bar = b
    assert one == ['one']
    assert two == ['two']
    assert foo == ['foo']
    assert bar == ['bar']
