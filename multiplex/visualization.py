"""
All visualizations must have, at least, a :class:`~drawable.Drawable`.
They must also implement the :class:`~visualization.Visualization.draw` function.
Any other functionality is up to the visualization type.

The goal of visualizations is not to run away with the data.
Their purpose is to structure the data and apply only the styling that is absolutely required.
They should allow the user to style all aspects of the visualization.

In short, visualization implementations are largely concerned with the structure, not the style.
"""

from abc import ABC, abstractmethod
import util

class Visualization(ABC):
    """
    All visualizations contain at least a :class:`~drawable.Drawable`.
    Furthermore, all classes that inherit the :class:`~visualization.Visualization` class also need to implement functionality to draw a visualization.
    This is implemented in the :func:`~visualization.Visualization.draw` function.

    :ivar drawable: The :class:`~drawable.Drawable` where the visualization will be drawn.
    :vartype drawable: :class:`~drawable.Drawable`
    """

    def __init__(self, drawable, *args, **kwargs):
        """
        Create the visualization with a drawable.

        :param drawable: The :class:`~drawable.Drawable` where the visualization will be drawn.
        :type drawable: :class:`~drawable.Drawable`
        """

        self.drawable = drawable

    @abstractmethod
    def draw(self, *args, **kwargs):
        """
        The draw method is the central method, used to create the visualization on this class' :class:`~drawable.Drawable` instance.
        The purpose of this function is two-fold:

            - Structure the data and apply the bare minimum styling to the visualization, and
            - Allow the user to style the created visualization's components.

        Therefore the drawing function should mainly be concerned with the layout.

        At the end, the function should return the drawn component.
        If the function draws multiple components, it can return them as a tuple.
        """

        pass

    def redraw(self):
        """
        Re-draw the visualization.
        This is mostly used for parts of the visualization that moved around because the axes limits changed, like annotations.
        By default, this function does nothing.
        """

        return

    def _fit_axes(self):
        """
        Make space for the x-axes.
        This function reduces the actual plot size so that the axes tick labels fit neatly.
        It does so by adding space to the left and right of the y-axis if there is need.
        """

        figure, axes, secondary = self.drawable.figure, self.drawable.axes, self.drawable.secondary

        ticks = axes.get_yticklabels() + secondary.get_yticklabels()
        if all( not tick.get_text() for tick in ticks ):
            axes.set_yticklabels(axes.get_yticks())
            secondary.set_yticklabels(secondary.get_yticks())
            ticks = axes.get_yticklabels() + secondary.get_yticklabels()

        # if there are no ticks, do not change the x-limits
        if not ticks:
            return

        # find the leftmost and rightmost axes labels and move the axes until convergence
        _xlim = None
        while _xlim != axes.get_xlim():
            _xlim = axes.get_xlim()
            for spine in [ 'left', 'right' ]:
                # only fit the axes if the type of the spine is data, otherwise it never converges
                type, _ = axes.spines[spine].get_position()
                if type != 'data':
                    continue

                # find the new offset of the axes
                xlim = axes.get_xlim()
                tick_bbs = [ util.get_bb(figure, axes, tick) for tick in ticks ]
                if spine == 'left':
                    offset = min(bb.x0 for bb in tick_bbs)
                    axes.set_xlim((min(offset, xlim[0]), xlim[1]))
                    secondary.set_xlim((min(offset, xlim[0]), xlim[1]))
                else:
                    offset = max(bb.x1 for bb in tick_bbs)
                    axes.set_xlim((xlim[0], max(offset, xlim[1])))
                    secondary.set_xlim((xlim[0], max(offset, xlim[1])))

class DummyVisualization(Visualization):
    """
    The dummy visualization is a simple class used only for testing.
    Its implementation is based on the visualization, but it has an empty :func:`~visualization.Visualization.draw` function.
    """

    def draw(self, *args, **kwargs):
        """
        The dummy visualization draws nothing, and therefore it returns nothing.

        :return: Nothing.
        :rtype: `None`
        """

        return
