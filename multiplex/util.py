"""
These utilities are very general: they are used in almost all visualization types, or re-usable in various scenarios.
"""

from matplotlib.transforms import Bbox
from operator import sub

import re

def get_bb(figure, axes, component, transform=None):
	"""
	Get the bounding box of the given component.

	The bounding box is a rectangular box that covers the component.
	It indicates the bounds of the component and it has many uses.
	For example, it can be used to align components, or to make sure that they do not overlap.

	:param figure: The figure that the component occupies.
				   This is used to get the figure renderer.
	:type figure: :class:`matplotlib.figure.Figure`
	:param axes: The axes (or subplot) where the component is plotted.
	:type axes: :class:`matplotlib.axes.Axes`
	:param component: The component whose bounding box will be fetched.
	:type component: object
	:param transform: The bounding box transformation.
					  If `None` is given, the data transformation is used.
	:type transform: None or :class:`matplotlib.transforms.TransformNode`

	:return: The bounding box of the component.
	:rtype: :class:`matplotlib.transforms.Bbox`
	"""

	transform = axes.transData if transform is None else transform

	renderer = figure.canvas.get_renderer()
	bb = component.get_window_extent(renderer).inverse_transformed(transform)
	return bb

def to_px(axes, bb, transform=None):
	"""
	Convert the given bounding box to pixels based on the given transform.

	:param axes: The axes (or subplot) where the component is plotted.
	:type axes: :class:`matplotlib.axes.Axes`
	:param bb: The bounding box of the component.
	:type bb: :class:`matplotlib.transforms.Bbox`
	:param transform: The bounding box transformation.
					  If `None` is given, the data transformation is used.
	:type transform: None or :class:`matplotlib.transforms.TransformNode`

	:return: A new bounding box with values as pixels.
	:rtype: :class:`matplotlib.transforms.Bbox`
	"""

	transform = transform or axes.transData
	bb = transform.transform(bb)
	return Bbox(bb)

def overlapping(figure, axes, c1, c2, *args, **kwargs):
	"""
	Check whether the given components overlap.
	To check whether the given components overlap, the function extracts their bounding boxes and calls the :func:`~util.overlapping_bb` function.

	If a complex component, such as an :class:`~text.annotation.Annotation`, is given, it cannot extract its bounding box.
	In such cases, where possible extract the bounding box separately, perhaps by getting the virtual bounding box (:func:`~text.annotation.Annotation.get_virtual_bb()`), and call the :func:`~util.overlapping_bb` function directly.

	.. note::

		Since the overlap considers the rectangular bounding box, it is not perfectly precise.

	:param figure: The figure that the component occupies.
				   This is used to get the figure renderer.
	:type figure: :class:`matplotlib.figure.Figure`
	:param axes: The axes (or subplot) where the component is plotted.
	:type axes: :class:`matplotlib.axes.Axes`
	:param c1: The first component.
			   Its bounding box will be compared to the second component.
	:type c1: object
	:param c2: The second component.
			   Its bounding box will be compared to the first component.
	:type c2: object

	:return: A boolean indicating whether the two components overlap.
	:rtype: bool
	"""

	bb1, bb2 = get_bb(figure, axes, c1, *args, **kwargs), get_bb(figure, axes, c2, *args, **kwargs)

	return overlapping_bb(bb1, bb2)

def overlapping_bb(bb1, bb2):
	"""
	Check whether the two given bounding boxes overlap.

	.. note:

		Since the overlap considers the rectangular bounding box, it is not perfectly precise.

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

def get_linespacing(figure, axes, wordspacing=0, transform=None, *args, **kwargs):
	"""
	Calculate the line spacing (or line height) of text tokens.
	The line spacing is calculated by creating a token and getting its height.
	The token is immediately removed so it is not visible on the plot.

	When calculating the line spacing, it is important to provide the style as ``args`` and ``kwargs``.
	In this way, the line spacing considers the font, font size and other attributes that may affect the line spacing.

	:param figure: The figure that the component occupies.
				   This is used to get the figure renderer.
	:type figure: :class:`matplotlib.figure.Figure`
	:param axes: The axes (or subplot) where the component is plotted.
	:type axes: :class:`matplotlib.axes.Axes`
	:param wordspacing: The spacing between tokens.
						This is used to be able to create the padding around words.
	:type wordspacing: float
	:param transform: The bounding box transformation.
					  If `None` is given, the data transformation is used.
	:type transform: None or :class:`matplotlib.transforms.TransformNode`

	:return: The line spacing (or line height).
	:rtype: float
	"""

	"""
	Draw a dummy token first.
	Some styling options are set specifically for the bbox.
	"""
	bbox_kwargs = { 'facecolor': 'None', 'edgecolor': 'None' }
	for arg in bbox_kwargs:
		if arg in kwargs:
			bbox_kwargs[arg] = kwargs.get(arg)
			del kwargs[arg]

	"""
	The bbox's padding is calculated in pixels.
	Therefore it is transformed from the provided axes coordinates to pixels.
	"""
	wordspacing = wordspacing or 0
	wordspacing_px = (axes.transData.transform((wordspacing, 0))[0] -
					  axes.transData.transform((0, 0))[0])
	token = axes.text(0, 0, 'None', bbox=dict(pad=wordspacing_px / 2., **bbox_kwargs),
					  *args, **kwargs)

	"""
	Get the height from the bbox.
	"""
	bb = get_bb(figure, axes, token, transform)
	height = bb.height
	token.remove()
	return height

def get_alignment(align, end=False):
	"""
	Get the proper alignment value for the current line.
	This is mainly used for justification values.

	Justified text justifies all lines except the last one.
	The last line is not full, therefore it is aligned differently: either ``left``, ``center`` or ``right``.
	This function extracts the proper alignment depending on whether this is the last line or not.

	This function supports all the alignment options in the :class:`~util.align` function.
	If a simple alignment, such as ``left`` is given, it returns that value.
	This function only modifies the ``justify`` options.

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

