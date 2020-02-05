"""
The :class:`text.annotation.Annotation` class is used to draw text on visualizations.
In and of itself, it is not a visualization type.
To create text-only visualizations, use the :class:`text.text.TextAnnotation` class.
"""

import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
import util

class Annotation():
	"""
	An annotation is a text-only description that is added to visualizations.
	Therefore it is not a visualization in and of itself.
	Text-only visualizations can be created using the :class:`text.text.TextAnnotation` class.
	"""

	pass
