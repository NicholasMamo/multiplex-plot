"""
Unit tests for the :class:`~text.annotation.Annotation` class.
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
	Unit tests for the :class:`~text.annotation.Annotation` class.
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
		Test that when an invalid alignment is given, a :class:`~ValueError` is raised.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		self.assertRaises(ValueError, annotation.draw, text, (0, 2), 0, va='top', align='invalid')

	def test_align_top_order(self):
		"""
		Test that when the vertical alignment is top, the order of tokens is still correct.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 1), 0, va='top')

		self.assertEqual('Memphis', lines[0][0].get_text())
		self.assertEqual('ground.', lines[-1][-1].get_text())

	def test_align_bottom_order(self):
		"""
		Test that when the vertical alignment is bottom, the order of tokens is still correct.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 1), 0, va='bottom')

		self.assertEqual('Memphis', lines[0][0].get_text())
		self.assertEqual('ground.', lines[-1][-1].get_text())

	def test_align_top(self):
		"""
		Test that when the alignment is top, all lines are below the provided y-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 1), 0, va='top')

		bb = util.get_bb(viz.figure, viz.axis, lines[0][0])
		self.assertEqual(0, bb.y1)

		for line in lines:
			self.assertLessEqual(0, bb.y1)

	def test_align_bottom(self):
		"""
		Test that when the alignment is top, all lines are above the provided y-coordinate.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 1), 0, va='bottom')

		bb = util.get_bb(viz.figure, viz.axis, lines[-1][-1])
		self.assertEqual(0, bb.y0)

		for line in lines:
			self.assertGreaterEqual(0, bb.y0)

	def test_align_top_line_alignment(self):
		"""
		Test that the lines all have the same vertical position when they are aligned to the top.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 1), 0, va='top')

		for line in lines:
			bb = util.get_bb(viz.figure, viz.axis, line[0])
			y0 = bb.y0

			for token in line:
				bb = util.get_bb(viz.figure, viz.axis, token)
				self.assertEqual(y0, bb.y0)

	def test_align_bottom_line_alignment(self):
		"""
		Test that the lines all have the same vertical position when they are aligned to the top.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 1), 0, va='bottom')

		for line in lines:
			bb = util.get_bb(viz.figure, viz.axis, line[0])
			y1 = bb.y1

			for token in line:
				bb = util.get_bb(viz.figure, viz.axis, token)
				self.assertEqual(y1, bb.y1)

	def test_align_top_lines_do_not_overlap(self):
		"""
		Test that when annotations are vertically aligned to the top, the lines do not overlap.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 1), 0, va='top')

		for i in range(0, len(lines) - 1):
			bb0 = util.get_bb(viz.figure, viz.axis, lines[i][0])
			bb1 = util.get_bb(viz.figure, viz.axis, lines[i + 1][0])

			self.assertGreaterEqual(bb0.y0, bb1.y1)

	def test_align_bottom_lines_do_not_overlap(self):
		"""
		Test that when annotations are vertically aligned to the bottom, the lines do not overlap.
		"""

		text = 'Memphis Depay, commonly known simply as Memphis, is a Dutch professional footballer and music artist who plays as a forward and captains French club Lyon and plays for the Netherlands national team. He is known for his pace, ability to cut inside, dribbling, distance shooting and ability to play the ball off the ground.'
		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		annotation = Annotation(viz)
		lines = annotation.draw(text, (0, 1), 0, va='bottom')

		for i in range(0, len(lines) - 1):
			bb0 = util.get_bb(viz.figure, viz.axis, lines[i][0])
			bb1 = util.get_bb(viz.figure, viz.axis, lines[i + 1][0])

			self.assertGreaterEqual(bb0.y0, bb1.y1)

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
