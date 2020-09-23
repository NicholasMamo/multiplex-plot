"""
General functions for Multiplex unit tests.
"""

import matplotlib.pyplot as plt
import unittest

class MultiplexTest(unittest.TestCase):
    """
    General functions for Multiplex unit tests.
    """

    @staticmethod
    def temporary_plot(f):
        """
        The temporary plot decorator function removes the plot after every test.
        In this way, the memory of the plot is freed.

        :param f: The function to wrap.
        :type f: function
        """

        def wrapper(*args, **kwargs):
            """
            Call the test function with any arguments and keyword arguments.
            Immediately after, close the plot to free the memory.
            """

            f(*args, **kwargs)
            plt.close()

        return wrapper
