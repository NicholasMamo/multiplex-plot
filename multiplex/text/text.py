"""
The :class:`~TextAnnotation` builds on the :class:`~text.annotation.Annotation`, but is a full-fledged visualization.
That means the :class:`~TextAnnotation` makes it easier to create a visualization and adds other functionality, such as a legend.

As with the :class:`~text.annotation.Annotation`, the :class:`~TextAnnotation` takes care of laying out the text for you.
All you have to do is specify the text to visualize and its style.

To start creating text visualizations, create a :class:`~drawable.Drawable` class and call the :func:`~drawable.Drawable.draw_text_annotation` function.
This method expects, at the very least, a string of text, but you can also pass on other styling options:

.. code-block:: python

    import matplotlib.pyplot as plt
    from multiplex import drawable
    viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
    text = 'Hello world!'
    viz.draw_text_annotation(text, align='justify',
                             fontfamily='serif', alpha=0.9,
                             lineheight=1.25, lpad=0.1, rpad=0.1)
    viz.show()

You can even use the :class:`~TextAnnotation` for more complex visualizations.
For example, instead of a string, you can segment your text into words yourself and style them individually.

.. note::

	You can view more complex text visualization examples in the `Jupyter Notebook tutorial <https://github.com/NicholasMamo/multiplex-plot/blob/master/examples/2.%20Text.ipynb>`_.
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
	The :class:`~TextAnnotation` is mainly concerned with organizing text.
	Like all visualizations, it stores a :class:`~drawable.Drawable` instance and revolves around the :func:`~TextAnnotation.draw` function.

	The main difference from the :class:`~text.annotation.Annotation` is that the :func:`~TextAnnotation.draw` function does not require the x and y positions.
	Instead, this class assumes that the visualization is made up only of text.

	Moreover, the :class:`~TextAnnotation` adds support for a legend.
	The legend is added when tokens have a ``label`` key.
	Therefore the :class:`~TextAnnotation` may only create a legend when tokens are provided as ``dict`` instances.
	"""

	def draw(self, annotation, wordspacing=0.005, lineheight=1.25,
			 align='left', with_legend=True, lpad=0, rpad=0, tpad=0, *args, **kwargs):
		"""
		Draw the text annotation visualization.

		The method expects, at least, the text annotation.
		You can pass on the text as a string, or segment the text into tokens yourself and pass them on as a ``list``.

		You can also split the text into words and pass them on as ``dict`` instances to style them individually.
		Dictionaries should have the following format:

		.. code-block:: python

			{
			  'text': 'token',
			  'style': { 'facecolor': 'None' },
			  'label': None
			}

		Of these keys, only the ``text`` is required.

		You can use the ``style`` to override the general styling options, which you can specify as ``kwargs``.
		Once again, the accepted styling options are those supported by the `matplotlib.text.Text <https://matplotlib.org/3.2.2/api/text_api.html#matplotlib.text.Text>`_ class.

		Use the ``kwargs`` as a general style, and the dictionary's ``style`` as a specific style for each word.
		If you specify a ``kwargs`` styling option, but it is missing from the dictionary's ``style``, the general style is used.

		.. note::

			For example, imagine you specify the text ``color`` to be ``blue`` and the ``fontsize`` to be ``12`` in the ``**kwargs``.
			If in the dictionary's ``style`` of a particular word you set the ``color`` to be ``red``, its color will be ``red``.
			However, since the ``fontsize`` is not specified, it will use the general font size: ``12``.

		The last key is the ``label``.
		If you set a ``label``, Multiplex automatically creates a legend for you.

		:param annotation: The text annotation.
					 The visualization expects a string, a `list` of tokens, or a `list` of `dict` instances as shown above.
		:type annotation: str or list of str or list of dict
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param lineheight: The space between lines.
		:type lineheight: float
		:param align: The text's alignment.
					  Possible values:

					      - ``left``
					      - ``center``
					      - ``right``
					      - ``justify``
					      - ``justify-start`` (or ``justify-left``)
					      - ``justify-center``
					      - ``justify-end`` or (``justify-right``)
		:type align: str
		:param with_legend: A boolean indicating whether the visualization should create a legend when it finds labels.
		:type with_legend: bool
		:param lpad: The left padding as a fraction of the plot.
					 The range is expected to be between 0 and 1.
		:type lpad: float
		:param rpad: The right padding as a fraction of the plot.
					 The range is expected to be between 0 and 1.
		:type rpad: float
		:param tpad: The top padding as a percentage of the plot.
		:type tpad: float

		:return: The drawn lines.
				 Each line is made up of tuples, and each tuple is made up of:

				     1. The list of legend labels in the line, and
				     2. The list of tokens drawn in the line.
		:rtype: list of tuple

		:raises ValueError: When the left padding is not between 0 and 1.
		:raises ValueError: When the right padding is not between 0 and 1.
		:raises ValueError: When the left padding and the right padding combined are larger than 1.
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes

		"""
		Validate the arguments.
		All padding arguments should be non-negative.
		The left-padding and the right-padding should not overlap.
		"""
		if not 0 <= lpad <= 1:
			raise ValueError("The left padding should be between 0 and 1, received %d" % lpad)

		if not 0 <= rpad <= 1:
			raise ValueError("The right padding should be between 0 and 1, received %d" % rpad)

		if lpad + rpad >= 1:
			raise ValueError("The left and right padding should not overlap, received %d left padding and %d right padding" % (lpad, rpad))

		"""
		Gradually convert text inputs to dictionary inputs: from `str` to `list`, and from `list` to `dict`.
		"""
		tokens = annotation.split() if type(annotation) is str else annotation
		tokens = [ { 'text': token } if type(token) is str else token for token in tokens ]

		"""
		Draw the text as an annotation first.
		"""
		annotation = Annotation(self.drawable)
		lines = annotation.draw(tokens, (lpad, axes.get_xlim()[1] - rpad), 0,
								 wordspacing=wordspacing, lineheight=lineheight,
								 align=align, va='top', *args, **kwargs)

		"""
		Draw a legend if it is requested.
		"""
		linespacing = util.get_linespacing(figure, axes, wordspacing, *args, **kwargs)
		labels = self._draw_legend(tokens, lines, wordspacing, linespacing,
								   *args, **kwargs) if with_legend else [ [] ] * len(lines)

		"""
		The entire visualization is shifted so that the legends start at x-coordinate 0.
		This way, the title is aligned with the visualization.
		This process is meant to tighten the layout.
		The axes is turned off since it has no purpose, and the y-limit is re-calculated.
		"""
		drawn_lines = list(zip(labels, lines))
		self._tighten(drawn_lines)
		axes.axis('off')
		axes.set_ylim(- len(lines) * linespacing, tpad + linespacing)

		return drawn_lines

	def _draw_legend(self, annotation, lines, wordspacing, linespacing, *args, **kwargs):
		"""
		Draw a legend by iterating through all the lines.
		The labels are drawn on the same line as the corresponding token.

		:annotation: The text annotation as a dictionary.
			   This is used to look for `label` attributes.
		:type annotation: dict
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
		axes = self.drawable.axes

		"""
		Iterate through each line, and then through each token in that line.
		"""
		drawn_labels = []
		i = 0
		for line, line_tokens in enumerate(lines):
			line_labels = []
			for token in line_tokens:
				label, style = annotation[i].get('label', ''), annotation[i].get('style', { })
				i += 1

				"""
				If the token has a label associated with it, draw it the first time it appears.
				"""
				if label and label not in drawn_labels:
					drawn_labels.append(label)
					token = text_util.draw_token(figure, axes, label, 0, line,
												  style, wordspacing, va='top',
												  *args, **kwargs)
					line_labels.append(token)

			"""
			After drawing the labels on each line, re-align the legend.
			The labels are aligned to the right.
			They are reversed so that the first label appears on the left.
			"""
			util.align(figure, axes, line_labels[::-1], 'right', wordspacing * 4,
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
		axes = self.drawable.axes

		"""
		Calculate the necessary offset.
		"""
		x_offset, y_offset = 0, 0
		for (labels, tokens) in drawn_lines:
			for label in labels:
				bb = util.get_bb(figure, axes, label)
				x_offset = min(x_offset, bb.x0)
				y_offset = min(y_offset, bb.y0)

		"""
		Move all labels and tokens by this offset.
		"""
		for (labels, tokens) in drawn_lines:
			for token in labels + tokens:
				bb = util.get_bb(figure, axes, token)
				token.set_position((bb.x0 - x_offset, bb.y0 - y_offset))
