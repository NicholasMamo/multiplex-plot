**********************
2. Text Visualizations
**********************

.. meta::
   :description: Python text visualizations for information retrieval, text mining and natural language processing (NLP)
   :keywords: Multiplex, Python, visualizations, information retrieval, text mining, natural language processing, nlp

.. automodule:: text
  :members:
  :special-members:

One of Multiplex's biggest additions to matplotlib is the text visualizations.
These visualizations embody Multiplex's principles: Multiplex structures the data, and you style it.

All text visualizations or annotations you see in Multiplex are based on the :class:`~text.annotation.Annotation` class.
This class isn't quite a visualization on its own, but it is the engine that lays out the text for you.

The :class:`~text.annotation.Annotation` class is only concerned with the layout of the visualiation.
That means that you get to keep all the flexibility to style the text.
For example, the below visualization, created using the :class:`~text.TextAnnotation` class, highlights only the named entities:

.. image:: ../examples/exports/2-text-annotation.png
   :class: example inline

.. note::

	Eager to start creating text visualizations?
	`Multiplex's Jupyter Notebook examples <https://github.com/NicholasMamo/multiplex-plot/tree/master/examples>`_ are a quick guide to get you up and running.
	Check out the `text visualizations Jupyter Notebook <https://github.com/NicholasMamo/multiplex-plot/blob/master/examples/2.%20Text.ipynb>`_ to learn how to create the above visualization, or to start creating your own text visualizations.

Annotations
===========

.. automodule:: text.annotation
   :members:
   :special-members:

Text Visualizations
===================

.. automodule:: text.text
   :members:
   :special-members:
