"""
Unit tests for the :class:`~text.annotation.Annotation` class.
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..')
if path not in sys.path:
    sys.path.insert(1, path)

from tests.test import MultiplexTest
from text.annotation import Annotation
import drawable
import util

class TestAnnotation(MultiplexTest):
    """
    Unit tests for the :class:`~text.annotation.Annotation` class.
    """

    @MultiplexTest.temporary_plot
    def test_draw_save(self):
        """
        Test that when drawing an annotation, the function saves the original annotation, position and style.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, align='left', va='top', color='red')
        self.assertEqual(text, annotation.annotation)
        self.assertEqual((0, 2), annotation.x)
        self.assertEqual(0, annotation.y)
        self.assertEqual({ 'wordspacing': None, 'lineheight': 1.25,
                           'align': 'left', 'va': 'top', 'pad': 0,
                           'color': 'red' }, annotation.style)

    @MultiplexTest.temporary_plot
    def test_draw_text(self):
        """
        Test that the text is written correctly.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, align='left', va='top')
        lines = annotation.draw()

        drawn_text = self._reconstruct_text(lines)
        self.assertEqual(text, drawn_text)

    @MultiplexTest.temporary_plot
    def test_draw_align_left(self):
        """
        Test that when aligning text left, all lines start at the same x-coordinate.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, align='left', va='top')
        lines = annotation.draw()
        self.assertTrue(all( util.get_bb(viz.figure, viz.axes, line[0]).x0 == 0 for line in lines ))

    @MultiplexTest.temporary_plot
    def test_draw_align_right(self):
        """
        Test that when aligning text right, all lines end at the same x-coordinate.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, align='right', va='top')
        lines = annotation.draw()

        x = 0
        for i, lines in enumerate(lines):
            bb = util.get_bb(viz.figure, viz.axes, lines[-1])
            if i == 0:
                x = bb.x1

            self.assertEqual(round(x, 5), round(bb.x1, 5))

    @MultiplexTest.temporary_plot
    def test_draw_align_center(self):
        """
        Test that when centering text, all of the lines' centers are the same.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, align='center', va='top')
        lines = annotation.draw()

        x = 0
        for i, lines in enumerate(lines[:-1]):
            bb0 = util.get_bb(viz.figure, viz.axes, lines[0])
            bb1 = util.get_bb(viz.figure, viz.axes, lines[-1])
            center = (bb0.x0 + bb1.x1) / 2.
            if i == 0:
                x = center

            self.assertEqual(round(x, 5), round(center, 5))

    @MultiplexTest.temporary_plot
    def test_draw_align_justify(self):
        """
        Test that when justifying text, all lines start and end at the same x-coordinate.
        The calculation is made on the center since the bboxes of text do not start or end at the exact same coordinate.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, align='justify', va='top')
        lines = annotation.draw()

        x = 0
        for i, lines in enumerate(lines[:-1]): # skip the last line as it is not justified
            bb0 = util.get_bb(viz.figure, viz.axes, lines[0])
            bb1 = util.get_bb(viz.figure, viz.axes, lines[-1])
            center = (bb0.x0 + bb1.x1) / 2.
            if i == 0:
                x = center

            self.assertEqual(round(x, 5), round(center, 5))

    @MultiplexTest.temporary_plot
    def test_draw_align_justify_left(self):
        """
        Test that when justifying text with the last line being left-aligned, the last line starts at x-coordinate 0.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, align='justify-start', va='top')
        lines = annotation.draw()

        bb = util.get_bb(viz.figure, viz.axes, lines[0][0])
        self.assertEqual(0, bb.x0)

    @MultiplexTest.temporary_plot
    def test_draw_align_justify_right(self):
        """
        Test that when justifying text with the last line being right-aligned, the last line ends at the farthest right.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, align='justify-end', va='top')
        lines = annotation.draw()

        bb = util.get_bb(viz.figure, viz.axes, lines[0][-1])
        self.assertEqual(2, round(bb.x1, 5))

    @MultiplexTest.temporary_plot
    def test_draw_align_justify_center(self):
        """
        Test that when justifying text with the last line centered, all lines have the exact same center.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, align='justify-center', va='top')
        lines = annotation.draw()

        x = 0
        for i, lines in enumerate(lines):
            bb0 = util.get_bb(viz.figure, viz.axes, lines[0])
            bb1 = util.get_bb(viz.figure, viz.axes, lines[-1])
            center = (bb0.x0 + bb1.x1) / 2.
            if i == 0:
                x = center

            self.assertEqual(round(x, 5), round(center, 5))

    @MultiplexTest.temporary_plot
    def test_draw_align_invalid(self):
        """
        Test that when an invalid alignment is given, a :class:`~ValueError` is raised.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, va='top', align='invalid')
        self.assertRaises(ValueError, annotation.draw)

    @MultiplexTest.temporary_plot
    def test_draw_align_top_order(self):
        """
        Test that when the vertical alignment is top, the order of lines is still correct.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='top')
        lines = annotation.draw()

        self.assertEqual('Memphis', lines[0][0].get_text())
        self.assertEqual('ground.', lines[-1][-1].get_text())

    @MultiplexTest.temporary_plot
    def test_draw_align_bottom_order(self):
        """
        Test that when the vertical alignment is bottom, the order of lines is still correct.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='bottom')
        lines = annotation.draw()

        self.assertEqual('Memphis', lines[0][0].get_text())
        self.assertEqual('ground.', lines[-1][-1].get_text())

    @MultiplexTest.temporary_plot
    def test_draw_align_top(self):
        """
        Test that when the alignment is top, all lines are below the provided y-coordinate.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='top')
        lines = annotation.draw()

        bb = util.get_bb(viz.figure, viz.axes, lines[0][0])
        self.assertEqual(0, bb.y1)

        for line in lines:
            self.assertLessEqual(0, bb.y1)

    @MultiplexTest.temporary_plot
    def test_draw_align_bottom(self):
        """
        Test that when the alignment is top, all lines are above the provided y-coordinate.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='bottom')
        lines = annotation.draw()

        bb = util.get_bb(viz.figure, viz.axes, lines[-1][-1])
        self.assertEqual(0, bb.y0)

        for line in lines:
            self.assertGreaterEqual(0, bb.y0)

    @MultiplexTest.temporary_plot
    def test_draw_align_top_line_alignment(self):
        """
        Test that the lines all have the same vertical position when they are aligned to the top.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='top')
        lines = annotation.draw()

        for line in lines:
            bb = util.get_bb(viz.figure, viz.axes, line[0])
            y0 = bb.y0

            for token in line:
                bb = util.get_bb(viz.figure, viz.axes, token)
                self.assertEqual(y0, bb.y0)

    @MultiplexTest.temporary_plot
    def test_draw_align_bottom_line_alignment(self):
        """
        Test that the lines all have the same vertical position when they are aligned to the top.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='bottom')
        lines = annotation.draw()

        for line in lines:
            bb = util.get_bb(viz.figure, viz.axes, line[0])
            y1 = bb.y1

            for token in line:
                bb = util.get_bb(viz.figure, viz.axes, token)
                self.assertEqual(y1, bb.y1)

    @MultiplexTest.temporary_plot
    def test_draw_align_top_lines_do_not_overlap(self):
        """
        Test that when annotations are vertically aligned to the top, the lines do not overlap.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='top')
        lines = annotation.draw()

        for i in range(0, len(lines) - 1):
            bb0 = util.get_bb(viz.figure, viz.axes, lines[i][0])
            bb1 = util.get_bb(viz.figure, viz.axes, lines[i + 1][0])

            self.assertGreaterEqual(bb0.y0, bb1.y1)

    @MultiplexTest.temporary_plot
    def test_draw_align_bottom_lines_do_not_overlap(self):
        """
        Test that when annotations are vertically aligned to the bottom, the lines do not overlap.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='bottom')
        lines = annotation.draw()

        for i in range(0, len(lines) - 1):
            bb0 = util.get_bb(viz.figure, viz.axes, lines[i][0])
            bb1 = util.get_bb(viz.figure, viz.axes, lines[i + 1][0])

            self.assertGreaterEqual(bb0.y0, bb1.y1)

    @MultiplexTest.temporary_plot
    def test_get_virtual_bb_single_token(self):
        """
        Test that the virtual bounding box of an annotation with one token is equivalent to the bounding box of a single token.
        """

        text = 'Memphis'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0)
        lines = annotation.draw()
        bb = util.get_bb(viz.figure, viz.axes, lines[0][0])
        virtual_bb = annotation.get_virtual_bb()
        self.assertEqual(bb.x0, virtual_bb.x0)
        self.assertEqual(bb.y0, virtual_bb.y0)
        self.assertEqual(bb.x1, virtual_bb.x1)
        self.assertEqual(bb.y1, virtual_bb.y1)

    @MultiplexTest.temporary_plot
    def test_get_virtual_bb_line(self):
        """
        Test that the virtual bounding box of an annotation with one line spans the entire line.
        """

        text = 'Memphis Depay plays for Olympique Lyonnais'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0)
        lines = annotation.draw()
        self.assertEqual(1, len(lines))
        virtual_bb = annotation.get_virtual_bb()
        self.assertEqual(util.get_bb(viz.figure, viz.axes, lines[0][0]).x0, virtual_bb.x0)
        self.assertEqual(util.get_bb(viz.figure, viz.axes, lines[0][0]).y0, virtual_bb.y0)
        self.assertEqual(util.get_bb(viz.figure, viz.axes, lines[0][-1]).x1, virtual_bb.x1)
        self.assertEqual(util.get_bb(viz.figure, viz.axes, lines[0][-1]).y1, virtual_bb.y1)

    @MultiplexTest.temporary_plot
    def test_get_virtual_bb_multiple_lines(self):
        """
        Test that the virtual bounding box of an annotation with multiple lines spans the entire block.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0)
        lines = annotation.draw()
        self.assertGreater(len(lines), 1)
        virtual_bb = annotation.get_virtual_bb()
        self.assertEqual(util.get_bb(viz.figure, viz.axes, lines[0][0]).x0, virtual_bb.x0)
        self.assertEqual(util.get_bb(viz.figure, viz.axes, lines[-1][-1]).y0, virtual_bb.y0)
        self.assertEqual(max(util.get_bb(viz.figure, viz.axes, lines[line][-1]).x1 for line in range(0, len(lines))), virtual_bb.x1)
        self.assertEqual(util.get_bb(viz.figure, viz.axes, lines[0][0]).y1, virtual_bb.y1)

    @MultiplexTest.temporary_plot
    def test_center_one_token(self):
        """
        Test that when centering a single token, the middle of the annotation is equivalent to the middle coordinate of the token.
        """

        text = 'Memphis'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='center')
        lines = annotation.draw()
        bb = util.get_bb(viz.figure, viz.axes, lines[0][0])
        self.assertEqual(0, (bb.y1 + bb.y0) / 2.)
        virtual_bb = annotation.get_virtual_bb()
        self.assertEqual(0, (virtual_bb.y1 + virtual_bb.y0) / 2.)

    @MultiplexTest.temporary_plot
    def test_center_one_line(self):
        """
        Test that when centering a single line, each token in that line is centered.
        """

        text = 'Memphis Depay  plays for Olympique Lyonnais'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='center')
        lines = annotation.draw()
        for token in lines[0]:
            bb = util.get_bb(viz.figure, viz.axes, lines[0][0])
            self.assertEqual(0, (bb.y1 + bb.y0) / 2.)

    @MultiplexTest.temporary_plot
    def test_center_multiple_even_lines(self):
        """
        Test that when centering multiple even lines, the block is centered around the given point.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground. Depay began his professional career with PSV Eindhoven.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='center')
        lines = annotation.draw()
        self.assertGreater(len(lines), 1)
        self.assertFalse(len(lines) % 2)
        tokens = [ tokens[0] for tokens in lines ]
        bb1 = util.get_bb(viz.figure, viz.axes, tokens[0])
        bb2 = util.get_bb(viz.figure, viz.axes, tokens[-1])
        self.assertEqual(0, round((bb1.y1 + bb2.y0) / 2., 10))

    @MultiplexTest.temporary_plot
    def test_center_multiple_odd_lines(self):
        """
        Test that when centering multiple odd lines, the block is centered around the given point.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='center')
        lines = annotation.draw()
        self.assertGreater(len(lines), 1)
        self.assertTrue(len(lines) % 2)
        tokens = [ tokens[0] for tokens in lines ]
        bb1 = util.get_bb(viz.figure, viz.axes, tokens[0])
        bb2 = util.get_bb(viz.figure, viz.axes, tokens[-1])
        self.assertEqual(0, round((bb1.y1 + bb2.y0) / 2., 10))

        """
        Check that the middle line is centered.
        """
        bb = util.get_bb(viz.figure, viz.axes, lines[math.floor(len(lines) / 2)][0])
        self.assertEqual(0, round((bb.y1 + bb.y0) / 2., 10))

    @MultiplexTest.temporary_plot
    def test_set_position_top(self):
        """
        Test that when moving an annotation with a `top` vertical alignment, the top of the first line is the given position.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='top')
        annotation.draw()
        annotation.set_position((0, 2), va='top')
        for token in annotation.lines[0]:
            self.assertEqual(2, util.get_bb(viz.figure, viz.axes, token).y1)

    @MultiplexTest.temporary_plot
    def test_set_position_top_below(self):
        """
        Test that when moving an annotation with a `top` vertical alignment, all lines are below the given position.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='top')
        annotation.draw()
        annotation.set_position((0, 2), va='top')
        for line in annotation.lines:
            for token in line:
                self.assertGreaterEqual(2, util.get_bb(viz.figure, viz.axes, token).y1)

    @MultiplexTest.temporary_plot
    def test_set_position_vertical_center(self):
        """
        Test that when moving an annotation with a `center` vertical alignment, the block is centered around the given point.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='center')
        annotation.draw()
        annotation.set_position((0, 2), va='center')
        bb = annotation.get_virtual_bb()
        self.assertEqual(2, (bb.y1 + bb.y0)/2.)

    @MultiplexTest.temporary_plot
    def test_set_position_vertical_center_multiple_even_lines(self):
        """
        Test that when centering multiple even lines vertically, the block is centered around the given point.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground. Depay began his professional career with PSV Eindhoven.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='center')
        annotation.draw()
        annotation.set_position((0, 2), va='center')
        lines = annotation.lines
        self.assertGreater(len(lines), 1)
        self.assertFalse(len(lines) % 2)
        tokens = [ tokens[0] for tokens in lines ]
        bb1 = util.get_bb(viz.figure, viz.axes, tokens[0])
        bb2 = util.get_bb(viz.figure, viz.axes, tokens[-1])
        self.assertEqual(2, round((bb1.y1 + bb2.y0) / 2., 10))

    @MultiplexTest.temporary_plot
    def test_set_position_vertical_center_multiple_odd_lines(self):
        """
        Test that when centering multiple odd lines vertically, the block is centered around the given point.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='center')
        lines = annotation.draw()
        annotation.set_position((0, 2), va='center')
        lines = annotation.lines
        self.assertGreater(len(lines), 1)
        self.assertTrue(len(lines) % 2)
        tokens = [ tokens[0] for tokens in lines ]
        bb1 = util.get_bb(viz.figure, viz.axes, tokens[0])
        bb2 = util.get_bb(viz.figure, viz.axes, tokens[-1])
        self.assertEqual(2, round((bb1.y1 + bb2.y0) / 2., 10))

        """
        Check that the middle line is centered.
        """
        bb = util.get_bb(viz.figure, viz.axes, lines[math.floor(len(lines) / 2)][0])
        self.assertEqual(2, round((bb.y1 + bb.y0) / 2., 10))

    @MultiplexTest.temporary_plot
    def test_set_position_bottom(self):
        """
        Test that when moving an annotation with a `bottom` vertical alignment, the bottom of the last line is the given position.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='bottom')
        annotation.draw()
        annotation.set_position((0, 2), va='bottom')
        for token in annotation.lines[-1]:
            self.assertEqual(2, util.get_bb(viz.figure, viz.axes, token).y0)

    @MultiplexTest.temporary_plot
    def test_set_position_bottom_above(self):
        """
        Test that when moving an annotation with a `bottom` vertical alignment, all lines are above the given position.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='bottom')
        annotation.draw()
        annotation.set_position((0, 2), va='bottom')
        for line in annotation.lines:
            for token in line:
                self.assertLessEqual(2, util.get_bb(viz.figure, viz.axes, token).y0)

    @MultiplexTest.temporary_plot
    def test_set_position_invalid_vertical_alignment(self):
        """
        Test that when setting the position of an annotation with an invalid vertical alignment, a ValueError is raised.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='top')
        annotation.draw()
        self.assertRaises(ValueError, annotation.set_position, (0, 2), va='invalid')

    @MultiplexTest.temporary_plot
    def test_set_position_left(self):
        """
        Test that when moving an annotation with a `left` horizontal alignment, all lines start at the given position.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, align='left')
        annotation.draw()
        annotation.set_position((2, 0), ha='left')
        for tokens in annotation.lines:
            self.assertEqual(2, round(util.get_bb(viz.figure, viz.axes, tokens[0]).x0, 10))

    @MultiplexTest.temporary_plot
    def test_set_position_left_to_the_right(self):
        """
        Test that when moving an annotation with a `left` horizontal alignment, all lines are to the right of the given position.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, align='left')
        annotation.draw()
        annotation.set_position((2, 0), ha='left')
        for line in annotation.lines:
            for token in line:
                self.assertLessEqual(2, round(util.get_bb(viz.figure, viz.axes, token).x0, 10))

    @MultiplexTest.temporary_plot
    def test_set_position_horizontal_center(self):
        """
        Test that when moving an annotation with a `center` horizontal alignment, the block is centered around the given point.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, align='center')
        annotation.draw()
        annotation.set_position((2, 0), ha='center')
        bb = annotation.get_virtual_bb()
        self.assertEqual(2, (bb.x0 + bb.x1)/2.)

    @MultiplexTest.temporary_plot
    def test_set_position_right(self):
        """
        Test that when moving an annotation with a `right` horizontal alignment, all lines end at the given position.
        To carry out this test, the annotation is aligned to the right.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, align='right')
        annotation.draw()
        annotation.set_position((2, 0), ha='right')
        for tokens in annotation.lines:
            self.assertEqual(2, round(util.get_bb(viz.figure, viz.axes, tokens[-1]).x1, 10))

    @MultiplexTest.temporary_plot
    def test_set_position_right_to_the_left(self):
        """
        Test that when moving an annotation with a `right` horizontal alignment, all lines are to the left of the given position.
        To carry out this test, the annotation is aligned to the right.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, align='right')
        annotation.draw()
        annotation.set_position((2, 0), ha='right')
        for line in annotation.lines:
            for token in line:
                self.assertGreaterEqual(2, round(util.get_bb(viz.figure, viz.axes, token).x1, 10))

    @MultiplexTest.temporary_plot
    def test_set_position_invalid_horizontal_alignment(self):
        """
        Test that when setting the position of an annotation with an invalid horizontal alignment, a ValueError is raised.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0)
        annotation.draw()
        self.assertRaises(ValueError, annotation.set_position, (0, 2), ha='invalid')

    @MultiplexTest.temporary_plot
    def test_draw_x_tuple(self):
        """
        Test that when drawing an annotation with a tuple as the x-bounds, the correct bounds are used.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 0.5), 0)
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0, bb.x0)
        self.assertLessEqual(0.49, bb.x1)
        self.assertGreaterEqual(0.5, bb.x1)

    @MultiplexTest.temporary_plot
    def test_draw_x_list(self):
        """
        Test that when drawing an annotation with a list as the x-bounds, the correct bounds are used.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, [0, 0.5], 0)
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0, bb.x0)
        self.assertLessEqual(0.49, bb.x1)
        self.assertGreaterEqual(0.5, bb.x1)

    @MultiplexTest.temporary_plot
    def test_draw_x_np_float(self):
        """
        Test that when drawing an annotation with a numpy float as the x-bounds, the limit of the plot is used.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, 0, 0)
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0, bb.x0)
        self.assertLessEqual(0.95, bb.x1)
        self.assertGreaterEqual(1, bb.x1)

    @MultiplexTest.temporary_plot
    def test_draw_x_float(self):
        """
        Test that when drawing an annotation with a float as the x-bounds, the limit of the plot is used.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, np.float64(0.2), 0)
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(round(0.2, 10), round(bb.x0, 10))
        self.assertLessEqual(0.95, bb.x1)
        self.assertGreaterEqual(1, bb.x1)

    @MultiplexTest.temporary_plot
    def test_draw_x_pad_left(self):
        """
        Test that when padding is applied with `left` alignment, the block moves to the right.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, pad=0.2, align='left')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0.2, round(bb.x0, 10))

    @MultiplexTest.temporary_plot
    def test_draw_x_pad_center(self):
        """
        Test that when padding is applied with `center` alignment, the block is narrower.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, pad=0.2, align='center')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertLessEqual(0.2, round(bb.x0, 10))
        self.assertGreaterEqual(0.8, round(bb.x1, 10))

    @MultiplexTest.temporary_plot
    def test_draw_x_pad_right(self):
        """
        Test that when padding is applied with `right` alignment, the block moves to the left.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, pad=0.2, align='right')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0.8, round(bb.x1, 10))

    @MultiplexTest.temporary_plot
    def test_draw_x_pad_justify_start(self):
        """
        Test that when padding is applied with `justify-start` alignment, the block moves to the right.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, pad=0.2, align='justify-start')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0.2, round(bb.x0, 10))

    @MultiplexTest.temporary_plot
    def test_draw_x_pad_justify_center(self):
        """
        Test that when padding is applied with `justify-center` alignment, the block is narrower.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, pad=0.2, align='justify-center')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0.2, round(bb.x0, 10))
        self.assertGreaterEqual(0.8, round(bb.x1, 10))

    @MultiplexTest.temporary_plot
    def test_draw_x_pad_justify_end(self):
        """
        Test that when padding is applied with `justify-end` alignment, the block moves to the left.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, pad=0.2, align='justify-end')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertGreaterEqual(0.8, round(bb.x1, 10))

    @MultiplexTest.temporary_plot
    def test_draw_x_pad_equal(self):
        """
        Test that when applying padding, the block is equally-narrower on both sides.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, pad=0.2, align='left')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0.2, round(bb.x0, 10))
        self.assertGreaterEqual(0.8, round(bb.x1, 10))

    @MultiplexTest.temporary_plot
    def test_draw_y_pad_top(self):
        """
        Test that when applying padding with `top` vertical alignment, the block moves down.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, pad=0.2, va='top')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(-0.2, round(bb.y1, 10))

    @MultiplexTest.temporary_plot
    def test_draw_y_pad_center(self):
        """
        Test that when applying padding with `center` vertical alignment, the block remains in place.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, pad=0.2, va='center')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0, round((bb.y0 + bb.y1)/2., 10))

    @MultiplexTest.temporary_plot
    def test_draw_y_pad_bottom(self):
        """
        Test that when applying padding with `bottom` vertical alignment, the block moves up.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, pad=0.2, va='bottom')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0.2, round(bb.y0, 10))

    @MultiplexTest.temporary_plot
    def test_redraw_same_text(self):
        """
        Test that when re-drawing an annotation, the same text is used.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 1), 0, va='bottom')
        lines = annotation.draw()
        viz.set_xlim((0, 100))
        self.assertEqual(self._reconstruct_text(lines), self._reconstruct_text(annotation.redraw()))

    @MultiplexTest.temporary_plot
    def test_redraw_same_position(self):
        """
        Test that when re-drawing an annotation, it is placed in the same position.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, align='justify', va='bottom')
        annotation.draw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0, bb.x0)
        self.assertEqual(2, round(bb.x1, 2))

        # increase the limit of the x-axes
        viz.set_xlim((0, 10))
        annotation.redraw()
        bb = annotation.get_virtual_bb()
        self.assertEqual(0, bb.x0)
        self.assertEqual(2, round(bb.x1, 2))

    @MultiplexTest.temporary_plot
    def test_redraw_same_style(self):
        """
        Test that when re-drawing an annotation, it retains the same style.
        """

        text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, va='bottom', color='red')
        lines = annotation.draw()
        self.assertTrue(all( token.get_color() == 'red'
                             for line in lines
                             for token in line ))

        # redraw and re-test
        lines = annotation.redraw()
        self.assertTrue(all( token.get_color() == 'red'
                             for line in lines
                             for token in line ))

    @MultiplexTest.temporary_plot
    def test_redraw_with_custom_style(self):
        """
        Test that when re-drawing an annotation that has a custom style, the new style is used.
        """

        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        text = [{ 'text': 'Memphis', 'style': { 'color': 'red' }  },
                { 'text': 'Depay',   'style': { 'color': 'blue' } }]
        annotation = Annotation(viz, text, (0, 2), 0, va='bottom')
        lines = annotation.draw()
        tokens = [ token for line in lines
                         for token in line ]
        self.assertEqual('red', tokens[0].get_color())
        self.assertEqual('blue', tokens[1].get_color())

        # redraw and re-test
        lines = annotation.redraw()
        tokens = [ token for line in lines
                         for token in line ]
        self.assertEqual('red', tokens[0].get_color())
        self.assertEqual('blue', tokens[1].get_color())

    @MultiplexTest.temporary_plot
    def test_redraw_overlapping(self):
        """
        Test that when re-drawing an annotation, the new annotation's tokens does not overlap.
        """

        text = 'Memphis Depay'
        viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
        annotation = Annotation(viz, text, (0, 2), 0, align='justify', va='bottom')
        lines = annotation.draw()
        tokens = [ token for line in lines
                         for token in line ]
        self.assertFalse(util.overlapping(viz.figure, viz.axes, *tokens))

        # increase the limit of the x-axes
        viz.set_xlim((0, 100))
        self.assertTrue(util.overlapping(viz.figure, viz.axes, *tokens))

        # redraw and the tokens should no longer overlap
        lines = annotation.redraw()
        tokens = [ token for line in lines
                         for token in line ]
        self.assertFalse(util.overlapping(viz.figure, viz.axes, *tokens))

    def _reconstruct_text(self, lines):
        """
        Reconstruct the visualization text from a list of lines.
        The method expects nested lists.
        Each high-level list is a list of tokens.

        :param lines: A list of lists, representing lines, each containing a list of tokens.
        :type lines: list of :class:`matplotlib.text.Text`

        :return: The re-constructed text.
        :rtype: str
        """

        return ' '.join([ ' '.join([ token.get_text() for token in line ]) for line in lines ]).strip()
