"""
The :class:`text.text.TextAnnotation` class is mainly concerned with organizing text.
You can do just about anything with these visualizations, including—unsurprisingly enough—annotating the text.

To start creating time series visualizations, create a :class:`timeseries.timeseries.TimeSeries` instance and call the :meth:`timeseries.timeseries.TimeSeries.draw` method.
If you are using the :class:`drawable.Drawable` class, just call the :meth:`drawable.Drawable.draw_time_series` method on a :class:`drawable.Drawable` instance instead.

This method expects, at the very least, a `list` of text tokens.
Alternatively, you can provide a `list` of `dict` of tokens containing at least a `text` attribute and any of the other keys:

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
You can find examples to help you get started `here <https://github.com/NicholasMamo/multiplex-plot/blob/master/examples/2.%20Text.ipynb>`_.
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

		The text can be provided either as strings or as dictionaries.
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
					 The visualization expects a `list` of tokens, or a `list` of `dict` instances as shown above.
		:type data: list of str or list of dict
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
		If text tokens are provided, convert them into a dictionary.
		"""
		for i, token in enumerate(data):
			if type(token) is str:
				data[i] = { 'text': token }

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
		tokens = annotation.draw(data, (lpad, axis.get_xlim()[1] - rpad), tpad,
								 wordspacing=wordspacing, lineheight=lineheight,
								 align=align, va='top', *args, **kwargs)

		"""
		Draw a legend if it is requested.
		"""
		legends = self._draw_legend(data, tokens, wordspacing, linespacing, *args, **kwargs) if with_legend else []

		"""
		Re-draw the axis and the figure dimensions.
		The axis and the figure are made to fit the text tightly.
		"""
		lines = len(tokens)
		axis.set_ylim(-linespacing, lines * linespacing)
		axis_height = axis.get_ylim()[1] - axis.get_ylim()[0]
		axis.set_ylim(axis.get_ylim()[0] - axis_height * tpad, axis.get_ylim()[1])
		axis.set_ylim(-lines * linespacing, tpad + linespacing)

		return tokens

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
		"""

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
			offset = 0
			for token in line_labels[::-1]:
				bb = util.get_bb(figure, axis, token)
				offset += bb.width + wordspacing * 2
				token.set_position((- wordspacing * 4 - offset, bb.y1))

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
