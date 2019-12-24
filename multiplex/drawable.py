"""
All of Multiplex's visualizations revolve around the :class:`Drawable` class.
A :class:`Drawable` is nothing more than a class that wraps a matplotlib figure and an axis.
All of the functions that you would call on a matplotlib axis, you can call on the :class:`Drawable`.
The :class:`Drawable` instance re-routes unknown functions to the matplotlib axis.
However, the :class:`Drawable` also comes with new visualizations to help you explore or explain data faster.

To start working with a :class:`Drawable`, create it from a normal plot:

.. code-block:: python

  viz = drawable.Drawable(plt.figure(figsize=(10, 5)))

If you want to plot on a particular axis, or a subplot, create it as follows instead:

.. code-block:: python

  figure, axis = plt.subplots(2, 1, figsize=(10, 10))
  viz = drawable.Drawable(figure, axis[0])

To learn more about how Multiplex works, keep reading the documentation.
If all you want is to get your hands dirty, take a look at the `examples <https://github.com/NicholasMamo/multiplex-plot/tree/master/examples>`_ directory.
Happy visualizing!
"""

import matplotlib.pyplot as plt
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from text.annotation import TextAnnotation
import util

class Drawable():
	"""
	The :class:`Drawable` class wraps a matplotlib figure and axis to provide additional functionality.
	If no axis is given, the default plot axis (:code:`plt.gca()`) is used.
	The :class:`Drawable` class can be used as a normal :class:`matplotlib.axis.Axis` object with additional functionality.
	The axis functionality can be called on the :class:`Drawable` class.
	The :class:`Drawable` instance re-routes method and attribute calls to the :class:`matplotlib.axis.Axis` instance.

	To create a :class:`Drawable` instance from a normal plot:

	.. code-block:: python

	  viz = drawable.Drawable(plt.figure(figsize=(10, 5)))

	To create a :class:`Drawable` instance from an axis, or a subplot:

	.. code-block:: python

	  figure, axis = plt.subplots(2, 1, figsize=(10, 10))
	  viz = drawable.Drawable(figure, axis[0])

	:ivar figure: The figure that the :class:`Drawable` class wraps.
	:vartype figure: :class:`matplotlib.figure.Figure`
	:ivar axis: The axis where the drawable will draw.
	:vartype axis: :class:`matplotlib.axis.Axis`
	"""

	def __init__(self, figure, axis=None):
		"""
		Create the drawable with the figure.

		:param figure: The figure that the :class:`Drawable` class wraps.
					   This is mainly used to get the figure renderer.
		:type figure: :class:`matplotlib.figure.Figure`
		:param axis: The axis (or subplot) where to plot visualizations.
					 If `None` is not given, the plot's main subplot is used instead.
		:type axis: `None` or :class:`matplotlib.axis.Axis`
		"""

		self.figure = figure
		self.axis = plt.gca() if axis is None else axis

	def set_caption(self, caption, alpha=0.8, ha='left', va='bottom',
					wordspacing=0.005, lineheight=1.25, *args, **kwargs):
		"""
		Add a caption to the subplot.
		The caption is added just beneath the title.
		The method re-draws the title to make space for the caption.

		The caption is a :class:`matplotlib.text.Text` object.
		Any arguments that the constructor accepts can be provided to this method.

		:param caption: The caption to add to the axis.
		:type caption: str
		:param alpha: The opacity of the caption.
					  1 is the maximum opacity, and 0 is the minimum.
		:type alpha: float
		:param ha: The horizontal alignment of the caption.
		:type ha: str
		:param va: The vertical alignment of the caption.
		:type va: str
		:param lineheight: The space between lines.
		:type lineheight: float

		:return: A list of tokens that make up the caption.
		:rtype: list of :class:`matplotlib.text.Text`
		"""

		"""
		Pre-process the caption.
		Remove extra spaces from it.
		"""
		lines = caption.split('\n')
		lines = [ re.sub('([ \t]+)', ' ', line).strip() for line in lines ]
		lines = [ line for line in lines if len(line) ]

		"""
		The caption is constructed bottom-up.
		Each time that a line wraps around, it pushes the already-drawn part up.
		"""
		line_number, linespacing = 0, 0
		caption_tokens = []
		for line in lines[::-1]:
			"""
			Go through each line and draw it word by word.
			"""
			tokens = line.split()
			line_captions = []

			offset, line_wraps = 0, 0
			for token in tokens:
				"""
				Draw the token at the bottom, displacing it by the number of already-drawn lines.
				"""
				caption = self.axis.text(offset, 1 + line_number * linespacing, token, transform=self.axis.transAxes,
										 ha=ha, va=va, alpha=alpha, linespacing=linespacing,
										 *args, **kwargs)

				"""
				Set the linespacing since it depends on the figure height.
				"""
				bb = util.get_bb(self.figure, self.axis, caption, self.axis.transAxes)
				linespacing = bb.height * lineheight

				if bb.x1 > 1:
					"""
					If the token overflows the axis, push all the previous tokens up one line.
					The overflowing token is added to the line instead.
					"""
					caption.set_position((0, 1 + (line_number) * linespacing))
					line_wraps = line_wraps + 1
					offset = 0

					"""
					Push up the previously-drawn tokens in the same line.
					"""
					for other in line_captions:
						position = (other.get_position()[0], other.get_position()[1] + linespacing)
						other.set_position(position)

				"""
				Mark the position of the next token.
				"""
				offset += bb.width + wordspacing
				line_captions.append(caption)

			"""
			The next line starts in a new line.
			The recently-drawn line may contain multiple lines because it wraps around.
			"""
			caption_tokens.insert(0, line_captions)
			line_number += 1 + line_wraps

		"""
		Re-draw the title to make space for the caption.
		"""
		title = self.axis.get_title(loc='left')
		self.axis.set_title(title, loc='left', pad=(5 + 16 * line_number))

		return caption_tokens

	def __getattr__(self, name):
		"""
		Get an attribute indicated by `name` from the class.
		If it gets to this point, then the attribute does not exist.
		Instead, it is retrieved from the :class:`Drawable` axis.

		:param name: The name of the attribute.
		:type name: str

		:return: The function applied on the axis.
		:rtype: function
		"""

		def method(*args, **kwargs):
			"""
			Try to get the attribute from the axis.
			If arguments were given, then the attribute is treated as a method call.
			Otherwise, it is treated as a normal attribute call.
			"""

			if callable(getattr(self.axis, name)):
				return getattr(self.axis, name)(*args, **kwargs)
			else:
				return getattr(self.axis, name)

		return method

	"""
	Visualizations
	"""

	def draw_text_annotation(self, *args, **kwargs):
		"""
		Draw a text annotation visualization on this Drawable.
		The arguments and keyword arguments are those supported by :meth:`text.annotation.TextAnnotation.draw` method.

		:return: The drawn text annotation.
		:rtype: :class:`text.annotation.TextAnnotation`
		"""

		text_annotation = TextAnnotation(self)
		text_annotation.draw(*args, **kwargs)

		return text_annotation
