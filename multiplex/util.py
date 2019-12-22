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
