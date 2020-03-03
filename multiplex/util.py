"""
A set of utility functions that are common to all types of visualizations.
"""

import re

def get_bb(figure, axis, component, transform=None):
	"""
	Get the bounding box of the given component.

	:param figure: The figure that the component occupies.
				   This is used to get the figure renderer.
	:type figure: :class:`matplotlib.figure.Figure`
	:param axis: The axis (or subplot) where the component is plotted.
	:type axis: :class:`matplotlib.axis.Axis`
	:param component: The component whose bounding box will be fetched.
	:type component: object
	:param transform: The bounding box transformation.
					  If `None` is given, the data transformation is used.
	:type transform: None or :class:`matplotlib.transforms.TransformNode`

	:return: The bounding box of the text object.
	:rtype: :class:`matplotlib.transforms.Bbox`
	"""

	transform = axis.transData if transform is None else transform

	renderer = figure.canvas.get_renderer()
	bb = component.get_window_extent(renderer).inverse_transformed(transform)
	return bb

def overlapping(figure, axis, c1, c2, *args, **kwargs):
	"""
	Check whether the given components overlap.
	The overlap considers the bounding box, and is therefore not perfectly precise.

	:param figure: The figure that the component occupies.
				   This is used to get the figure renderer.
	:type figure: :class:`matplotlib.figure.Figure`
	:param axis: The axis (or subplot) where the component is plotted.
	:type axis: :class:`matplotlib.axis.Axis`
	:param c1: The first component.
			   Its bounding box will be compared to the second component.
	:type c1: object
	:param c2: The second component.
			   Its bounding box will be compared to the first component.
	:type c2: object

	:return: A boolean indicating whether the two components overlap.
	:rtype: bool
	"""

	bb1, bb2 = get_bb(figure, axis, c1, *args, **kwargs), get_bb(figure, axis, c2, *args, **kwargs)

	return overlapping_bb(b1, b2)

def overlapping_bb(bb1, bb2):
	"""
	Check whether the two given bounding boxes overlap.

	:param bb1: The first bounding box.
	:type bb1: :class:`matplotlib.transforms.Bbox`
	:param bb2: The second bounding box.
	:type bb2: :class:`matplotlib.transforms.Bbox`

	:return: A boolean indicating whether the two bounding boxes overlap.
	:rtype: bool
	"""

	return (
		(bb2.x0 < bb1.x0 < bb2.x1 or bb2.x0 < bb1.x1 < bb2.x1) and
		(bb2.y0 < bb1.y0 < bb2.y1 or bb2.y0 < bb1.y1 < bb2.y1) or
		(bb1.x0 < bb2.x0 < bb1.x1 or bb1.x0 < bb2.x1 < bb1.x1) and
		(bb1.y0 < bb2.y0 < bb1.y1 or bb1.y0 < bb2.y1 < bb1.y1)
	)

