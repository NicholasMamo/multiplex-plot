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

from text.annotation import Annotation
import drawable
import util

class TestAnnotation(unittest.TestCase):
	"""
	Unit tests for the :class:`text.annotation.Annotation` class.
	"""

	def test_text(self):
		"""
		Test that the text is written correctly.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 2), 0, align='left', va='top')

		drawn_text = self._reconstruct_text(lines)
		self.assertEqual(text, drawn_text)

	def test_align_left(self):
		"""
		Test that when aligning text left, all lines start at the same x-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 2), 0, align='left', va='top')

	def test_align_right(self):
		"""
		Test that when aligning text right, all lines end at the same x-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 2), 0, align='right', va='top')

		x = 0
		for i, tokens in enumerate(lines):
			bb = util.get_bb(viz.figure, viz.axis, tokens[-1])
			if i == 0:
				x = bb.x1

			self.assertEqual(round(x, 5), round(bb.x1, 5))

	def test_align_center(self):
		"""
		Test that when centering text, all of the lines' centers are the same.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 2), 0, align='center', va='top')

		x = 0
		for i, tokens in enumerate(lines[:-1]):
			bb0 = util.get_bb(viz.figure, viz.axis, tokens[0])
			bb1 = util.get_bb(viz.figure, viz.axis, tokens[-1])
			center = (bb0.x0 + bb1.x1) / 2.
			if i == 0:
				x = center

			self.assertEqual(round(x, 5), round(center, 5))

	def test_align_justify(self):
		"""
		Test that when justifying text, all lines start and end at the same x-coordinate.
		The calculation is made on the center since the bboxes of text do not start or end at the exact same coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 2), 0, align='justify', va='top')

		x = 0
		for i, tokens in enumerate(lines[:-1]): # skip the last line as it is not justified
			bb0 = util.get_bb(viz.figure, viz.axis, tokens[0])
			bb1 = util.get_bb(viz.figure, viz.axis, tokens[-1])
			center = (bb0.x0 + bb1.x1) / 2.
			if i == 0:
				x = center

			self.assertEqual(round(x, 5), round(center, 5))

	def test_align_justify_left(self):
		"""
		Test that when justifying text with the last line being left-aligned, the last line starts at x-coordinate 0.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 2), 0, align='justify-start', va='top')

		bb = util.get_bb(viz.figure, viz.axis, lines[0][0])
		self.assertEqual(0, bb.x0)

	def test_align_justify_right(self):
		"""
		Test that when justifying text with the last line being right-aligned, the last line ends at the farthest right.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 2), 0, align='justify-end', va='top')

		bb = util.get_bb(viz.figure, viz.axis, lines[0][-1])
		self.assertEqual(2, round(bb.x1, 5))

	def test_align_justify_center(self):
		"""
		Test that when justifying text with the last line centered, all lines have the exact same center.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 1), 0, align='justify-center', va='top')

		x = 0
		for i, tokens in enumerate(lines):
			bb0 = util.get_bb(viz.figure, viz.axis, tokens[0])
			bb1 = util.get_bb(viz.figure, viz.axis, tokens[-1])
			center = (bb0.x0 + bb1.x1) / 2.
			if i == 0:
				x = center

			self.assertEqual(round(x, 5), round(center, 5))

	def test_align_invalid(self):
		"""
		Test that when an invalid alignment is given, a :class:`ValueError` is raised.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		self.assertRaises(ValueError, annotation.draw, text, (0, 2), 0, va='top', align='invalid')

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

		return ' '.join([ ' '.join([ token.get_text() for token in line ]) for line in lines ])
