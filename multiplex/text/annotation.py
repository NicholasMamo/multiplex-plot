"""
An :class:`~Annotation` is a text-only description that is added to visualizations.
The :class:`~Annotation` class is not quite a visualization, but it's one of Multiplex's most important classes.
It is a tool to help you tell your story.

For example, any visualization based on the :class:`~labelled.LabelledVisualization` class can draw labels—text annotations—anywhere on the plot.
You can also use it on any normal matplotlib plot as long as you wrap it around a :class:`~drawable.Drawable`.
All you have to do is create a :class:`~drawable.Drawable` and call the :func:`~drawable.Drawable.annotate` function.

.. code-block:: python

	import matplotlib.pyplot as plt
	from multiplex import drawable
	viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
	lines = viz.annotate('Hello world!', (0, 2), 0)

Annotations can be as simple as providing a string of text, the x-position, and the y-position, as in the example above.
However, you can also create more complex annotations.
You can even style each word individually!

The :class:`~Annotation` is most important for the :class:`~text.text.TextAnnotation` class.
:class:`~text.text.TextAnnotation` visualizations are made up only of text and revolve around the :class:`~Annotation` class.
It also adds some extra functionality to annotations, such as by drawing legends.

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
	Although the :class:`~Annotation` is not a visualization, it is also based on a :class:`~drawable.Drawable`.
	Moreover, like any :class:`~visualization.Visualization`, it also revolves around the :func:`~Annotation.draw` method.

	Apart from the :class:`~drawable.Drawable`, the :class:`~Annotation` keeps track of the text it has drawn in the ``lines`` instance variable.
	The name of this variable comes from the fact that the :class:`~Annotation` is mainly concerned with organizing the text.
	The annotation draws every bit of the text as a token and organizes these tokens into lines.

	:ivar drawable: The :class:`~drawable.Drawable` where the time series visualization will be drawn.
	:vartype drawable: :class:`~drawable.Drawable`
	:ivar lines: The lines drawn by the annotation.
				 Each line in turn is made up of a list of tokens as :class:`matplotlib.text.Text`.
	:vartype lines: list of list of :class:`matplotlib.text.Text`
	"""

	def __init__(self, drawable):
		"""
		Initialize the :class:`~Annotation` with the :class:`~drawable.Drawable`.
		The :class:`~Annotation` uses the :class:`~drawable.Drawable`'s figure to get the renderer and the axes to draw the text.
		The constructor also creates an instance variable with the lines in the :class:`~Annotation`.

		:param drawable: The :class:`~drawable.Drawable` where the text visualization will be drawn.
		:type drawable: :class:`~drawable.Drawable`
		"""

		self.drawable = drawable
		self.lines = [ ]

	def draw(self, annotation, x, y, wordspacing=None, lineheight=1.25,
			 align='left', va='top', pad=0, *args, **kwargs):
		"""
		Draw a text annotation on the plot.
		This function requires three types of inputs:

			1. The text to draw,
			2. The x-bounds for the annotation, and
			3. The y-position of the annotation.

		You can use the rest of the defined keyword arguments to style the annotation as a whole.
		For example, the ``align`` option aligns the entire annotation.
		Conversely, you can use the keyword arguments (``kwargs``) to style each individual word.
		The accepted styling options are those supported by the `matplotlib.text.Text <https://matplotlib.org/3.2.2/api/text_api.html#matplotlib.text.Text>`_ class.

		You can provide the text either as a string or as a dictionary.
		If you provide a string, the function automatically segments it into words.
		Dictionaries should have the following format:

		.. code-block:: python

			{
			  'text': 'token',
			  'style': { 'facecolor': 'None' }
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

		:param annotation: The text data.
						   The visualization expects a string, a `list` of tokens, or a `list` of `dict` instances as shown above.
		:type annotation: str or list of str or list of dict
		:param x: The x-position of the annotation.
				  The function expects either a float or a tuple.
				  If a float is given, the annotation starts at that x-position and ends at the axes' limit.
				  If a tuple is given, the annotation starts at the first value and ends at the second value.
		:type x: float or tuple
		:param y: The starting y-position of the annotation.
		:type y: float
		:param wordspacing: The space between words.
							If `None` is given, the space is calculated based on the height of the line.
		:type wordspacing: float or None
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
		:param va: The vertical alignment, can be one of:

				       - ``top``: the annotation grows down from the ``y`` position.
				       - ``center``: the annotation is centered around the given ``y`` position.
				       - ``bottom``: the annotation grows up from the ``y`` position.
		:type va: str
		:param pad: The amount of padding applied to the annotation along the x-axis.
					The padding is applied to all sides of the annotation and reduces its size.

					.. note::

						Note that the padding decreases the width of the annotation.
						In CSS terms, the box-sizing is the border box.
		:type pad: float

		:return: The drawn annotation's lines.
				 Each line is made up of a list of tokens.
		:rtype: list of :class:`matplotlib.text.Text`
		"""

		if type(x) is not tuple and type(x) is not list:
			x = (x, self.drawable.axes.get_xlim()[1])

		x, y = self._pad(x, y, pad, va)

		"""
		Gradually convert text inputs to dictionary inputs: from `str` to `list`, and from `list` to `dict`.
		"""
		tokens = annotation.split() if type(annotation) is str else annotation
		for i, token in enumerate(tokens):
			if type(token) is str:
				tokens[i] = { 'text': token }

		tokens = self._draw_tokens(tokens, x, y, wordspacing, lineheight, align, va, *args, **kwargs)
		self.lines.extend(tokens)

		"""
		If the vertical alignment is meant to be centered, center the annotation now.
		"""
		if va == 'center':
			self._center(self.get_virtual_bb().x0, y, *args, **kwargs)

		return tokens

	def get_virtual_bb(self, transform=None):
		"""
		Get the bounding box of the entire :class:`~Annotation`.
		This is called a virtual bounding box because it is not a real bounding box.
		Rather, it is the smallest rectangular bounding box that covers all of the bounding boxes of the :class:`~Annotation`'s tokens.

		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The bounding box of the annotation.
		:rtype: :class:`matplotlib.transforms.Bbox`
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes

		transform = axes.transData if transform is None else transform
		renderer = figure.canvas.get_renderer()

		"""
		Go through all the lines and their tokens and get their bounding boxes.
		Compare them with the virtual bounding box and update it as need be.
		"""
		x0, y0, x1, y1 = None, None, None, None
		for line in self.lines:
			for token in line:
				bb = util.get_bb(figure, axes, token, transform)
				x0 = bb.x0 if x0 is None or bb.x0 < x0 else x0
				y0 = bb.y0 if y0 is None or bb.y0 < y0 else y0
				x1 = bb.x1 if x1 is None or bb.x1 > x1 else x1
				y1 = bb.y1 if y1 is None or bb.y1 > y1 else y1

		return Bbox(((x0, y0), (x1, y1)))

	def set_position(self, position, ha='left', va='top', transform=None,
					 *args, **kwargs):
		"""
		Move the annotation to the given position.
		This function moves all of the tokens stored in the ``lines`` instance variable to its new position.

		.. warning::

			The vertical alignment should be the same as the vertical alignment when the annotation was created.

		:param position: A tuple made up of the new x and y coordinates.
		:type position: tuple
		:param ha: The horizontal alignment, can be one of:

				       - ``left``: the given x-coordinate becomes the leftmost point of the annotation.
				       - ``center``: the given x-coordinate becomes the center point of the annotation.
				       - ``right``: the given x-coordinate becomes the rightmost point of the annotation.
		:type ha: str
		:param va: The vertical alignment, can be one of:

				       - ``top``: the given y-coordinate becomes the highest point of the annotation.
				       - ``center``: the given y-coordinate becomes the center point of the annotation.
				       - ``bottom``: the given y-coordinate becomes the lowest point of the annotation.
		:type va: str
		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:raises ValueError: When the given horizontal alignment is not supported.
		:raises ValueError: When the given vertical alignment is not supported.
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes

		bb = self.get_virtual_bb(transform=transform)
		"""
		Calculate the x-offset by which every token needs to be moved.
		The offset depends on the horizontal alignment.
		"""
		if ha == 'left':
			offset_x = bb.x0 - position[0]
		elif ha == 'center':
			offset_x = (bb.x0 + bb.x1) / 2. - position[0]
		elif ha == 'right':
			offset_x = bb.x1 - position[0]
		else:
			raise ValueError(f"Unsupported horizontal alignment: {ha}")

		"""
		Calculate the y-offset by which every token needs to be moved.
		The offset depends on the vertical alignment.
		"""
		if va == 'top':
			offset_y = bb.y1 - position[1]
		elif va == 'center':
			offset_y = (bb.y1 + bb.y0) / 2. - position[1]
		elif va == 'bottom':
			offset_y = bb.y0 - position[1]
		else:
			raise ValueError(f"Unsupported vertical alignment: {va}")

		offset = (offset_x, offset_y)

		"""
		Go through each token and move them individually.
		"""
		for line in self.lines:
			for token in line:
				bb = util.get_bb(figure, axes, token, transform=transform)
				if va == 'top':
					token.set_position((bb.x0 - offset[0], bb.y1 - offset[1]))
				elif va == 'center':
					token.set_position((bb.x0 - offset[0], bb.y1 - offset[1]))
				elif va == 'bottom':
					token.set_position((bb.x0 - offset[0], bb.y0 - offset[1]))

	def remove(self):
		"""
		Remove all tokens in the annotation from the visualization.
		This function removes all of the :class:`~Annotation`'s text from the plot and then empties the lines.
		"""

		for line in self.lines:
			for token in line:
				token.remove()

		self.lines = [ ]

	def _draw_tokens(self, tokens, x, y, wordspacing, lineheight, align, va,
					 transform=None, *args, **kwargs):
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
							If `None` is given, the space is calculated based on the height of the line.
		:type wordspacing: float or None
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
		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The drawn lines.
				 Each line is made up of the text tokens.
		:rtype: list of list of :class:`matplotlib.text.Text`
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes
		transform = transform if transform is not None else axes.transData

		linespacing = util.get_linespacing(figure, axes, wordspacing, transform=transform, *args, **kwargs) * lineheight
		if wordspacing is None:
			wordspacing = linespacing / 10.

		"""
		Go through each token and draw it on the axes.
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

			Note that the center alignment is not considered here.
			There is no way of knowing how many lines there will be in advance.
			Therefore lines are centered at a later stage.
			"""
			va = 'top' if va == 'center' else va
			text = text_util.draw_token(figure, axes, token.get('text'), offset,
										y - len(drawn_lines) * linespacing if va == 'top' else y,
										token.get('style', {}), wordspacing, va=va,
										transform=transform, *args, **kwargs)
			line_tokens.append(text)

			"""
			If the token exceeds the x-limit, break it into a new line.
			The offset is reset to the left, and a new line is added.
			The token is moved to this new line.
			Lines do not break on punctuation marks.

			Note that lists are passed by reference.
			Therefore when the last token is removed from drawn lines when create a new line, the change is reflected here.
			"""
			bb = util.get_bb(figure, axes, text, transform=transform)
			if bb.x1 > x[1] and token.get('text') not in string.punctuation:
				self._newline(line_tokens, drawn_lines, linespacing, x[0], y, va, transform=transform)
				util.align(figure, axes, line_tokens, xpad=wordspacing,
						   align=util.get_alignment(align), xlim=x, va=va, transform=transform)
				offset = x[0]
				line_tokens = [ text ]

			offset += bb.width + wordspacing

		"""
		Align the last line.
		"""
		drawn_lines.append(line_tokens)
		util.align(figure, axes, line_tokens, xpad=wordspacing,
				   align=util.get_alignment(align, end=True), xlim=x, va=va, transform=transform)

		return drawn_lines

	def _newline(self, line, previous_lines, linespacing, x, y, va, transform=None):
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
		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`
		"""

		figure = self.drawable.figure
		axes = self.drawable.axes

		"""
		Remove the last token added to the line.
		This token will make up the new line.
		The line that was being edited, without this token, is added to the list of previous lines—it is 'retired'.
		"""
		token = line.pop(-1)
		bb = util.get_bb(figure, axes, token, transform=transform)
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
					bb = util.get_bb(figure, axes, token, transform=transform)
					token.set_position((position[0], y + (line + 1) * linespacing))
		elif va == 'top':
			"""
			Move the last token to a new line.
			"""
			token.set_position((x, y - len(previous_lines) * linespacing))

	def _center(self, x, y, transform=None, *args, **kwargs):
		"""
		Center the annotation around the given y-coordinate.

		.. note::

			This function centers all lines in the annotation.

		:param x: The x-coordinate of the lines.
		:type x: float
		:param y: The y-coordinate of the center.
				  The annotation's lines will be centered around this coordinate.
		:type y: float
		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`
		"""

		bb = self.get_virtual_bb(transform=transform)
		self.set_position((x, y + bb.height / 2.))

	def _pad(self, x, y, pad, va):
		"""
		Apply the padding to the given coordinates.
		The way the horizontal padding is applied depends on the alignment.
		The way the vertical padding is applied depends on the vertical alignment.

		:param x: The x-coordinate as a tuple, representing the bounds of the annotation.
		:type x: tuple
		:param y: The starting y-position of the annotation.
		:type y: float
		:param pad: The amount of padding applied to the annotation.
		:type pad: float
		:param va: The vertical alignment, can be one of `top`, `center` or `bottom`.
				   If the vertical alignment is `top`, the annotation grows down.
				   If the vertical alignment is `center`, the annotation is centered around the given y-coordinate.
				   If the vertical alignment is `bottom`, the annotation grows up.
		:type va: str
		"""

		x = self._x_pad(x, pad)
		y = self._y_pad(y, pad, va)
		return x, y

	def _x_pad(self, x, pad):
		"""
		Calculate the x-padding.
		The way that the padding is applied depends on the alignment of the text.

		:param x: The x-coordinate as a tuple, representing the bounds of the annotation.
		:type x: tuple
		:param pad: The padding applied to the annotation.
					The padding is taken to be a fraction of the axes width.
		:type pad: float

		:return: The new x-coordinate tuple with padding applied.
		:rtype: tuple
		"""

		return (x[0] + pad, x[1] - pad)

	def _y_pad(self, y, pad, va):
		"""
		Calculate the x-padding.
		The way that the padding is applied depends on the alignment of the text.

		:param y: The starting y-position of the annotation.
		:type y: float
		:param pad: The padding applied to the annotation.
					The padding is taken to be a fraction of the axes width.
		:type pad: float
		:param va: The vertical alignment, can be one of `top`, `center` or `bottom`.
				   If the vertical alignment is `top`, the annotation grows down.
				   If the vertical alignment is `center`, the annotation is centered around the given y-coordinate.
				   If the vertical alignment is `bottom`, the annotation grows up.
		:type va: str
		"""

		return {
			'top': y - pad,
			'center': y,
			'bottom': y + pad
		}[va]

	def __repr__(self):
		"""
		Get the annotation as text.
		The representation is the concatenated text.

		:return: The text representation of the annotation, made up of the annotation text.
		:rtype: str
		"""

		lines = [ ' '.join([ token.get_text() for token in line ]) for line in self.lines ]
		return ' '.join(lines)
