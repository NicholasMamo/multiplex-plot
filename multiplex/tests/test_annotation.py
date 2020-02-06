"""
Unit tests for the :class:`text.annotation.Annotation` class.
"""

import matplotlib.pyplot as plt
import os
import sys
import unittest

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

import drawable
import util

class TestAnnotation(unittest.TestCase):
	"""
	Unit tests for the :class:`text.annotation.Annotation` class.
	"""

	pass
