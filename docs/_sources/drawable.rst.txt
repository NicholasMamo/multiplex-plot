******************
1. Getting started
******************

.. meta::
   :description: Multiplex: visualizations that tell stories
   :keywords: Multiplex, Python, visualizations, data science

There is one thing that is more important than anything else in Multiplex: the :class:`~drawable.Drawable` class.
All of Multiplex's visualizations revolve around it.
Indeed, if you are using Multiplex, you can—and should—work only with :class:`~drawable.Drawable` class.

A :class:`~drawable.Drawable` is nothing more than a class that wraps a matplotlib figure and an axis.
All of the functions that you would call on a `matplotlib axis <https://matplotlib.org/api/axes_api.html>`_, you can call on the :class:`~drawable.Drawable`.
If you call any function that belongs to a `matplotlib axis <https://matplotlib.org/api/axes_api.html>`_, then matplotlib handles it as usual.
However, if you call a function that is new to Multiplex, such as a new visualization, then the library handles it.

.. image:: ../examples/exports/3-temperatures.png

To start working with a :class:`~drawable.Drawable`, create it from a normal plot:

.. code-block:: python

	import matplotlib.pyplot as plt
	from multiplex import drawable
	viz = drawable.Drawable(plt.figure(figsize=(10, 5)))

That code block would use matplotlib's default plot.
If you want to plot on a particular axis, or a subplot, you can create it as follows instead:

.. code-block:: python

	import matplotlib.pyplot as plt
	from multiplex import drawable
	figure, axis = plt.subplots(2, 1, figsize=(10, 10))
	viz = drawable.Drawable(figure, axis[0])

To learn more about how Multiplex works, keep reading the documentation.
If all you want is to get your hands dirty, take a look at the `examples <https://github.com/NicholasMamo/multiplex-plot/tree/master/examples>`_ directory.
Happy visualizing!

Drawable
========

.. automodule:: drawable
   :members:
   :special-members:

Visualizations
==============

Multiplex also contains visualization types to help you get started creating new types of visualizations.

.. automodule:: visualization
   :members:
   :special-members:

.. automodule:: labelled
   :members:
   :special-members:

Legend
======

.. automodule:: legend
   :members:
   :special-members:
