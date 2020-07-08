"""
Unit tests for the :class:`~legend.Legend` class.
"""

from matplotlib import lines
import matplotlib.pyplot as plt
import os
import string
import sys

path = os.path.join(os.path.dirname(__file__), '..')
if path not in sys.path:
	sys.path.insert(1, path)

from .test import MultiplexTest
import drawable
import util

class TestLegend(MultiplexTest):
	"""
	Unit tests for the :class:`~legend.Legend` class.
	"""

	@MultiplexTest.temporary_plot
	def test_draw_duplicates(self):
		"""
		Test that the legend does not re-draw duplicate labels.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		figure, axis = viz.figure, viz.axis
		viz.legend.draw_text_only('label')
		self.assertEqual(1, len(viz.legend.lines))
		self.assertEqual(1, len(viz.legend.lines[0]))

		"""
		Test that even when trying to draw new legends with the same label, they are not drawn.
		"""
		for i in range(0, 10):
			viz.legend.draw_text_only('label')

		self.assertEqual(1, len(viz.legend.lines))
		self.assertEqual(1, len(viz.legend.lines[0]))

	@MultiplexTest.temporary_plot
	def test_draw_duplicates_visual_type(self):
		"""
		Test that the legend does not re-draw duplicate labels even though the types may be different.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		figure, axis = viz.figure, viz.axis
		viz.legend.draw_text_only('label')
		self.assertEqual(1, len(viz.legend.lines))
		self.assertEqual(1, len(viz.legend.lines[0]))

		"""
		Try drawing a line next.
		The legend should reject it.
		"""

		viz.legend.draw_line('label')
		self.assertEqual(1, len(viz.legend.lines))
		self.assertEqual(1, len(viz.legend.lines[0]))

	@MultiplexTest.temporary_plot
	def test_redraw_bottom_xaxis(self):
		"""
		Test that when the x-axis label is at the bottom, the legend's bottom is at y=1.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		figure, axis = viz.figure, viz.axis

		viz.legend.draw_line('label')
		self.assertEqual(1, viz.legend.get_virtual_bb(transform=axis.transAxes).y0)
		line, text = viz.legend.lines[0][0]
		self.assertLessEqual(1, util.get_bb(figure, axis, line, transform=axis.transAxes).y0)
		self.assertEqual(1, text.get_virtual_bb().y0)

	@MultiplexTest.temporary_plot
	def test_redraw_text_only(self):
		"""
		Test that when drawing a legend with text-only annotations, it does not crash.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		figure, axis = viz.figure, viz.axis
		viz.legend.draw_text_only('label')

		"""
		Move the x-axis label and ticks to the top.
		"""
		viz.axis.xaxis.set_label_position('top')
		viz.axis.xaxis.tick_top()
		viz.axis.spines['top'].set_visible(True)
		viz.axis.spines['bottom'].set_visible(False)
		viz.set_xlabel('label')

		self.assertEqual(1, viz.legend.get_virtual_bb(transform=axis.transAxes).y0)
		_, text = viz.legend.lines[0][0]
		self.assertEqual(1, text.get_virtual_bb().y0)

	@MultiplexTest.temporary_plot
	def test_redraw_top_xaxis(self):
		"""
		Test that when the x-axis label is at the top, the legend moves up.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		figure, axis = viz.figure, viz.axis
		viz.legend.draw_text_only('label')
		legend_bb = viz.legend.get_virtual_bb(transform=axis.transAxes)

		"""
		Move the x-axis label and ticks to the top.
		"""
		viz.axis.xaxis.set_label_position('top')
		viz.axis.xaxis.tick_top()
		viz.axis.spines['top'].set_visible(True)
		viz.axis.spines['bottom'].set_visible(False)

		"""
		After adding a label, the legend should move up.
		"""
		viz.set_xlabel('label')
		viz.legend.redraw()
		self.assertLess(legend_bb.y0, viz.legend.get_virtual_bb(transform=axis.transAxes).y0)

	@MultiplexTest.temporary_plot
	def test_redraw_move_all(self):
		"""
		Test that when the x-axis label is at the top, the legend moves the visuals up as well.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		figure, axis = viz.figure, viz.axis
		viz.legend.draw_line('label')
		legend_bb = viz.legend.get_virtual_bb(transform=axis.transAxes)

		"""
		Move the x-axis label and ticks to the top.
		"""
		viz.axis.xaxis.set_label_position('top')
		viz.axis.xaxis.tick_top()
		viz.axis.spines['top'].set_visible(True)
		viz.axis.spines['bottom'].set_visible(False)

		"""
		After adding a label, the legend should move up.
		"""
		viz.set_xlabel('label')
		visual, annotation = viz.legend.lines[0][0]
		before_annotation = annotation.get_virtual_bb(transform=axis.transAxes)
		before_visual = util.get_bb(figure, axis, visual, transform=axis.transAxes)
		viz.legend.redraw()
		after_annotation = annotation.get_virtual_bb(transform=axis.transAxes)
		after_visual = util.get_bb(figure, axis, visual, transform=axis.transAxes)
		self.assertLess(before_annotation.y0, after_annotation.y0)
		self.assertLess(before_visual.y0, after_visual.y0)

	@MultiplexTest.temporary_plot
	def test_redraw_multiple_lines(self):
		"""
		Test that when the x-axis label is at the top, the legend moves all lines up.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 5)))
		figure, axis = viz.figure, viz.axis
		for i in range(0, 20):
			viz.legend.draw_line(f"label { i }")
		legend_bb = viz.legend.get_virtual_bb(transform=axis.transAxes)
		self.assertGreater(len(viz.legend.lines), 1)

		"""
		Move the x-axis label and ticks to the top.
		"""
		viz.axis.xaxis.set_label_position('top')
		viz.axis.xaxis.tick_top()
		viz.axis.spines['top'].set_visible(True)
		viz.axis.spines['bottom'].set_visible(False)

		"""
		After adding a label, the legend should move up.
		"""
		viz.set_xlabel('label')
		before_annotations = [ annotation.get_virtual_bb(transform=axis.transAxes)
								   for line in viz.legend.lines
								   for _, annotation in line ]
		before_visuals = [ util.get_bb(figure, axis, visual, transform=axis.transAxes)
							   for line in viz.legend.lines
							   for visual, _ in line ]
		viz.legend.redraw()
		after_annotations = [ annotation.get_virtual_bb(transform=axis.transAxes)
								   for line in viz.legend.lines
								   for _, annotation in line ]
		after_visuals = [ util.get_bb(figure, axis, visual, transform=axis.transAxes)
								   for line in viz.legend.lines
								   for visual, _ in line ]
		self.assertTrue(all( a1.y0 < a2.y0
							 for a1, a2 in zip(before_annotations, after_annotations) ))
		self.assertTrue(all( v1.y0 < v2.y0
							 for v1, v2 in zip(before_visuals, after_visuals) ))

	@MultiplexTest.temporary_plot
	def test_visual_annotation_do_not_overlap(self):
		"""
		Test that when drawing a legend, the visual and the annotation do not overlap.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line, annotation = viz.legend.draw_line('A')
		linebb = util.get_bb(viz.figure, viz.axis, line)
		self.assertFalse(util.overlapping_bb(linebb, annotation.get_virtual_bb()))

	@MultiplexTest.temporary_plot
	def test_offset_new_legend(self):
		"""
		Test that when getting the offset of an empty legend, the offset returned is 0.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertEqual(0, viz.legend._get_offset())

	@MultiplexTest.temporary_plot
	def test_offset_legend(self):
		"""
		Test that when getting the offset of a legend with one component, the offset returned is beyond that component.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line, annotation = viz.legend.draw_line('A')
		self.assertEqual(annotation.get_virtual_bb().x1, viz.legend._get_offset(pad=0))

	@MultiplexTest.temporary_plot
	def test_offset_pad_new_legend(self):
		"""
		Test that when getting the offset of an empty legend, the offset returned has no padding applied to it.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertEqual(0, viz.legend._get_offset())

	@MultiplexTest.temporary_plot
	def test_offset_pad_legend(self):
		"""
		Test that when getting the offset of a legend with one component, the offset returned has padding applied to it.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line, annotation = viz.legend.draw_line('A')
		self.assertEqual(annotation.get_virtual_bb().x1 + 0.025, viz.legend._get_offset(pad=0.025))

	@MultiplexTest.temporary_plot
	def test_new_line(self):
		"""
		Test that when creating a new line, the legend starts at x-coordinate 0.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		line, annotation = viz.legend.draw_line('A')

		new_line = lines.Line2D([ 0.95, 1], [ 1, 1 ])
		new_annotation = viz.legend.draw_annotation('B', 1, 1)
		viz.legend._newline(new_line, new_annotation, new_annotation.get_virtual_bb().height)
		self.assertEqual(0, new_line.get_xdata()[0])

	@MultiplexTest.temporary_plot
	def test_new_line_overlap(self):
		"""
		Test that when creating a new line, the lines do not overlap.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		for label in string.ascii_uppercase:
			line, annotation = viz.legend.draw_line(label)
		self.assertGreaterEqual(len(viz.legend.lines), 2)

		"""
		Compare the top annotation with the one beneath it.
		"""
		for i in range(len(viz.legend.lines) -1):
			top = viz.legend.lines[i][0][1]
			bottom = viz.legend.lines[i + 1][0][1]
			self.assertLessEqual(round(bottom.get_virtual_bb().y1, 10),
								 round(top.get_virtual_bb().y0, 10))

	@MultiplexTest.temporary_plot
	def test_new_line_top(self):
		"""
		Test that when creating a new line, the last line is at the top of the axis.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		for label in string.ascii_uppercase:
			line, annotation = viz.legend.draw_line(label)
		self.assertGreaterEqual(len(viz.legend.lines), 2)

		bottom = viz.legend.lines[-1][0][-1]
		self.assertEqual(1, round(bottom.get_virtual_bb(transform=viz.axis.transAxes).y0))

	@MultiplexTest.temporary_plot
	def test_new_line_text_only(self):
		"""
		Test that when creating a new line for text-only annotations, the new line does not crash because there is no annotation.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		vocab = string.ascii_uppercase
		labels = [ ''.join(vocab[i:(i+3)])
				   for i in range(len(vocab) - 3) ]
		for label in labels:
			line, annotation = viz.legend.draw_text_only(label)
		self.assertGreaterEqual(len(viz.legend.lines), 2)

		annotations = [ annotation for line in viz.legend.lines
								   for _, annotation in line ]
		for i in range(len(annotations) - 1):
			bb1 = annotations[i].get_virtual_bb()
			bb2 = annotations[i + 1].get_virtual_bb()
			self.assertFalse(util.overlapping_bb(bb1, bb2))

	@MultiplexTest.temporary_plot
	def test_text_only_no_visual(self):
		"""
		Test that when adding text-only annotations, the annotation part is `None`.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		vocab = string.ascii_uppercase
		labels = [ ''.join(vocab[i:(i+3)])
				   for i in range(len(vocab) - 3) ]
		for label in labels:
			line, annotation = viz.legend.draw_text_only(label)

		annotations = [ visual for line in viz.legend.lines
							   for visual, _ in line ]
		self.assertFalse(any(annotations))

	@MultiplexTest.temporary_plot
	def test_text_only_overlap(self):
		"""
		Test that when adding text-only annotations, they do not overlap.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		vocab = string.ascii_uppercase
		labels = [ ''.join(vocab[i:(i+3)])
				   for i in range(len(vocab) - 3) ]
		for label in labels:
			line, annotation = viz.legend.draw_text_only(label)

		annotations = [ annotation for line in viz.legend.lines
								   for _, annotation in line ]
		for i in range(len(annotations) - 1):
			bb1 = annotations[i].get_virtual_bb()
			bb2 = annotations[i + 1].get_virtual_bb()
			self.assertFalse(util.overlapping_bb(bb1, bb2))

	@MultiplexTest.temporary_plot
	def test_new_arrow(self):
		"""
		Test that when creating a new arrow, the legend starts at x-coordinate 0.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		arrow, annotation = viz.legend.draw_arrow('A')
		bb = util.get_bb(viz.figure, viz.axis, arrow)
		self.assertEqual(0, bb.x0)

	@MultiplexTest.temporary_plot
	def test_new_line_arrow_overlap(self):
		"""
		Test that when creating a new line with arrows, the lines do not overlap.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		for label in string.ascii_uppercase:
			arrow, annotation = viz.legend.draw_arrow(label)
		self.assertGreaterEqual(len(viz.legend.lines), 2)

		"""
		Compare the top annotation with the one beneath it.
		"""
		for i in range(len(viz.legend.lines) -1):
			top = viz.legend.lines[i][0][1]
			bottom = viz.legend.lines[i + 1][0][1]
			self.assertLessEqual(round(bottom.get_virtual_bb().y1, 10),
								 round(top.get_virtual_bb().y0, 10))

	@MultiplexTest.temporary_plot
	def test_new_line_arrow_top(self):
		"""
		Test that when creating a new line with arrows, the last line is at the top of the axis.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		for label in string.ascii_uppercase:
			arrow, annotation = viz.legend.draw_arrow(label)
		self.assertGreaterEqual(len(viz.legend.lines), 2)

		bottom = viz.legend.lines[-1][0][-1]
		self.assertEqual(1, round(bottom.get_virtual_bb(transform=viz.axis.transAxes).y0))

	@MultiplexTest.temporary_plot
	def test_new_point(self):
		"""
		Test that when creating a new point, the legend starts at x-coordinate 0.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		point, annotation = viz.legend.draw_point('A')
		bb = util.get_bb(viz.figure, viz.axis, point)
		self.assertEqual(0, round(bb.x0, 2))

	@MultiplexTest.temporary_plot
	def test_new_line_point_overlap(self):
		"""
		Test that when creating a new line with points, the lines do not overlap.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		for label in string.ascii_uppercase:
			point, annotation = viz.legend.draw_point(label)
		self.assertGreaterEqual(len(viz.legend.lines), 2)

		axis = viz.axis
		figure = viz.figure

		"""
		Compare the top annotation with the one beneath it.
		"""
		for i in range(len(viz.legend.lines) -1):
			top = viz.legend.lines[i][0][1]
			bottom = viz.legend.lines[i + 1][0][1]
			self.assertLessEqual(round(bottom.get_virtual_bb().y1, 10),
								 round(top.get_virtual_bb().y0, 10))

			top = viz.legend.lines[i][0][0]
			bottom = viz.legend.lines[i + 1][0][0]
			bb_top = util.get_bb(figure, axis, top)
			bb_bottom = util.get_bb(figure, axis, bottom)
			self.assertLessEqual(round(bb_bottom.y1, 10), round(bb_top.y0, 10))

	@MultiplexTest.temporary_plot
	def test_new_line_point_top(self):
		"""
		Test that when creating a new line with points, the last line is at the top of the axis.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		for label in string.ascii_uppercase:
			point, annotation = viz.legend.draw_point(label)
		self.assertGreaterEqual(len(viz.legend.lines), 2)

		bottom = viz.legend.lines[-1][0][-1]
		self.assertEqual(1, round(bottom.get_virtual_bb(transform=viz.axis.transAxes).y0))

	@MultiplexTest.temporary_plot
	def test_virtual_bb_no_legend(self):
		"""
		Test that when getting the virtual bounding box of an empty legend, a flat one is returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertEqual(0, viz.legend.get_virtual_bb().x0)
		self.assertEqual(1, viz.legend.get_virtual_bb().y0)
		self.assertEqual(1, viz.legend.get_virtual_bb().x1)
		self.assertEqual(1, viz.legend.get_virtual_bb().y1)

	@MultiplexTest.temporary_plot
	def test_virtual_bb_one_legend(self):
		"""
		Test that when getting the virtual bounding box of a legend with one legend, it is equivalent to the virtual bounding box of the annotation.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		for label in string.ascii_uppercase[:10]:
			line, annotation = viz.legend.draw_line(label)
		self.assertEqual(1, len(viz.legend.lines))

		self.assertEqual(0, viz.legend.get_virtual_bb().x0)
		self.assertEqual(1, viz.legend.get_virtual_bb().y0)
		self.assertEqual(1, viz.legend.get_virtual_bb().x1)
		_, annotation = viz.legend.lines[0][0]
		self.assertEqual(annotation.get_virtual_bb().y0, viz.legend.get_virtual_bb().y0)
		self.assertEqual(annotation.get_virtual_bb().y1, viz.legend.get_virtual_bb().y1)

	@MultiplexTest.temporary_plot
	def test_virtual_bb_one_line(self):
		"""
		Test that when getting the virtual bounding box of a legend with one line, it is equivalent to any annotation in the line.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		for label in string.ascii_uppercase[:10]:
			line, annotation = viz.legend.draw_line(label)
		self.assertEqual(1, len(viz.legend.lines))

		self.assertEqual(0, viz.legend.get_virtual_bb().x0)
		self.assertEqual(1, viz.legend.get_virtual_bb().y0)
		self.assertEqual(1, viz.legend.get_virtual_bb().x1)
		for _, annotation in viz.legend.lines[0]:
			self.assertEqual(annotation.get_virtual_bb().y1, viz.legend.get_virtual_bb().y1)

	@MultiplexTest.temporary_plot
	def test_virtual_bb_multiple_lines(self):
		"""
		Test that when getting the virtual bounding box of a legend with multiple lines, it grows from the top of the axis.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		for label in string.ascii_lowercase + string.ascii_uppercase:
			line, annotation = viz.legend.draw_line(label)
		self.assertGreaterEqual(len(viz.legend.lines), 3)

		self.assertEqual(0, viz.legend.get_virtual_bb().x0)
		self.assertEqual(1, viz.legend.get_virtual_bb().y0)
		self.assertEqual(1, viz.legend.get_virtual_bb().x1)
		self.assertEqual(viz.legend.lines[0][0][1].get_virtual_bb().y1, viz.legend.get_virtual_bb().y1)

	@MultiplexTest.temporary_plot
	def test_contains_empty(self):
		"""
		Test that when checking whether an empty legend contains a label, `None` is returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertEqual(None, viz.legend._contains('label'))

	@MultiplexTest.temporary_plot
	def test_contains_contained(self):
		"""
		Test that when a legend contains a label, the tuple is returned.
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertEqual(None, viz.legend._contains('label'))
		visual, annotation = viz.legend.draw_line('label')
		self.assertEqual((visual, annotation), viz.legend._contains('label'))

	@MultiplexTest.temporary_plot
	def test_contains_does_not_contain(self):
		"""
		Test that when a legend does not contain a label, `None` is returned
		"""

		viz = drawable.Drawable(plt.figure(figsize=(10, 10)))
		self.assertEqual(None, viz.legend._contains('label'))
		visual, annotation = viz.legend.draw_line('label')
		self.assertEqual((visual, annotation), viz.legend._contains('label'))
		self.assertEqual(None, viz.legend._contains('another label'))
