#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the capacity_mapping module.
"""
import pytest

from capacity_mapping import capacity_mapping


def test_something():
    assert True


def test_with_error():
    with pytest.raises(ValueError):
        # Do something that raises a ValueError
        raise(ValueError)


# Fixture example
@pytest.fixture
def an_object():
    return {}


def test_capacity_mapping(an_object):
    assert an_object == {}
