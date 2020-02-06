"""
The :class:`text.text.TextAnnotation` class is aimed to help you create text-only visualizations with ease.
As a visualization, it takes care or organizing text, allowing you to create visualizations by providing as little information as a string.

To start creating text visualizations, create a :class:`text.Text` instance and call the :meth:`text.Text.draw` method.
If you are using the :class:`drawable.Drawable` class, just call the :meth:`drawable.Drawable.draw_text_annotation` method on a :class:`drawable.Drawable` instance instead.

This method expects, at the very least, a string to draw a visualization.
However, you can create richer text visualizations by providing additional parameters.
For example, instead of a string, you can provide a `list` of text tokens to split them however you want.
Or, you can input a `list` of `dict` of tokens containing at least a `text` attribute and any of the other keys:

.. code-block:: python

	{
	  'label': None,
	  'style': { 'facecolor': 'None' },
	  'text': 'token',
	}

Instructions on how the text should be formatted can be passed on to the :meth:`text.text.TextAnnotation.draw` method.
Among others, these attributes include alignment and the line height.
The text can also be styled by passing on any attributes supported by the :class:`matplotlib.text.Text` class.
The same attributes can be passed on to the `style` key in the code block above.
"""

import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '.'))
import util

from annotation import Annotation

class TextAnnotation():
	"""
	A class of visualization that allows text annotations.
	The :class:`text.text.TextAnnotation` is mainly concered with organizing text.

	:ivar drawable: The :class:`drawable.Drawable` where the text visualization will be drawn.
	:vartype drawable: :class:`drawable.Drawable`
	"""

	def __init__(self, drawable):
		"""
		Initialize the text annotation with the figure and axis.
		The figure is used to get the renderer.
		The visualization is drawn on the given axis.

		:param drawable: The :class:`drawable.Drawable` where the text visualization will be drawn.
		:type drawable: :class:`drawable.Drawable`
		"""

		self.drawable = drawable

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
		axis.axis('off')

		"""
		Gradually convert text inputs to dictionary inputs: from `str` to `list`, and from `list` to `dict`.
		"""
		if type(data) is str:
			tokens = data.split()
		else:
			tokens = data

		for i, token in enumerate(tokens):
			if type(token) is str:
				tokens[i] = { 'text': token }

		"""
		Validate the arguments.
		All padding arguments should be non-negative.
		The left-padding and the right-padding should not overlap.
		"""
		if lpad < 0:
			raise ValueError("The left padding should be between 0 and 1, received %d" % lpad)
		if rpad < 0:
			raise ValueError("The right padding should be between 0 and 1, received %d" % rpad)
		if tpad < 0:
			raise ValueError("The top padding should be between 0 and 1, received %d" % tpad)

		if lpad + rpad >= 1:
			raise ValueError("The left and right padding should not overlap, received %d left padding and %d right padding" % (lpad, rpad))

		annotation = Annotation(self.drawable)
		linespacing = util.get_linespacing(figure, axis, wordspacing, *args, **kwargs)
		lines = annotation.draw(tokens, (lpad, axis.get_xlim()[1] - rpad), 0,
								 wordspacing=wordspacing, lineheight=lineheight,
								 align=align, va='top', *args, **kwargs)

		"""
		Draw a legend if it is requested.
		"""
		labels = self._draw_legend(tokens, lines, wordspacing, linespacing, *args, **kwargs) if with_legend else [] * len(lines)
		drawn_lines = zip(labels, lines)
		self._tighten(drawn_lines)

		"""
		Re-draw the axis and the figure dimensions.
		The axis and the figure are made to fit the text tightly.
		"""
		axis.set_ylim(- len(lines) * linespacing, tpad + linespacing)

		return drawn_lines

	def _draw_legend(self, data, tokens, wordspacing, linespacing, *args, **kwargs):
		"""
		Draw a legend by iterating through all the data points.
		The labels are drawn on the same line as the corresponding token.

		:data: The text data as a dictionary.
			   This is used to look for `label` attributes.
		:type data: dict
		:param tokens: The drawn tokens, separated by lines.
		:type tokens: list of list of :class:`matplotlib.text.Text`
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param linespacing: The space between lines.
		:type linespacing: float

		:return: A list of lines, each containing a list of labels on that line.
		:rtype: list of list of :class:`matplotlib.text.Text`
		"""

		labels = []

		figure = self.drawable.figure
		axis = self.drawable.axis
		lines = len(tokens)

		drawn_labels = []
		i = 0
		for line, line_tokens in enumerate(tokens):
			line_labels = []
			for token in line_tokens:
				text = data[i]
				i += 1

				"""
				If the token has a label associated with it, draw it on the first instance.
				The labels are ordered left-to-right according to when they appeared.
				"""
				label = text.get('label', '')
				if label and label not in drawn_labels:
					drawn_labels.append(label)
					label = self._draw_token(
						label, text.get('style', {}), 0, line,
						wordspacing, linespacing, va='top', *args, **kwargs
					)
					line_labels.append(label)


			"""
			Re-align the legend.
			"""
			util.align(figure, axis, line_labels[::-1], 'right', wordspacing * 4,
					   (-1, - wordspacing * 4))

			labels.append(line_labels)

		return labels

	def _draw_token(self, text, style, offset, line, wordspacing, linespacing, *args, **kwargs):
		"""
		Draw the token on the plot.

		:param text: The text token to draw.
		:type text: str
		:param style: The style information for the token.
		:type style: dict
		:param offset: The token's offset.
		:type offset: float
		:param line: The line number of the token.
		:type line: int
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param linespacing: The space between lines.
		:type linespacing: float

		:return: The drawn text box.
		:rtype: :class:`matplotlib.text.Text`
		"""

		axis = self.drawable.axis

		kwargs.update(style)
		"""
		Some styling are set specifically for the bbox.
		"""
		bbox_kwargs = { 'facecolor': 'None', 'edgecolor': 'None' }
		for arg in bbox_kwargs:
			if arg in kwargs:
				bbox_kwargs[arg] = kwargs.get(arg)
				del kwargs[arg]

		"""
		The bbox's padding is calculated in pixels.
		Therefore it is transformed from the provided axis coordinates to pixels.
		"""
		wordspacing_px = (axis.transData.transform((wordspacing, 0))[0] -
						  axis.transData.transform((0, 0))[0])
		text = axis.text(offset, line * linespacing, text,
						 bbox=dict(pad=wordspacing_px / 2., **bbox_kwargs),
						 *args, **kwargs)
		return text

	def _tighten(self, drawn_lines):
		"""
		Move the plot so that it starts from x- and y-coordinate 0.
		This offsets the legend labels so that they start at 0.

		:param drawn_lines: A list of drawn lines.
						   The function expects lines to be tuples of legend labels and tokens.
		:type drawn_lines: list of float
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis
		drawn_lines = list(drawn_lines)

		"""
		Calculate the necessary offset.
		"""
		x_offset = 0
		y_offset = 0
		for (labels, tokens) in drawn_lines:
			for label in labels:
				bb = util.get_bb(figure, axis, label)
				x_offset = min(x_offset, bb.x0)
				y_offset = min(y_offset, bb.y0)

		"""
		Move all tokens by this offset.
		"""
		for (labels, tokens) in drawn_lines:
			for token in labels + tokens:
				bb = util.get_bb(figure, axis, token)
				token.set_position((bb.x0 - x_offset, bb.y0 - y_offset))
