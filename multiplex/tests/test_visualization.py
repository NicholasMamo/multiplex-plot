"""
Unit tests for the :class:`~visualization.Visualization` class.
"""

import matplotlib.pyplot as plt
import os
import string
import sys
import time

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
    sys.path.insert(1, path)

from .test import MultiplexTest
from visualization import DummyVisualization
import drawable
import util

class TestVisualization(MultiplexTest):
    """
    Unit tests for the :class:`~visualization.Visualization` class.
    """

    
