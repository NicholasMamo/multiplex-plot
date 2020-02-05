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
		annotation.draw(data, (lpad, axis.get_xlim()[1] - rpad), tpad, wordspacing=wordspacing,
						lineheight=lineheight, align=align)
		return self._draw_tokens(data, wordspacing, lineheight, align,
								 with_legend, lpad, rpad, tpad, *args, **kwargs)
