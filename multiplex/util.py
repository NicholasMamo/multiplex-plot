"""
A set of utility functions that are common to all types of visualizations.
"""

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

	return (
		(bb2.x0 < bb1.x0 < bb2.x1 or bb2.x0 < bb1.x1 < bb2.x1) and
		(bb2.y0 < bb1.y0 < bb2.y1 or bb2.y0 < bb1.y1 < bb2.y1) or
		(bb1.x0 < bb2.x0 < bb1.x1 or bb1.x0 < bb2.x1 < bb1.x1) and
		(bb1.y0 < bb2.y0 < bb1.y1 or bb1.y0 < bb2.y1 < bb1.y1)
	)
