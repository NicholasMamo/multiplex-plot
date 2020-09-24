"""
Unit tests for the :class:`~slope.slope.Slope` class.
"""

import matplotlib.pyplot as plt
import os
import pandas as pd
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..')
if path not in sys.path:
    sys.path.insert(1, path)

from tests.test import MultiplexTest
import drawable
import util

class TestSlope(MultiplexTest):
    """
    Unit tests for the :class:`~slope.slope.Slope` class.
    """
