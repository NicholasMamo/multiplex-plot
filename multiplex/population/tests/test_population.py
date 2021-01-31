"""
Unit tests for the :class:`~population.population.Population` class.
"""

import math
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import os
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..')
if path not in sys.path:
    sys.path.insert(1, path)

from tests.test import MultiplexTest
from population.population import Population
import drawable
import util

class TestPopulation(MultiplexTest):
    """
    Unit tests for the :class:`~population.population.Population` class.
    """
