.. Multiplex documentation master file, created by
   sphinx-quickstart on Thu Dec 19 16:50:01 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. meta::
   :description: Multiplex: visualizations that tell stories
   :keywords: Multiplex, Python, visualizations, data science

.. image:: ../../assets/logo.png
   :class: multiplex-logo
   :width: 400

.. image:: ../../examples/exports/3-time-series.png
   :class: example

Multiplex is a visualization library for Python built on `matplotlib <https://github.com/matplotlib/matplotlib/>`_.
Multiplex is built on the principle that visualizations are about exploring and explaining data in a beautiful way.
For this reason, Multiplex is built with the intent of making it as easy as possible to transform data into visualizations.

.. note::

	This websites documents all of Multiplex's functionality.
	If you want to get started right away, check out the `example notebooks <https://github.com/NicholasMamo/multiplex-plot/tree/master/examples>`_.

Multiplex is aimed at data scientists who want to explore and explain data.
Currently, the library provides text visualizations, useful for Natural Language Processing (NLP) tasks, as well as easy-to-annotate time series.
In the future, it will also provide other visualizations that are used in information retrieval tasks.

Why Multiplex?
==============

If Multiplex is based on matplotlib, why not use matplotlib directly?
Multiplex does not replace matplotlib: anything you can do with Multiplex, you can also do with matplotlib, and vice-versa.
What Multiplex does is make it easier to create visualizations with matplotlib.

For example, the :class:`text.text.TextAnnotation` class lets you create text visualizations by providing just a string.
You can then style that string, such as by specifying alignment options or by highlighting parts of the text.
All of this can be done in a handful of lines:

.. code-block:: python
	:linenos:

	from multiplex import drawable
	plt.style.use(os.path.join(sys.path[0], '..', 'styles', "multiplex.style"))
	viz = drawable.Drawable(plt.figure(figsize=(10, 1)))
	text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit lacus pharetra augue sodales, id porta purus porta. Nam ut euismod risus'
	viz.draw_text_annotation(text, align='justify', fontfamily='serif', fontsize='large', lpad=0.1, rpad=0.1)
	viz.set_title('Text visualization', loc='left')
	viz.set_caption("It doesn't take much to create text visualizations!")
	plt.show()

The first three lines are standard: they import Multiplex and its style, and create the visualization, which uses the :class:`drawable.Drawable` class.
The emphasized lines are all you need to do to draw and style the text, and set the title and caption.
It takes just 7 lines to create a text-only visualization, including styling.

Multiplex abstracts the tedious process of manually programming which elements go where, and lets you create beautiful visualizations with ease.

.. note::

	The rest of this documentation describes all of Multiplex's functionality.
	It is not necessary to go through all of it.
	You can use it as a reference when you need to know what arguments different visualizations accept.
	If you want to start creating visualizations right away, check out the `example notebooks <https://github.com/NicholasMamo/multiplex-plot/tree/master/examples>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   drawable
   text
   timeseries
   utilities

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
