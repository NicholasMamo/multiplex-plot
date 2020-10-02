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

    @MultiplexTest.temporary_plot
    def test_fit_axes_no_ticks(self):
        """
        Test that when there are no ticks, fitting the axes changes nothing.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        dummy = DummyVisualization(viz)
        viz.set_yticks([ ])
        xlim = viz.get_xlim()
        dummy._fit_axes()
        self.assertEqual(xlim, viz.get_xlim())

    @MultiplexTest.temporary_plot
    def test_fit_axes_one_tick_left(self):
        """
        Test that when there is one tick, the x-axes start at the minimum point of that tick.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks([ 1 ])

        # make sure that the x-limit moves to the left
        xlim = viz.get_xlim()
        dummy._fit_axes()
        self.assertGreater(xlim[0], viz.get_xlim()[0])

        # make sure the axes limit just includes the label
        labels = viz.get_yticklabels()
        self.assertEqual(1, len(labels))
        limit = util.get_bb(viz.figure, viz.axes, labels[0]).x0
        self.assertEqual(round(limit, 10), round(viz.get_xlim()[0], 10))

    @MultiplexTest.temporary_plot
    def test_fit_axes_one_tick_label_left(self):
        """
        Test that when there is one tick with a custom label, the x-axes start at the minimum point of that label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks([ 1 ])
        viz.set_yticklabels([ 'label' ])

        # make sure that the x-limit moves to the left
        xlim = viz.get_xlim()
        dummy._fit_axes()
        self.assertGreater(xlim[0], viz.get_xlim()[0])

        # make sure the axes limit just includes the label
        labels = viz.get_yticklabels()
        self.assertEqual(1, len(labels))
        limit = util.get_bb(viz.figure, viz.axes, labels[0]).x0
        self.assertEqual(limit, viz.get_xlim()[0])

    @MultiplexTest.temporary_plot
    def test_fit_axes_multiple_ticks_left(self):
        """
        Test that when there are multiple ticks, the x-axes start at the minimum point.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks(range(0, 10))

        # make sure that the x-limit moves to the left
        xlim = viz.get_xlim()
        dummy._fit_axes()
        self.assertGreater(xlim[0], viz.get_xlim()[0])

        # make sure the axes limit just includes the label
        labels = viz.get_yticklabels()
        self.assertEqual(10, len(labels))
        limit = min(util.get_bb(viz.figure, viz.axes, label).x0 for label in labels)
        self.assertEqual(round(limit, 10), round(viz.get_xlim()[0], 10))

    @MultiplexTest.temporary_plot
    def test_fit_axes_multiple_tick_labels_left(self):
        """
        Test that when there are multiple ticks with custom labels, the x-axes start at the minimum point.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks(range(0, 10))
        viz.set_yticklabels([ f"label { i }" for i in range(0, 10) ])

        # make sure that the x-limit moves to the left
        xlim = viz.get_xlim()
        dummy._fit_axes()

        # make sure the axes limit just includes the label
        labels = viz.get_yticklabels()
        self.assertEqual(10, len(labels))
        limit = min(util.get_bb(viz.figure, viz.axes, label).x0 for label in labels)
        self.assertEqual(round(limit, 10), round(viz.get_xlim()[0], 10))

    @MultiplexTest.temporary_plot
    def test_fit_axes_one_tick_right(self):
        """
        Test that when there is one tick, the x-axes end at the maximum point of that tick.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        viz.yaxis().set_label_position("right")
        viz.yaxis().tick_right()
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks([ 1 ])
        labels = viz.get_yticklabels()
        self.assertEqual(1, len(labels))

        # make sure that the x-limit moves to the right
        xlim = viz.get_xlim()
        dummy._fit_axes()
        limit = util.get_bb(viz.figure, viz.axes, labels[0]).x1
        self.assertLess(xlim[1], viz.get_xlim()[1])
        self.assertEqual(round(limit, 10), round(viz.get_xlim()[1], 10))

    @MultiplexTest.temporary_plot
    def test_fit_axes_one_tick_label_right(self):
        """
        Test that when there is one tick with a custom label, the x-axes end at the maximum point of that label.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        viz.yaxis().set_label_position("right")
        viz.yaxis().tick_right()
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks([ 1 ])
        viz.set_yticklabels([ 'label' ])
        labels = viz.get_yticklabels()
        self.assertEqual(1, len(labels))

        # make sure that the x-limit moves to the right
        xlim = viz.get_xlim()
        dummy._fit_axes()
        limit = util.get_bb(viz.figure, viz.axes, labels[0]).x1
        self.assertLess(xlim[1], viz.get_xlim()[1])
        self.assertEqual(limit, viz.get_xlim()[1])

    @MultiplexTest.temporary_plot
    def test_fit_axes_multiple_ticks_right(self):
        """
        Test that when there are multiple ticks, the x-axes end at the maximum point.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        viz.yaxis().set_label_position("right")
        viz.yaxis().tick_right()
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks(range(1, 10))
        labels = viz.get_yticklabels()
        self.assertEqual(9, len(labels))

        # make sure that the x-limit moves to the right
        xlim = viz.get_xlim()
        dummy._fit_axes()
        limit = max(util.get_bb(viz.figure, viz.axes, label).x1 for label in labels)
        self.assertLess(xlim[1], viz.get_xlim()[1])
        self.assertEqual(round(limit, 10), round(viz.get_xlim()[1], 10))

    @MultiplexTest.temporary_plot
    def test_fit_axes_multiple_tick_labels_right(self):
        """
        Test that when there are multiple ticks with custom labels, the x-axes end at the maximum point.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        viz.yaxis().set_label_position("right")
        viz.yaxis().tick_right()
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks(range(0, 10))
        viz.set_yticklabels([ f"label { i }" for i in range(0, 10) ])
        labels = viz.get_yticklabels()
        self.assertEqual(10, len(labels))

        # make sure that the x-limit moves to the right
        xlim = viz.get_xlim()
        dummy._fit_axes()
        limit = max(util.get_bb(viz.figure, viz.axes, label).x1 for label in labels)
        self.assertLess(xlim[1], viz.get_xlim()[1])
        self.assertEqual(round(limit, 10), round(viz.get_xlim()[1], 10))

    @MultiplexTest.temporary_plot
    def test_fit_axes_multiple_tick_both_sides(self):
        """
        Test that when there are multiple ticks with custom labels on both sides, the x-axes fit both.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        viz.tick_params(labelright=True)
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks(range(0, 10))
        viz.set_yticklabels([ f"label { i }" for i in range(0, 10) ])
        labels = viz.get_yticklabels()
        self.assertEqual(20, len(labels)) # on both sides

        # make sure that the x-limit moves to the right
        xlim = viz.get_xlim()
        dummy._fit_axes()
        llimit = min(util.get_bb(viz.figure, viz.axes, label).x0 for label in labels)
        rlimit = max(util.get_bb(viz.figure, viz.axes, label).x1 for label in labels)
        self.assertGreater(xlim[0], viz.get_xlim()[0])
        self.assertLess(xlim[1], viz.get_xlim()[1])

    @MultiplexTest.temporary_plot
    def test_fit_axes_secondary_labels(self):
        """
        Test that when there is a secondary axes, the y-ticks are taken from it.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        viz.set_yticks([ ])
        viz.secondary = viz.twinx()
        viz.secondary.tick_params(labelleft=True, labelright=True)
        viz.secondary.spines['left'].set_position(('data', 0))
        viz.secondary.spines['right'].set_position(('data', 1))
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.secondary.set_yticks(range(0, 10))
        viz.secondary.set_yticklabels([ f"label { i }" for i in range(0, 10) ])
        self.assertEqual(0, len(viz.get_yticklabels())) # no ticks in the primary axes
        labels = viz.secondary.get_yticklabels()
        self.assertEqual(20, len(labels)) # on both sides

        # make sure that the x-limit moves to the right
        xlim = viz.secondary.get_xlim()
        dummy._fit_axes()
        self.assertGreater(xlim[0], viz.secondary.get_xlim()[0])
        self.assertLess(xlim[1], viz.secondary.get_xlim()[1])
        llimit = min(util.get_bb(viz.figure, viz.axes, label).x0 for label in labels)
        rlimit = max(util.get_bb(viz.figure, viz.axes, label).x1 for label in labels)
        self.assertEqual(round(llimit, 10), round(viz.get_xlim()[0], 10))
        self.assertEqual(round(rlimit, 10), round(viz.get_xlim()[1], 10))

    @MultiplexTest.temporary_plot
    def test_fit_axes_wider(self):
        """
        Test that when the axes are wider than the ticks, fitting the axes changes nothing.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        viz.tick_params(labelright=True)
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks(range(0, 10))
        viz.set_yticklabels([ f"label { i }" for i in range(0, 10) ])
        labels = viz.get_yticklabels()
        self.assertEqual(20, len(labels)) # on both sides
        llimit = min(util.get_bb(viz.figure, viz.axes, label).x0 for label in labels)
        rlimit = max(util.get_bb(viz.figure, viz.axes, label).x1 for label in labels)

        # position the axes
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('data', 0))
        viz.set_xlim((-100, 100))

        # make sure that the x-limit does not move after fitting it
        xlim = viz.get_xlim()
        self.assertLess(xlim[0], llimit)
        self.assertGreater(xlim[1], rlimit)
        dummy._fit_axes()
        self.assertEqual(xlim, viz.get_xlim())

    @MultiplexTest.temporary_plot
    def test_fit_axes_outward(self):
        """
        Test that when fitting outward axes, nothing changes.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('outward', 0))
        viz.axes.spines['right'].set_position(('outward', 1))
        viz.tick_params(labelright=True)
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks(range(0, 10))
        viz.set_yticklabels([ f"label { i }" for i in range(0, 10) ])
        labels = viz.get_yticklabels()
        self.assertEqual(20, len(labels))

        # make sure that the x-limit does not move after fitting it
        xlim = viz.get_xlim()
        dummy._fit_axes()
        self.assertEqual(xlim, viz.get_xlim())

    @MultiplexTest.temporary_plot
    def test_fit_axes_right_outward_only(self):
        """
        Test that when only the right axes are outward, only the left axes change.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('data', 0))
        viz.axes.spines['right'].set_position(('outward', 1))
        viz.tick_params(labelright=True)
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks(range(0, 10))
        viz.set_yticklabels([ f"label { i }" for i in range(0, 10) ])

        # make sure that the x-limit of the left axes changes after fitting the plot
        xlim = viz.get_xlim()
        dummy._fit_axes()
        labels = viz.get_yticklabels()
        self.assertEqual(20, len(labels))
        limit = min(util.get_bb(viz.figure, viz.axes, label).x0 for label in labels)
        self.assertEqual(xlim[1], viz.get_xlim()[1])
        self.assertEqual(limit, viz.get_xlim()[0])

    @MultiplexTest.temporary_plot
    def test_fit_axes_left_outward_only(self):
        """
        Test that when only the left axes are outward, only the right axes change.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        viz.axes.spines['left'].set_position(('outward', 0))
        viz.axes.spines['right'].set_position(('data', 1))
        viz.tick_params(labelright=True)
        dummy = DummyVisualization(viz)

        # set the y-ticks
        viz.set_yticks(range(0, 10))
        viz.set_yticklabels([ f"label { i }" for i in range(0, 10) ])

        # make sure that the x-limit of the left axes changes after fitting the plot
        xlim = viz.get_xlim()
        dummy._fit_axes()
        labels = viz.get_yticklabels()
        self.assertEqual(20, len(labels))
        limit = max(util.get_bb(viz.figure, viz.axes, label).x1 for label in labels)
        self.assertEqual(xlim[0], viz.get_xlim()[0])
        self.assertEqual(round(limit, 10), round(viz.get_xlim()[1], 10))
