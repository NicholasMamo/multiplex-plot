"""
Unit tests for the :class:`Drawable` class.
"""

import matplotlib.pyplot as plt
import os
import sys
import unittest

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

import drawable

class TestDrawable(unittest.TestCase):
	"""
	Unit tests for the :class:`Drawable` class.
	"""

	def test_caption(self):
		"""
		Test that the caption is set correctly.
		"""

		text = 'caption.'

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption = viz.set_caption(text)
		self.assertEqual(text, caption.get_text())

	def test_caption_removes_multiple_spaces(self):
		"""
		Test that the caption preprocessing removes multiple consecutive spaces.
		"""

		text = """
			This is a multi-level   caption.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption = viz.set_caption(text)
		self.assertEqual('This is a multi-level caption.', caption.get_text())

	def test_caption_removes_tabs(self):
		"""
		Test that the caption preprocessing removes tabs.
		"""

		text = """
			This is a multi-level	caption.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption = viz.set_caption(text)
		self.assertEqual('This is a multi-level caption.', caption.get_text())

	def test_caption_retains_newlines(self):
		"""
		Test that the caption preprocessing does not remove newlines.
		"""

		text = """
			This is a multi-level
			caption.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption = viz.set_caption(text)
		self.assertEqual('This is a multi-level\ncaption.', caption.get_text())
