"""
The :class:`~Annotation` class is not quite a visualization, but it's an important class nevertheless.
This class is used to draw text on any visualization or matplotlib plot.
For example, it is used in the :class:`~timeseries.timeseries.TimeSeries` visualization to draw text on visualizations and explain them better.
You can also use it on any normal matplotlib plot as long as you wrap it around a :class:`~drawable.Drawable`:

.. code-block:: python

	import matplotlib.pyplot as plt
	from multiplex import drawable
	viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
	annotation = Annotation(viz)
	lines = annotation.draw('Hello world!', (0, 2), 0)

The :class:`~Annotation` class is most prominent in the :class:`~text.text.TextAnnotation` class, described further down.
Text visualizations actually revolve around the basic annotation and use it to create text-only visualizations.
It also adds some extra functionality to annotations, such as legends.

Look over the :class:`~Annotation` class to learn more about what kind of annotations you can create.
If you want to create text-only visualizations, skip ahead to the :class:`~text.text.TextAnnotation` class.
"""

import os
import string
import sys

from matplotlib.transforms import Bbox

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import text_util
import util

class Annotation():
	"""
	An annotation is a text-only description that is added to visualizations.
	Therefore it is not a visualization in and of itself.
	Text-only visualizations can be created using the :class:`~text.text.TextAnnotation` class.

	:ivar drawable: The :class:`~drawable.Drawable` where the time series visualization will be drawn.
	:vartype drawable: :class:`~drawable.Drawable`
	:ivar tokens: The tokens drawn by the annotation.
	:vartype tokens: list of :class:`matplotlib.text.Text`
	"""

	def __init__(self, drawable):
		"""
		Initialize the text annotation with the figure and axis.
		The figure is used to get the renderer.
		The visualization is drawn on the given axis.

		:param drawable: The :class:`~drawable.Drawable` where the text visualization will be drawn.
		:type drawable: :class:`~drawable.Drawable`
		"""

		self.drawable = drawable
		self.tokens = [ ]

	def draw(self, annotation, x, y, wordspacing=0.005, lineheight=1.25,
			 align='left', va='top', *args, **kwargs):
		"""
		Draw the text annotation visualization.
		The method receives text as a list of tokens and draws them as text.

		The text can be provided either as strings or as dictionaries.
		If strings are provided, the function converts them into dictionaries.
		Dictionaries should have the following format:

		.. code-block:: python

			{
			  'style': { 'facecolor': 'None' },
			  'text': 'token',
			}

		Of these keys, only `text` is required.
		The correct styling options are those accepted by the :class:`matplotlib.text.Text` class.
		Anything not given uses default values.

		Any other styling options, common to all tokens, should be provided as keyword arguments.

		:param annotation: The text data.
						   The visualization expects a string, a `list` of tokens, or a `list` of `dict` instances as shown above.
		:type annotation: str or list of str or list of dict
		:param x: The x-position of the annotation.
				  The function expects either a float or a tuple.
				  If a float is given, it is taken to be the start x-position of the annotation.
				  The end x-position is taken from the axis limit.
				  If a tuple is given, the first two values are the start and end x-position of the annotation.
		:type x: float or tuple
		:param y: The starting y-position of the annotation.
		:type y: float
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
		:param va: The vertical alignment, can be one of `top` or `bottom`.
				   If the vertical alignment is `bottom`, the annotation grows up.
				   If the vertical alignment is `top`, the annotation grows down.
		:type va: str

		:return: The drawn annotation's lines.
				 The second list in each tuple is the list of actual tokens.
		:rtype: list of :class:`matplotlib.text.Text`
		"""

		if type(x) is float:
			x = (x, self.drawable.axis.get_xlim()[1])

		"""
		Gradually convert text inputs to dictionary inputs: from `str` to `list`, and from `list` to `dict`.
		"""
		if type(annotation) is str:
			tokens = annotation.split()
		else:
			tokens = annotation

		for i, token in enumerate(tokens):
			if type(token) is str:
				tokens[i] = { 'text': token }

		tokens = self._draw_tokens(tokens, x, y, wordspacing, lineheight, align, va, *args, **kwargs)
		self.tokens.extend(tokens)
		return tokens

	def get_virtual_bb(self, transform=None):
		"""
		Get the bounding box of the entire annotation.
		This is called a virtual bounding box because it is not a real bounding box.
		Rather, it is a bounding box that covers all of the bounding boxes of the annotation's tokens.

		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The bounding box of the annotation.
		:rtype: :class:`matplotlib.transforms.Bbox`
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		transform = axis.transData if transform is None else transform
		renderer = figure.canvas.get_renderer()

		"""
		Go through all the lines and their tokens and get their bounding boxes.
		Compare them with the virtual bounding box and update it as need be.
		"""
		x0, y0, x1, y1 = None, None, None, None
		for line in self.tokens:
			for token in line:
				bb = util.get_bb(figure, axis, token, transform)
				x0 = bb.x0 if x0 is None or bb.x0 < x0 else x0
				y0 = bb.y0 if y0 is None or bb.y0 < y0 else y0
				x1 = bb.x1 if x1 is None or bb.x1 > x1 else x1
				y1 = bb.y1 if y1 is None or bb.y1 > y1 else y1

		return Bbox(((x0, y0), (x1, y1)))

	def set_position(self, position, *args, **kwargs):
		"""
		Move the annotation to the given position.

		:param position: A tuple made up of the new x and y coordinates.
		:type position: tuple
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Calculate the offset by which every token needs to be moved.
		"""
		bb = self.get_virtual_bb()
		offset = (bb.x0 - position[0], bb.y0 - position[1])

		"""
		Go through each token and move them individually.
		"""
		for line in self.tokens:
			for token in line:
				bb = util.get_bb(figure, axis, token)
				token.set_position((bb.x0 - offset[0], bb.y0 - offset[1]))

	def _draw_tokens(self, tokens, x, y, wordspacing, lineheight, align, va, *args, **kwargs):
		"""
		Draw the tokens on the plot.

		:param tokens: The text tokens to draw.
					   The method expects a `list` of tokens, each one a `dict`.
		:type tokens: list of str
		:param x: The start and end x-position of the annotation.
		:type x: tuple
		:param y: The starting y-position of the annotation.
		:type y: float
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
		:param va: The vertical alignment, can be one of `top` or `bottom`.
				   If the vertical alignment is `bottom`, the annotation grows up.
				   If the vertical alignment is `top`, the annotation grows down.
		:type va: str

		:return: The drawn lines.
				 Each line is made up of the text tokens.
		:rtype: list of list of :class:`matplotlib.text.Text`
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		linespacing = util.get_linespacing(figure, axis, wordspacing, *args, **kwargs) * lineheight

		"""
		Go through each token and draw it on the axis.
		"""
		drawn_lines, line_tokens = [], []
		offset = x[0]
		for token in tokens:
			"""
			Draw the text token.
			If the vertical alignment is top, the annotation grows downwards: one line after the other.
			If the vertical alignment is bottom, the annotation grows upwards.
			When the vertical alignment is bottom, new text is always added to the same place.
			New lines push previous lines up.
			"""
			text = text_util.draw_token(figure, axis, token.get('text'), offset,
										y - len(drawn_lines) * linespacing if va == 'top' else y,
										token.get('style', {}), wordspacing, va=va,
										*args, **kwargs)
			line_tokens.append(text)

			"""
			If the token exceeds the x-limit, break it into a new line.
			The offset is reset to the left, and a new line is added.
			The token is moved to this new line.
			Lines do not break on punctuation marks.

			Note that lists are passed by reference.
			Therefore when the last token is removed from drawn lines when create a new line, the change is reflected here.
			"""
			bb = util.get_bb(figure, axis, text)
			if bb.x1 > x[1] and token.get('text') not in string.punctuation:
				self._newline(line_tokens, drawn_lines, linespacing, x[0], y, va)
				util.align(figure, axis, line_tokens, xpad=wordspacing,
						   align=util.get_alignment(align), xlim=x, va=va)
				offset = x[0]
				line_tokens = [ text ]

			offset += bb.width + wordspacing

		"""
		Align the last line.
		"""
		drawn_lines.append(line_tokens)
		util.align(figure, axis, line_tokens, xpad=wordspacing,
				   align=util.get_alignment(align, end=True), xlim=x, va=va)

		return drawn_lines

	def _newline(self, line, previous_lines, linespacing, x, y, va):
		"""
		Create a new line with the given token.

		If the vertical alignment is top, the text grows downwards.
		Therefore the last token added to the line is added to a new line.

		If the vertical alignment is bottom, the text grows upwards.
		Therefore all lines are pushed up by one line.
		The last token added to the line is moved to the start of the line.

		:param line: The latest line.
		:type line: list of :class:`matplotlib.text.Text`
		:param previous_lines: The previously-drawn lines.
		:type previous_lines: list of list of :class:`matplotlib.text.Text`
		:param linespacing: The space between lines.
		:type linespacing: float
		:param x: The x-coordinate where the line starts.
		:type x: float
		:param y: The starting y-position of the annotation.
		:type y: float
		:param va: The vertical alignment, can be one of `top` or `bottom`.
				   If the vertical alignment is `bottom`, the annotation grows up.
				   If the vertical alignment is `top`, the annotation grows down.
		:type va: str
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Remove the last token added to the line.
		This token will make up the new line.
		The line that was being edited, without this token, is added to the list of previous lines—it is 'retired'.
		"""
		token = line.pop(-1)
		bb = util.get_bb(figure, axis, token)
		previous_lines.append(line)

		if va == 'bottom':
			"""
			Move the last token to the start of the line.
			"""
			token.set_position((x, y))

			"""
			Go through the previous lines and push them up.
			"""
			for line, previous_line in enumerate(previous_lines[::-1]):
				for token in previous_line:
					position = token.get_position()
					bb = util.get_bb(figure, axis, token)
					token.set_position((position[0], y + (line + 1) * linespacing))
		elif va == 'top':
			"""
			Move the last token to a new line.
			"""
			token.set_position((x, y - len(previous_lines) * linespacing))

	def __repr__(self):
		"""
		Get the annotation as text.
		The representation is the concatenated text.

		:return: The text representation of the annotation, made up of the annotation text.
		:rtype: str
		"""

		lines = [ ' '.join([ token.get_text() for token in line ]) for line in self.tokens ]
		return ' '.join(lines)
