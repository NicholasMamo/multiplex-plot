"""
The :class:`text.annotation.TextAnnotation` class is mainly concerned with organizing text.
You can do just about anything with these visualizations, including—unsurprisingly enough—annotating the text.

To get started with a :class:`text.annotation.TextAnnotation` visualization, create an instance of it and call the :meth:`text.annotation.TextAnnotation.draw` method.
This method expects, at the very least, a `list` of text tokens.
Alternatively, you can provide a `list` of `dict` of tokens containing at least a `text` attribute and any of the other keys:

.. code-block:: python

	{
	  'label': None,
	  'style': { 'facecolor': 'None' },
	  'text': 'token',
	}

Instructions on how the text should be formatted can be passed on to the :meth:`text.annotation.TextAnnotation.draw` method.
Among others, these attributes include alignment and the line height.
The text can also be styled by passing on any attributes supported by the :class:`matplotlib.text.Text` class.
The same attributes can be passed on to the `style` key in the code block above.
You can find examples to help you get started `here <https://github.com/NicholasMamo/multiplex-plot/blob/master/examples/2.%20Text.ipynb>`_.
"""

import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

class TextAnnotation():
	"""
	A class of visualization that allows text annotations.
	The :class:`text.annotation.TextAnnotation` is mainly concered with organizing text.

	:ivar drawable: The axis where the text annotation visualization will be drawn.
	:vartype drawable: :class:`drawable.Drawable`
	"""

	def __init__(self, drawable):
		"""
		Initialize the text annotation with the figure and axis.
		The figure is used to get the renderer.
		The visualization is drawn on the given axis.

		:param drawable: The axis where the text annotation visualization will be drawn.
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

		return self._draw_tokens(data, wordspacing, lineheight, align,
								 with_legend, lpad, rpad, tpad, *args, **kwargs)

	def _draw_tokens(self, tokens, wordspacing, lineheight,
					 align, with_legend, lpad, rpad, tpad, *args, **kwargs):
		"""
		Draw the tokens on the plot.

		:param tokens: The text tokens to draw.
					   The method expects a `list` of tokens, each one a `dict`.
		:type tokens: list of str
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
					 The left padding and the right padding cannot reach or exceed 100%.
		:type lpad: float
		:param rpad: The right padding as a percentage of the plot.
					 The range is expected to be between 0 and 1.
					 The left padding and the right padding cannot reach or exceed 100%.
		:type rpad: float
		:param tpad: The top padding as a percentage of the plot.
					 Any value greater or equal than 0 is accepted.
		:type tpad: float

		:return: The drawn lines.
				 Each line is made up of tuples of lists.
				 The first list in each tuple is the list of legend labels.
				 The second list in each tuple is the list of actual tokens.
		:rtype: list of tuple
		"""

		axis = self.drawable.axis
		figure = self.drawable.figure

		punctuation = [ ',', '.', '?', '!', '\'', '"', ')' ]
		x_lim = (
			axis.get_xlim()[1] * lpad,
			axis.get_xlim()[1] * (1. - rpad)
		)

		"""
		Go through each token and draw it on the axis.
		"""
		drawn_lines = []
		linespacing = self._get_linespacing(*args, **kwargs) * lineheight
		offset, lines = x_lim[0], 0
		line_tokens, labels, line_labels = [], [], []
		for token in tokens:
			"""
			If the token is a punctuation mark, do not add wordspacing to it.
			"""
			if token.get('text') in punctuation:
				offset -= wordspacing * 1.5

			"""
			Draw the text token.
			"""
			text = self._draw_token(
				token.get('text'), token.get('style', {}), offset, lines,
				wordspacing, linespacing, va='top', *args, **kwargs
			)
			line_tokens.append(text)

			"""
			If the token exceeds the x-limit, break line.
			The offset is reset to the left, and a new line is added.
			The token is moved to this new line.
			Lines do not break on certain types of punctuation.
			"""
			bb = util.get_bb(figure, axis, text)
			if bb.x1 > x_lim[1] and token.get('text') not in punctuation:
				self._newline(line_tokens.pop(-1), lines, linespacing, x_lim[0])
				self._align(
					line_tokens, lines, wordspacing, linespacing,
					self._get_alignment(align), x_lim
				)
				offset, lines = x_lim[0], lines + 1
				drawn_lines.append((line_labels, line_tokens))
				line_tokens, line_labels = [ text ], []

			"""
			If the token has a label associated with it, draw it on the first instance.
			The labels are ordered left-to-right according to when they appeared.
			"""
			if with_legend and 'label' in token and token.get('label') not in labels:
				labels.append(token.get('label'))
				label = self._draw_token(
					token.get('label'), token.get('style', {}), 0, lines,
					wordspacing, linespacing, va='top', *args, **kwargs
				)
				line_labels.append(label)
				self._align(line_labels, lines, wordspacing * 2,
							linespacing, align='right', x_lim=(-1, - wordspacing * 8))

			offset += bb.width + wordspacing

		"""
		Align the last line.
		"""
		drawn_lines.append((line_labels, line_tokens))
		self._align(
			line_tokens, lines, wordspacing, linespacing,
			self._get_alignment(align, last=True), x_lim
		)

		"""
		Move the plot so that it starts from x-coordinate 0.
		Then, re-draw the axis and the figure dimensions.
		The axis and the figure are made to fit the text tightly.
		"""
		self._tighten(drawn_lines)
		axis.set_ylim(-linespacing, lines * linespacing)
		axis_height = axis.get_ylim()[1] - axis.get_ylim()[0]
		axis.set_ylim(axis.get_ylim()[0] - axis_height * tpad, axis.get_ylim()[1])
		axis.invert_yaxis()
		self.drawable.figure.set_figheight((1 + tpad) * lines * lineheight / 2)

		return drawn_lines

	def _get_linespacing(self, *args, **kwargs):
		"""
		Calculate the line spacing.
		The line spacing is calculated by creating a token and getting its height.
		The token is immediately removed.
		The token's styling have to be provided as keyword arguments.

		:return: The line spacing.
		:rtype: float
		"""

		axis = self.drawable.axis
		figure = self.drawable.figure

		"""
		Draw a dummy token and get its height.
		Then, remove that token.
		"""
		token = self._draw_token('None', {}, 0, 0, 0, 0, *args, **kwargs)
		bb = util.get_bb(figure, axis, token)
		height = bb.height
		token.remove()
		return height

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

	def _newline(self, token, line, linespacing, line_start):
		"""
		Create a new line with the given token.

		:param token: The text token to move to the next line.
		:type token: :class:`matplotlib.text.Text`
		:param line: The new line number of the token.
		:type line: int
		:param linespacing: The space between lines.
		:type linespacing: float
		:param line_start: The x-coordinate where the line starts.
		:type line_start: float
		"""

		token.set_position((line_start, (line + 1) * linespacing))

	def _get_alignment(self, align, last=False):
		"""
		Get the proper alignment value for the current line.

		:param align: The provided alignment value.
		:type align: str
		:param last: A boolean indicating whether this is the last line.
					 If it is the last line, alignments like `justify-left` transform into `left`.
					 Otherwise, `justify` is returned.
		:type last: bool

		:return: The alignment value for the current line.
		:rtype: str
		"""

		align = align.lower()
		map = { 'start': 'left', 'end': 'right' }

		alignment = re.findall('(justify)?-?(.+?)$', align)[0]
		if last:
			return 'left' if alignment[1] == 'justify' else map.get(alignment[1], alignment[1])
		else:
			return alignment[0] if alignment[0] else alignment[1]

	def _align(self, tokens, line, wordspacing, linespacing, align='left',
			   x_lim=None, *args, **kwargs):
		"""
		Organize the line tokens.
		This function is used when the line overflows.

		:param tokens: The list of tokens added to the line.
		:type tokens: list of :class:`matplotlib.text.Text`
		:param line: The line number of the tokens.
		:type line: int
		:param wordspacing: The space between words.
		:type wordspacing: float
		:param linespacing: The space between lines.
		:type linespacing: float
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
		:param x_lim: The x-limit relative to which to align the tokens.
					  If it is not given, the axis' x-limit is used instead.
					  The x-limit is a tuple limiting the start and end.
		:type x_lim: tuple
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		punctuation = [ ',', '.', '?', '!', '\'', '"', ')' ]
		x_lim = axis.get_xlim() if x_lim is None else x_lim

		"""
		If the text is left-aligned or justify, move the last token to the next line.

		Otherwise, if the text is right-aligned, move the last token to the next line.
		Then align all the tokens in the last line to the right.
		"""
		if align == 'left':
			pass
		elif align == 'justify':
			"""
			If the alignment is justified, add space between text tokens to fill the line.
			"""
			text_tokens = [ token for token in tokens if token.get_text() not in punctuation ]

			"""
			Calculate the total space between tokens.

			Use this space to calculate the total projected space after justification.
			The process therefore first calculates the space between tokens.
			Then, it calculates the empty space to fill the line.
			"""
			space = 0
			for i in range(len(text_tokens) - 1):
				space += (util.get_bb(figure, axis, text_tokens[i + 1]).x0 -
						  util.get_bb(figure, axis, text_tokens[i]).x1)

			last = util.get_bb(figure, axis, tokens[-1])
			space = space + x_lim[1] - last.x1
			space = space / (len(text_tokens) - 1)

			wordspacing_px = (axis.transData.transform((space, 0))[0] -
							  axis.transData.transform((0, 0))[0])

			"""
			Re-position the tokens.
			"""
			offset = x_lim[0]
			for token in tokens:
				if token.get_text() in punctuation:
					token.set_position((offset - space * 1.25, line * linespacing))
				else:
					token.set_position((offset, line * linespacing))
					bb = token.get_bbox_patch()
					token.set_bbox(dict(
						facecolor=bb.get_facecolor(), edgecolor=bb.get_edgecolor(),
						pad=wordspacing_px / 2.))
					bb = util.get_bb(figure, axis, token)
					offset += bb.width + space
		elif align == 'right':
			if len(tokens):
				"""
				Start moving the tokens to the back of the line in reverse.
				"""

				offset = 0
				for token in tokens[::-1]:
					bb = util.get_bb(figure, axis, token)
					offset += bb.width
					token.set_position((x_lim[1] - offset, bb.y1))

					"""
					Do not add to the offset if the token is a punctuation mark.
					"""
					if token.get_text() not in punctuation:
						offset += wordspacing
		elif align == 'center':
			if len(tokens):
				"""
				Calculate the space that is left in the line.
				Then, halve it and move all tokens by that value.
				"""

				bb = util.get_bb(figure, axis, tokens[-1])
				offset = (x_lim[1] - bb.x1)/2.

				for token in tokens:
					bb = util.get_bb(figure, axis, token)
					token.set_position((bb.x0 + offset, bb.y1))
		else:
			raise ValueError("Unsupported alignment %s" % align)

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
			tokens = labels + tokens
			for token in tokens:
				bb = util.get_bb(figure, axis, token)
				token.set_position((bb.x0 - x_offset, bb.y0 - y_offset))
