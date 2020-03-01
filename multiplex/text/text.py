"""
The :class:`~TextAnnotation` class is aimed to help you create text-only visualizations with ease.
As a visualization, it takes care or organizing text, allowing you to create visualizations by providing as little information as a string.

To start creating text visualizations, create a :class:`~TextAnnotation` instance and call the :meth:`~TextAnnotation.draw` method.
If you are using the :class:`~drawable.Drawable` class, just call the :meth:`~drawable.Drawable.draw_text_annotation` method on a :class:`~drawable.Drawable` instance instead.

This method expects, at the very least, a string to draw a visualization:

.. code-block:: python

    import matplotlib.pyplot as plt
    from multiplex import drawable
    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    text = 'Hello world!'
    viz.draw_text_annotation(text, align='justify',
                             fontfamily='serif', alpha=0.9,
                             lineheight=1.25, lpad=0.1, rpad=0.1)

However, you can create richer text visualizations by providing additional parameters.
For example, instead of a string, you can provide a `list` of text tokens to split them however you want.
Or, you can input a `list` of `dict` of tokens containing at least a `text` attribute and any of the other keys:

.. code-block:: python

	{
	  'label': None,
	  'style': { 'facecolor': 'None' },
	  'text': 'token',
	}

Instructions on how the text should be formatted can be passed on to the :meth:`~TextAnnotation.draw` method.
Among others, these attributes include alignment and the line height.
The text can also be styled by passing on any attributes supported by the :class:`matplotlib.text.Text` class.
The same attributes can be passed on to the `style` key in the code block above.

.. note::

	More complex text visualization examples are in the `tutorial Jupyter Notebook <https://github.com/NicholasMamo/multiplex-plot/blob/master/examples/2.%20Text.ipynb>`_.
"""

import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '.'))
import text_util
import util

from annotation import Annotation
from visualization import Visualization

