"""
Unit tests for the :class:`text.annotation.TextAnnotation` class.
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

class TestTextAnnotation(unittest.TestCase):
	"""
	Unit tests for the :class:`text.annotation.TextAnnotation` class.
	"""

	def test_text(self):
		"""
		Test that the text is written correctly.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		lines = viz.draw_text_annotation(text.split())

		drawn_text = self._reconstruct_text(lines)
		self.assertEqual(text, drawn_text)

	def test_text_vertically_aligned(self):
		"""
		Test that each line is vertically-aligned (the y-coordinate is the same for each line's tokens).
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split())

		for _, tokens in lines:
			y = 0
			for i, token in enumerate(tokens):
				bb = util.get_bb(viz.figure, viz.axis, token)
				if i > 0:
					self.assertEqual(y, bb.y0)
				else:
					y = bb.y0

	def test_text_does_not_overlap(self):
		"""
		Test that the lines do not overlap.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split())

		for i, (_, tokens) in enumerate(lines):
			y = 0
			bb = util.get_bb(viz.figure, viz.axis, tokens[0])
			if i > 0:
				self.assertLessEqual(y, bb.y0)

			y = bb.y1

	def test_align_left(self):
		"""
		Test that when aligning text left, all lines start at the same x-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split(), align='left')

		x = 0
		for i, (_, tokens) in enumerate(lines):
			bb = util.get_bb(viz.figure, viz.axis, tokens[0])
			if i == 0:
				x = bb.x0

			self.assertLessEqual(x, bb.x0)

	def test_align_right(self):
		"""
		Test that when aligning text right, all lines end at the same x-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split(), align='right')

		x = 0
		for i, (_, tokens) in enumerate(lines):
			bb = util.get_bb(viz.figure, viz.axis, tokens[-1])
			if i == 0:
				x = bb.x1

			self.assertLessEqual(x, bb.x1)

	def test_align_justify(self):
		"""
		Test that when justifying text, all lines start and end at the same x-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		lines = viz.draw_text_annotation(text.split(), align='justify')

		x0, x1 = 0, 0
		for i, (_, tokens) in enumerate(lines[:-1]):
			bb = util.get_bb(viz.figure, viz.axis, tokens[-1])
			if i == 0:
				x0 = bb.x0
				x1 = bb.x1

			self.assertLessEqual(x0, bb.x0)
			self.assertLessEqual(x1, bb.x1)

	def _reconstruct_text(self, lines):
		"""
		Reconstruct the visualization text from a list of lines.
		The method expects nested lists.
		Each high-level list is a tuple, where the second element is a list of tokens.

		:param lines: A list of lists, each list a line of tokens.
		:type lines: list of list

		:return: The re-constructed text.
		:rtype: str
		"""

		return ' '.join([ ' '.join([ token.get_text() for token in line ]) for _, line in lines ])
