"""
Unit tests for the :class:`~bar.100.Bar100` class.
"""

import matplotlib.pyplot as plt
import os
import pandas as pd
import sys

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

from .test import MultiplexTest
import drawable
import util

class TestBar100(MultiplexTest):
	"""
	Unit tests for the :class:`~bar.100.Bar100` class.
	"""
