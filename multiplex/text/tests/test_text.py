"""
Unit tests for the :class:`~text.text.TextAnnotation` class.
"""

import matplotlib.pyplot as plt
import os
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..')
if path not in sys.path:
	sys.path.insert(1, path)

from tests.test import MultiplexTest
import drawable
import util

class TestTextAnnotation(MultiplexTest):
	"""
	Unit tests for the :class:`~text.text.TextAnnotation` class.
	"""

	@MultiplexTest.temporary_plot
	def test_text(self):
		"""
		Test that the text is written correctly.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		lines = viz.draw_text_annotation(text)

		drawn_text = self._reconstruct_text(lines)
		self.assertEqual(text, drawn_text)

	@MultiplexTest.temporary_plot
	def test_text_vertically_aligned(self):
		"""
		Test that each line is vertically-aligned (the y-coordinate is the same for each line's tokens).
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text)

		for _, tokens in lines:
			y = 0
			for i, token in enumerate(tokens):
				bb = util.get_bb(viz.figure, viz.axes, token)
				if i > 0:
					self.assertEqual(y, bb.y0)
				else:
					y = bb.y0

	@MultiplexTest.temporary_plot
	def test_text_does_not_overlap(self):
		"""
		Test that the lines do not overlap.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text)

		for i, (_, tokens) in enumerate(lines):
			y = 0
			bb = util.get_bb(viz.figure, viz.axes, tokens[0])
			if i > 0:
				self.assertGreaterEqual(y, bb.y0)

			y = bb.y1

	@MultiplexTest.temporary_plot
	def test_align_left(self):
		"""
		Test that when aligning text left, all lines start at the same x-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text, align='left')

		x = 0
		for i, (_, tokens) in enumerate(lines):
			bb = util.get_bb(viz.figure, viz.axes, tokens[0])
			if i == 0:
				x = bb.x0

			self.assertEqual(x, bb.x0)

	@MultiplexTest.temporary_plot
	def test_align_right(self):
		"""
		Test that when aligning text right, all lines end at the same x-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text, align='right')

		x = 0
		for i, (_, tokens) in enumerate(lines):
			bb = util.get_bb(viz.figure, viz.axes, tokens[-1])
			if i == 0:
				x = bb.x1

			self.assertEqual(x, bb.x1)

	@MultiplexTest.temporary_plot
	def test_align_center(self):
		"""
		Test that when centering text, all of the lines' centers are the same.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text, align='center')

		x = 0
		for i, (_, tokens) in enumerate(lines[:-1]):
			bb0 = util.get_bb(viz.figure, viz.axes, tokens[0])
			bb1 = util.get_bb(viz.figure, viz.axes, tokens[-1])
			center = (bb0.x0 + bb1.x1) / 2.
			if i == 0:
				x = center

			self.assertEqual(round(x, 5), round(center, 5))

	@MultiplexTest.temporary_plot
	def test_align_justify(self):
		"""
		Test that when justifying text, all lines start and end at the same x-coordinate.
		The calculation is made on the center since the bboxes of text do not start or end at the exact same coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text, align='justify')

		x = 0
		for i, (_, tokens) in enumerate(lines[:-1]): # skip the last line as it is not justified
			bb0 = util.get_bb(viz.figure, viz.axes, tokens[0])
			bb1 = util.get_bb(viz.figure, viz.axes, tokens[-1])
			center = (bb0.x0 + bb1.x1) / 2.
			if i == 0:
				x = center

			self.assertEqual(round(x, 5), round(center, 5))

	@MultiplexTest.temporary_plot
	def test_align_justify_left(self):
		"""
		Test that when justifying text with the last line being left-aligned, the last line starts at x-coordinate 0.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text, align='justify-start')

		bb = util.get_bb(viz.figure, viz.axes, lines[0][-1][0])
		self.assertEqual(0, bb.x0)

	@MultiplexTest.temporary_plot
	def test_align_justify_right(self):
		"""
		Test that when justifying text with the last line being right-aligned, the last line ends at the farthest right.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text, align='justify-end')

		bb = util.get_bb(viz.figure, viz.axes, lines[0][-1][-1])
		self.assertEqual(viz.axes.get_xlim()[1], bb.x1)

	@MultiplexTest.temporary_plot
	def test_align_justify_center(self):
		"""
		Test that when justifying text with the last line centered, all lines have the exact same center.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text, align='justify-center')

		x = 0
		for i, (_, tokens) in enumerate(lines):
			bb0 = util.get_bb(viz.figure, viz.axes, tokens[0])
			bb1 = util.get_bb(viz.figure, viz.axes, tokens[-1])
			center = (bb0.x0 + bb1.x1) / 2.
			if i == 0:
				x = center

			self.assertEqual(round(x, 5), round(center, 5))

	@MultiplexTest.temporary_plot
	def test_align_invalid(self):
		"""
		Test that when an invalid alignment is given, a :class:`~ValueError` is raised.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_text_annotation, text, align='invalid')

	@MultiplexTest.temporary_plot
	def test_with_legend(self):
		"""
		Test that when a label is given, a legend is drawn.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		tokens = text.split()
		for i, token in enumerate(tokens):
			if token == 'Memphis':
				tokens[i] = {
					'text': token,
					'label': 'name'
				}

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(tokens)
		self.assertTrue(len(lines[0][0]))

	@MultiplexTest.temporary_plot
	def test_without_legend(self):
		"""
		Test that a legend is not drawn when it is disabled, even if labels are given.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		tokens = text.split()
		for i, token in enumerate(tokens):
			if token == 'Memphis':
				tokens[i] = {
					'text': token,
					'label': 'name'
				}

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(tokens, with_legend=False)
		self.assertFalse(len(lines[0][0]))

	@MultiplexTest.temporary_plot
	def test_lpad_bounds(self):
		"""
		Test that the left padding is bound between 0 and 1.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

		"""
		The left padding cannot be negative.
		"""
		self.assertRaises(ValueError, viz.draw_text_annotation, text, lpad=-0.1)

		"""
		A left padding of 0 is allowed.
		"""
		lines = viz.draw_text_annotation(text, lpad=0)
		self.assertTrue(len(lines))

		"""
		The left padding cannot be greater or equal to 1.
		"""
		self.assertRaises(ValueError, viz.draw_text_annotation, text, lpad=1)

	@MultiplexTest.temporary_plot
	def test_rpad_bounds(self):
		"""
		Test that the right padding is bound between 0 and 1.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

		"""
		The right padding cannot be negative.
		"""
		self.assertRaises(ValueError, viz.draw_text_annotation, text, rpad=-0.1)

		"""
		A right padding of 0 is allowed.
		"""
		lines = viz.draw_text_annotation(text, rpad=0)
		self.assertTrue(len(lines))

		"""
		The right padding cannot be greater or equal to 1.
		"""
		self.assertRaises(ValueError, viz.draw_text_annotation, text, rpad=1)

	@MultiplexTest.temporary_plot
	def test_tpad_bounds(self):
		"""
		Test that the top padding has no lower or upper bounds.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))

		"""
		The top padding can be negative.
		"""
		lines = viz.draw_text_annotation(text, tpad=-0.1)
		self.assertTrue(len(lines))

		"""
		A top padding of 0 is allowed.
		"""
		lines = viz.draw_text_annotation(text, tpad=0)
		self.assertTrue(len(lines))

		"""
		A top padding of 1 is allowed.
		"""
		lines = viz.draw_text_annotation(text, tpad=1)
		self.assertTrue(len(lines))

		"""
		A top padding greater than 1 is allowed.
		"""
		lines = viz.draw_text_annotation(text, tpad=1.1)
		self.assertTrue(len(lines))

	@MultiplexTest.temporary_plot
	def test_xpad_bounds(self):
		"""
		Test that the left and right padding cannot occupy the entire axes.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertRaises(ValueError, viz.draw_text_annotation, text, lpad=0.5, rpad=0.5)

	def _reconstruct_text(self, lines):
		"""
		Reconstruct the visualization text from a list of lines.
		The method expects nested lists.
		Each high-level list is a tuple, where the second element is a list of tokens.

		:param lines: A list of lists, representing lines, and each list being a tuple.
					  Each tuple's first element is the legend.
					  Each tuple's second element is the list of tokens.
		:type lines: list of list of tuple

		:return: The re-constructed text.
		:rtype: str
		"""

		return ' '.join([ ' '.join([ token.get_text() for token in line ]) for _, line in lines ])
