"""
Unit tests for the :mod:`~util` module.
"""

from matplotlib import lines
import matplotlib.pyplot as plt
import os
import string
import sys

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

from .test import MultiplexTest
import drawable
import util

class TestUtil(MultiplexTest):
	"""
    Unit tests for the :mod:`~util` module.
	"""