def align(figure, axes, items, align='left', xpad=0,
		  xlim=None, va='top', transform=None, *args, **kwargs):
	"""
	Align the given objects horizontally around the given ``xlim``.

	:param figure: The figure that the component occupies.
				   This is used to get the figure renderer.
	:type figure: :class:`matplotlib.figure.Figure`
	:param axes: The axes (or subplot) where the component is plotted.
	:type axes: :class:`matplotlib.axes.Axes`
	:param items: The list of objects to organize.
	:type items: list of objcet
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
	:param xpad: The space between objects.
				 Normally this depends on the ``wordspacing``.
	:type xpad: float
	:param xlim: The x-limit relative to which to align the objects.
				  If it is not given, the axes' x-limit is used instead.
				  The x-limit is a tuple limiting the start and end.
	:type xlim: tuple
	:param va: The vertical alignment, can be one of `top` or `bottom`.
			   If the vertical alignment is `bottom`, the annotation grows up.
			   If the vertical alignment is `top`, the annotation grows down.
	:type va: str
	:param transform: The bounding box transformation.
					  If `None` is given, the data transformation is used.
	:type transform: None or :class:`matplotlib.transforms.TransformNode`

	:raises: ValueError
	"""

	xlim = axes.get_xlim() if xlim is None else xlim
	transform = transform if transform is not None else axes.transData

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
			space += (get_bb(figure, axes, items[i + 1], transform=transform).x0 -
					  get_bb(figure, axes, items[i], transform=transform).x1)

		last = get_bb(figure, axes, items[-1], transform=transform)
		space = space + xlim[1] - last.x1
		space = space / (len(items) - 1)

		wordspacing_px = (transform.transform((space, 0))[0] -
						  transform.transform((0, 0))[0])

		"""
		Re-position the items.
		"""
		offset = xlim[0]
		for item in items:
			bb = get_bb(figure, axes, item, transform=transform)
			item.set_position((offset, bb.y1 if va == 'top' else bb.y0))
			bb = item.get_bbox_patch()
			item.set_bbox(dict(
				facecolor=bb.get_facecolor(), edgecolor=bb.get_edgecolor(),
				pad=wordspacing_px / 2.))
			bb = get_bb(figure, axes, item, transform=transform)
			offset += bb.width + space
	elif align == 'right':
		if len(items):
			"""
			Start moving the items to the back of the line in reverse.
			"""

			offset = 0
			for item in items[::-1]:
				bb = get_bb(figure, axes, item, transform=transform)
				offset += bb.width
				item.set_position((xlim[1] - offset, bb.y1 if va == 'top' else bb.y0))
				offset += xpad
	elif align == 'center':
		if len(items):
			"""
			Calculate the space that is left in the line.
			Then, halve it and move all items by that value.
			"""

			bb = get_bb(figure, axes, items[-1], transform=transform)
			offset = (xlim[1] - bb.x1)/2.

			for item in items:
				bb = get_bb(figure, axes, item, transform=transform)
				item.set_position((bb.x0 + offset, bb.y1 if va == 'top' else bb.y0))
	else:
		raise ValueError("Unsupported alignment %s" % align)

def get_aspect(axes):
	"""
	Get the aspect ratio of the axes.
	The calculation considers the display ratio as well as the data ratio.

	.. note::

		This solution is based on `Mad Physicist's answer on Stack Overflow <https://stackoverflow.com/a/42014041/1771724>`_.

	:param axes: The axes whose aspect ratio will be calculated.
	:type axes: :class:`matplotlib.axes.Axes`

	:return: The aspect ratio as a fraction of the display ratio and the data ratio.
	:rtype: float
	"""

	"""
	Get the figure and axes dimensions.
	"""
	fig_w, fig_h = axes.get_figure().get_size_inches()
	_, _, axes_w, axes_h = axes.get_position().bounds

	"""
	Calculate the display ratio and the data ratio.
	"""
	display_ratio = (fig_h * axes_h) / (fig_w * axes_w)
	data_ratio = sub(*axes.get_ylim()) / sub(*axes.get_xlim())

	return display_ratio / data_ratio