def get_linespacing(figure, axis, wordspacing=0, *args, **kwargs):
	"""
	Calculate the line spacing of text tokens.
	The line spacing is calculated by creating a token and getting its height.
	The token is immediately removed.
	The token's styling have to be provided as keyword arguments.

	:param figure: The figure that the component occupies.
				   This is used to get the figure renderer.
	:type figure: :class:`matplotlib.figure.Figure`
	:param axis: The axis (or subplot) where the component is plotted.
	:type axis: :class:`matplotlib.axis.Axis`
	:param wordspacing: The spacing between tokens.
						This is used to be able to create the padding around words.
	:type wordspacing: float

	:return: The line spacing.
	:rtype: float
	"""

	"""
	Draw a dummy token first.
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
	token = axis.text(0, 0, 'None', bbox=dict(pad=wordspacing_px / 2., **bbox_kwargs),
					  *args, **kwargs)

	"""
	Get the height from the bbox.
	"""
	bb = get_bb(figure, axis, token)
	height = bb.height
	token.remove()
	return height

def get_alignment(align, end=False):
	"""
	Get the proper alignment value for the current line.
	This is mainly used for justification values.
	Since the last line of justified items is aligned differently, this function extracts the appropriate value.

	:param align: The provided alignment value.
	:type align: str
	:param end: A boolean indicating whether this is the end of the group of items to be aligned.
				 If it is the end line, alignments like `justify-left` transform into `left`.
				 Otherwise, `justify` is returned.
	:type end: bool

	:return: The alignment value for the current line.
	:rtype: str
	"""

	align = align.lower()
	map = { 'start': 'left', 'end': 'right' }

	alignment = re.findall('(justify)?-?(.+?)$', align)[0]
	if end:
		return 'left' if alignment[1] == 'justify' else map.get(alignment[1], alignment[1])
	else:
		return alignment[0] if alignment[0] else alignment[1]

def align(figure, axis, items, align='left', xpad=0,
		  xlim=None, va='top', *args, **kwargs):
	"""
	Organize the given objects.

	:param figure: The figure that the component occupies.
				   This is used to get the figure renderer.
	:type figure: :class:`matplotlib.figure.Figure`
	:param axis: The axis (or subplot) where the component is plotted.
	:type axis: :class:`matplotlib.axis.Axis`
	:param items: The list of objects to organize.
	:type items: list of objcet
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
	:param xpad: The space between objects.
	:type xpad: float
	:param xlim: The x-limit relative to which to align the objects.
				  If it is not given, the axis' x-limit is used instead.
				  The x-limit is a tuple limiting the start and end.
	:type xlim: tuple
	:param va: The vertical alignment, can be one of `top` or `bottom`.
			   If the vertical alignment is `bottom`, the annotation grows up.
			   If the vertical alignment is `top`, the annotation grows down.
	:type va: str

	:raises: ValueError
	"""

	xlim = axis.get_xlim() if xlim is None else xlim

	"""
	If the text is left-aligned or justify, move the last item to the next line.

	Otherwise, if the text is right-aligned, move the last item to the next line.
	Then align all the objects in the last line to the right.
	"""
	if align == 'left':
		pass
	elif align == 'justify':
		"""
		Calculate the total space between items.

		Use this space to calculate the total projected space after justification.
		The process therefore first calculates the space between items.
		Then, it calculates the empty space to fill the line.
		"""
		space = 0
		for i in range(len(items) - 1):
			space += (get_bb(figure, axis, items[i + 1]).x0 -
					  get_bb(figure, axis, items[i]).x1)

		last = get_bb(figure, axis, items[-1])
		space = space + xlim[1] - last.x1
		space = space / (len(items) - 1)

		wordspacing_px = (axis.transData.transform((space, 0))[0] -
						  axis.transData.transform((0, 0))[0])

		"""
		Re-position the items.
		"""
		offset = xlim[0]
		for item in items:
			bb = get_bb(figure, axis, item)
			item.set_position((offset, bb.y1 if va == 'top' else bb.y0))
			bb = item.get_bbox_patch()
			item.set_bbox(dict(
				facecolor=bb.get_facecolor(), edgecolor=bb.get_edgecolor(),
				pad=wordspacing_px / 2.))
			bb = get_bb(figure, axis, item)
			offset += bb.width + space
	elif align == 'right':
		if len(items):
			"""
			Start moving the items to the back of the line in reverse.
			"""

			offset = 0
			for item in items[::-1]:
				bb = get_bb(figure, axis, item)
				offset += bb.width
				item.set_position((xlim[1] - offset, bb.y1 if va == 'top' else bb.y0))
				offset += xpad
	elif align == 'center':
		if len(items):
			"""
			Calculate the space that is left in the line.
			Then, halve it and move all items by that value.
			"""

			bb = get_bb(figure, axis, items[-1])
			offset = (xlim[1] - bb.x1)/2.

			for item in items:
				bb = get_bb(figure, axis, item)
				item.set_position((bb.x0 + offset, bb.y1 if va == 'top' else bb.y0))
	else:
		raise ValueError("Unsupported alignment %s" % align)