class TextAnnotation(Visualization):
	"""
	A class of visualization that allows text annotations.
	The :class:`~TextAnnotation` is mainly concered with organizing text.
	"""

	def draw(self, data, wordspacing=0.005, lineheight=1.25,
			 align='left', with_legend=True, lpad=0, rpad=0, tpad=0, *args, **kwargs):
		"""
		Draw the text annotation visualization.
		The method receives text as a list of tokens and draws them as text.

		The text can be provided either as a string, a list of strings or as dictionaries.
		If strings are provided, the function converts them into dictionaries.
		Dictionaries should have the following format:

		.. code-block:: python

			{
			  'label': None,
			  'style': { 'facecolor': 'None' },
			  'text': 'token',
			}

		Of these keys, only `text` is required.
		The correct styling options are those accepted by the :class:`matplotlib.text.Text` class.
		Anything not given uses default values.

		Any other styling options, common to all tokens, should be provided as keyword arguments.

		:param data: The text data.
					 The visualization expects a string, a `list` of tokens, or a `list` of `dict` instances as shown above.
		:type data: str or list of str or list of dict
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param lineheight: The space between lines.
		:type lineheight: float
		:param align: The text's alignment.
					  Possible values:

					    - left
					    - center
					    - right
					    - justify
					    - justify-start (or justify-left)
					    - justify-center
					    - justify-end or (justify-right)
		:type align: str
		:param with_legend: A boolean indicating whether labels should create a legend.
		:type with_legend: bool
		:param lpad: The left padding as a percentage of the plot.
					 The range is expected to be between 0 and 1.
		:type lpad: float
		:param rpad: The right padding as a percentage of the plot.
					 The range is expected to be between 0 and 1.
		:type rpad: float
		:param tpad: The top padding as a percentage of the plot.
					 The range is expected to be between 0 and 1.
		:type tpad: float

		:return: The drawn lines.
				 Each line is made up of tuples of lists.
				 The first list in each tuple is the list of legend labels.
				 The second list in each tuple is the list of actual tokens.
		:rtype: list of tuple

		:raises: ValueError
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Validate the arguments.
		All padding arguments should be non-negative.
		The left-padding and the right-padding should not overlap.
		"""
		if lpad < 0:
			raise ValueError("The left padding should be between 0 and 1, received %d" % lpad)

		if rpad < 0:
			raise ValueError("The right padding should be between 0 and 1, received %d" % rpad)

		if lpad + rpad >= 1:
			raise ValueError("The left and right padding should not overlap, received %d left padding and %d right padding" % (lpad, rpad))

		"""
		Gradually convert text inputs to dictionary inputs: from `str` to `list`, and from `list` to `dict`.
		"""
		tokens = data.split() if type(data) is str else data
		tokens = [ { 'text': token } if type(token) is str else token for token in tokens ]

		"""
		Draw the text as an annotation first.
		"""
		annotation = Annotation(self.drawable)
		lines = annotation.draw(tokens, (lpad, axis.get_xlim()[1] - rpad), 0,
								 wordspacing=wordspacing, lineheight=lineheight,
								 align=align, va='top', *args, **kwargs)

		"""
		Draw a legend if it is requested.
		"""
		linespacing = util.get_linespacing(figure, axis, wordspacing, *args, **kwargs)
		labels = self._draw_legend(tokens, lines, wordspacing, linespacing,
								   *args, **kwargs) if with_legend else [ [] ] * len(lines)

		"""
		The entire visualization is shifted so that the legends start at x-coordinate 0.
		This way, the title is aligned with the visualization.
		This process is meant to tighten the layout.
		The axis is turned off since it has no purpose, and the y-limit is re-calculated.
		"""
		drawn_lines = list(zip(labels, lines))
		self._tighten(drawn_lines)
		axis.axis('off')
		axis.set_ylim(- len(lines) * linespacing, tpad + linespacing)

		return drawn_lines

	def _draw_legend(self, data, lines, wordspacing, linespacing, *args, **kwargs):
		"""
		Draw a legend by iterating through all the lines.
		The labels are drawn on the same line as the corresponding token.

		:data: The text data as a dictionary.
			   This is used to look for `label` attributes.
		:type data: dict
		:param lines: The drawn lines.
		:type lines: list of list of :class:`matplotlib.text.Text`
		:param wordspacing: The space between tokens.
		:type wordspacing: float
		:param linespacing: The space between lines.
		:type linespacing: float

		:return: A list of lines, each containing a list of labels on that line.
		:rtype: list of list of :class:`matplotlib.text.Text`
		"""

		labels = []

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Iterate through each line, and then through each token in that line.
		"""
		drawn_labels = []
		i = 0
		for line, line_tokens in enumerate(lines):
			line_labels = []
			for token in line_tokens:
				label, style = data[i].get('label', ''), data[i].get('style', { })
				i += 1

				"""
				If the token has a label associated with it, draw it the first time it appears.
				"""
				if label and label not in drawn_labels:
					drawn_labels.append(label)
					token = text_util.draw_token(figure, axis, label, 0, line,
												  style, wordspacing, va='top',
												  *args, **kwargs)
					line_labels.append(token)

			"""
			After drawing the labels on each line, re-align the legend.
			The labels are aligned to the right.
			They are reversed so that the first label appears on the left.
			"""
			util.align(figure, axis, line_labels[::-1], 'right', wordspacing * 4,
					   (-1, - wordspacing * 4))

			labels.append(line_labels)

		return labels

	def _tighten(self, drawn_lines):
		"""
		Move the text visualization so that it starts from x- and y-coordinate 0.

		:param drawn_lines: A list of drawn lines.
						   The function expects lines to be tuples.
						   The first value of each tuple should be the legend labels.
						   The second value of each tuple should be the tokens.
		:type drawn_lines: list of float
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Calculate the necessary offset.
		"""
		x_offset, y_offset = 0, 0
		for (labels, tokens) in drawn_lines:
			for label in labels:
				bb = util.get_bb(figure, axis, label)
				x_offset = min(x_offset, bb.x0)
				y_offset = min(y_offset, bb.y0)

		"""
		Move all labels and tokens by this offset.
		"""
		for (labels, tokens) in drawn_lines:
			for token in labels + tokens:
				bb = util.get_bb(figure, axis, token)
				token.set_position((bb.x0 - x_offset, bb.y0 - y_offset))
