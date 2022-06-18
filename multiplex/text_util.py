"""
The text utility functions are generally used only with text.
"""

import util

def draw_token(figure, axes, text, x, y, style, wordspacing, *args, **kwargs):
    """
    Draw the token on the plot.

    Use the ``kwargs`` as a general style, and the ``style`` as a specific style for each word.
    If you specify a ``kwargs`` styling option, but it is missing from the ``style``, the general style is used.

    .. note::

        For example, imagine you specify the token ``color`` to be ``blue`` and the ``fontsize`` to be ``12`` in the ``**kwargs``.
        If in the dictionary's ``style`` of a particular word you set the ``color`` to be ``red``, its color will be ``red``.
        However, since the ``fontsize`` is not specified, it will use the general font size: ``12``.

    :param figure: The figure that the component occupies.
                   This is used to get the figure renderer.
    :type figure: :class:`matplotlib.figure.Figure`
    :param axes: The axes (or subplot) where the component is plotted.
    :type axes: :class:`matplotlib.axes.Axes`
    :param text: The text token to draw.
    :type text: str
    :param x: The x-position of the token.
    :type x: int
    :param y: The y-position of the token.
    :type y: int
    :param style: The style information for the token.
                  This ``dict`` is used to override the styling options in the ``kwargs``.
    :type style: dict
    :param wordspacing: The space between words.
                        This value is used to add padding around words (the whitespace).
    :type wordspacing: float

    :return: The drawn text box.
    :rtype: :class:`matplotlib.text.Text`
    """

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
    Therefore it is transformed from the provided axes coordinates to pixels.
    """
    wordspacing_px = (axes.transData.transform((wordspacing, 0))[0] -
                      axes.transData.transform((0, 0))[0])
    text = axes.text(x, y, text,
                     bbox=dict(pad=wordspacing_px / 2., **bbox_kwargs),
                     *args, **kwargs)
    return text

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

    transform = axes.transData if transform is None else transform

    """
    Draw a dummy token first.
    Some styling options are set specifically for the bbox.
    """
    bbox_kwargs = { 'facecolor': 'None', 'edgecolor': 'None' } # TODO: Create new text utility function
    for arg in bbox_kwargs:
        if arg in kwargs:
            bbox_kwargs[arg] = kwargs.get(arg)
            del kwargs[arg]

    """
    The bbox's padding is calculated in pixels.
    Therefore it is transformed from the provided axes coordinates to pixels.
    """
    wordspacing = wordspacing or 0
    wordspacing_px = (transform.transform((wordspacing, 0))[0] -
                      transform.transform((0, 0))[0])
    token = axes.text(0, 0, 'None', bbox=dict(pad=wordspacing_px / 2., **bbox_kwargs),
                      *args, **kwargs)

    """
    Get the height from the bbox.
    """
    bb = util.get_bb(figure, axes, token, transform)
    height = bb.height
    token.remove()
    return height

def get_wordspacing(figure, axes, transform=None, *args, **kwargs):
    """
    Calculate the word spacing of text tokens.
    The word spacing is given as half a sample character.
    The token is immediately removed so it is not visible on the plot.

    When calculating the word spacing, it is important to provide the style as ``args`` and ``kwargs``.
    In this way, the word spacing considers the font, font size and other attributes that may affect the word spacing.

    :param figure: The figure that the component occupies.
                   This is used to get the figure renderer.
    :type figure: :class:`matplotlib.figure.Figure`
    :param axes: The axes (or subplot) where the component is plotted.
    :type axes: :class:`matplotlib.axes.Axes`
    :param transform: The bounding box transformation.
                      If `None` is given, the data transformation is used.
    :type transform: None or :class:`matplotlib.transforms.TransformNode`

    :return: The word spacing.
    :rtype: float
    """

    transform = axes.transData if transform is None else transform

    """
    Draw a dummy token first.
    Some styling options are set specifically for the bbox.
    """
    bbox_kwargs = { 'facecolor': 'None', 'edgecolor': 'None', 'pad': 0 } # TODO: Create new text utility function
    for arg in bbox_kwargs:
        if arg in kwargs:
            bbox_kwargs[arg] = kwargs.get(arg)
            del kwargs[arg]

    token = axes.text(0, 0, '—', bbox=dict(**bbox_kwargs), *args, **kwargs)

    """
    Get the height from the bbox.
    """
    bb = util.get_bb(figure, axes, token, transform)
    width = bb.width
    token.remove()
    return width / 4.
