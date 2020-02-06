"""
The :class:`text.annotation.Annotation` class is not quite a visualization, but it's an important class nevertheless.
The :class:`text.annotation.Annotation` class is used to draw text on visualizations.
For example, it is used in the :class:`timeseries.timeseries.TimeSeries` visualization to draw text on visualizations and explain them better.

The :class:`text.annotation.Annotation` class is most prominent in the :class:`text.text.TextAnnotation` class, described further down.
The :class:`text.text.TextAnnotation` visualization actually revolves around the annotation and is used to create text-only visualizations.
It also adds some extra functionality to annotations, such as legends.

Look over the :class:`text.annotation.Annotation` class to learn more about what kind of annotations you can create.
If you want to create text-only visualizations, skip ahead to the :class:`text.text.TextAnnotation` class.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

class Annotation():
	"""
	An annotation is a text-only description that is added to visualizations.
	Therefore it is not a visualization in and of itself.
	Text-only visualizations can be created using the :class:`text.text.TextAnnotation` class.

	:ivar drawable: The :class:`drawable.Drawable` where the time series visualization will be drawn.
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

		return self._draw_tokens(tokens, x, y, wordspacing, lineheight, align, va, *args, **kwargs)

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

		punctuation = [ ',', '.', '?', '!', '\'', '"', ')' ]

		"""
		Go through each token and draw it on the axis.
		"""
		drawn_lines = []
		linespacing = util.get_linespacing(figure, axis, wordspacing, *args, **kwargs) * lineheight
		offset, lines = x[0], 0
		line_tokens = []
		for token in tokens:
			"""
			If the token is a punctuation mark, do not add wordspacing to it.
			"""
			if token.get('text') in punctuation:
				offset -= wordspacing * 1.5

			"""
			Draw the text token.
			"""
			if va == 'top':
				text = self._draw_token(
					token.get('text'), offset, y - lines * linespacing,
					token.get('style', {}), wordspacing, linespacing, va=va, *args, **kwargs
				)
			elif va == 'bottom':
				text = self._draw_token(
					token.get('text'), offset, y,
					token.get('style', {}), wordspacing, linespacing, va=va, *args, **kwargs
				)
			line_tokens.append(text)

			"""
			If the token exceeds the x-limit, break it into a new line.
			The offset is reset to the left, and a new line is added.
			The token is moved to this new line.
			Lines do not break on certain types of punctuation.
			"""
			bb = util.get_bb(figure, axis, text)
			if bb.x1 > x[1] and token.get('text') not in punctuation:
				self._newline(line_tokens, drawn_lines, linespacing, x[0], y, va)
				util.align(figure, axis, line_tokens, xpad=wordspacing,
						   align=util.get_alignment(align), xlim=x, va=va)
				offset, lines = x[0], lines + 1
				line_tokens = [ text ]

			offset += bb.width + wordspacing

		"""
		Align the last line.
		"""
		drawn_lines.append(line_tokens)
		util.align(figure, axis, line_tokens, xpad=wordspacing,
				   align=util.get_alignment(align, end=True), xlim=x, va=va)

		return drawn_lines

	def _draw_token(self, text, x, y, style, wordspacing, linespacing, *args, **kwargs):
		"""
		Draw the token on the plot.

		:param text: The text token to draw.
		:type text: str
		:param x: The x-position of the token.
		:type x: int
		:param y: The y-position of the token.
		:type y: int
		:param style: The style information for the token.
		:type style: dict
		:param offset: The token's offset.
		:type offset: float
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param linespacing: The space betw.
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
		text = axis.text(x, y, text,
						 bbox=dict(pad=wordspacing_px / 2., **bbox_kwargs),
						 *args, **kwargs)
		return text

	def _newline(self, line, previous_lines, linespacing, line_start, y, va):
		"""
		Create a new line with the given token.

		:param token: The text token to move to the next line.
		:type token: :class:`matplotlib.text.Text`
		:param line: The latest line.
		:type line: list of :class:`matplotlib.text.Text`
		:param previous_lines: The previously-drawn lines.
		:type previous_lines: list  of list of :class:`matplotlib.text.Text`
		:param linespacing: The space between lines.
		:type linespacing: float
		:param line_start: The x-coordinate where the line starts.
		:type line_start: float
		:param y: The starting y-position of the annotation.
		:type y: float
		:param va: The vertical alignment, can be one of `top` or `bottom`.
				   If the vertical alignment is `bottom`, the annotation grows up.
				   If the vertical alignment is `top`, the annotation grows down.
		:type va: str
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		if va == 'bottom':
			"""
			Move the token into a new line.
			"""
			token = line.pop(-1)
			bb = util.get_bb(figure, axis, token)
			token.set_position((line_start, y))

			"""
			Go through the previous lines and push them up.
			"""
			previous_lines.append(line)
			for line, previous_line in enumerate(previous_lines[::-1]):
				for token in previous_line:
					position = token.get_position()
					bb = util.get_bb(figure, axis, token)
					token.set_position((position[0], y + (line + 1) * linespacing))
		elif va == 'top':
			"""
			Make a new line out of the last token.
			"""
			token = line.pop(-1)
			bb = util.get_bb(figure, axis, token)
			token.set_position((line_start, y - (len(previous_lines) + 1) * linespacing))
			previous_lines.append(line)
