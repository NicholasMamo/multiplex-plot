"""
Unit tests for the :class:`~Drawable` class.
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
	Unit tests for the :class:`~Drawable` class.
	"""

	def test_caption(self):
		"""
		Test that the caption is set correctly.
		"""

		text = 'caption.'

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption_tokens = viz.set_caption(text)
		caption_text = self._reconstruct_caption(caption_tokens)
		self.assertEqual(text, caption_text)

	def test_caption_removes_multiple_spaces(self):
		"""
		Test that the caption preprocessing removes multiple consecutive spaces.
		"""

		text = """
			This is a multi-level   caption.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption_tokens = viz.set_caption(text)
		caption_text = self._reconstruct_caption(caption_tokens)
		self.assertEqual('This is a multi-level caption.', caption_text)

	def test_caption_removes_tabs(self):
		"""
		Test that the caption preprocessing removes tabs.
		"""

		text = """
			This is a multi-level	caption.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption_tokens = viz.set_caption(text)
		caption_text = self._reconstruct_caption(caption_tokens)
		self.assertEqual('This is a multi-level caption.', caption_text)

	def test_caption_retains_newlines(self):
		"""
		Test that the caption preprocessing does not remove newlines.
		"""

		text = """
			This is a multi-level
			caption.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		caption_tokens = viz.set_caption(text)
		caption_text = self._reconstruct_caption(caption_tokens)
		self.assertEqual('This is a multi-level\ncaption.', caption_text)

	def _reconstruct_caption(self, caption_tokens):
		"""
		Reconstruct the caption text from a list of lines.
		The method expects nested lists.
		Each high-level list is a line, made up of another list of tokens.

		:param caption_tokens: A list of lists, each list a line of tokens.
		:type caption_tokens: list of list

		:return: The re-constructed text.
		:rtype: str
		"""

		return '\n'.join([ ' '.join([ token.get_text() for token in caption_line ]) for caption_line in caption_tokens ])
