![Multiplex](https://raw.githubusercontent.com/NicholasMamo/multiplex-plot/master/assets/logo.png)

# Multiplex

Visualizations should tell a story, and tell it in a beautiful way.
Multiplex is a visualization library for Python built on these principles using [matplotlib](https://github.com/matplotlib/matplotlib/).
This library aims to make it as easy as possible for you to transform data into beautiful visualizations that tell a story.

> The instructions in this README.md file will get you a copy of the project up and running.
> For use-cases of Multiplex, check out the [Jupyter Notebook examples](https://github.com/NicholasMamo/multiplex-plot/tree/master/examples).
> To read more about Multiplex, read the [documentation](https://nicholasmamo.github.io/multiplex-plot/).

## Who is Multiplex for?

Multiplex is aimed at data scientists, researchers, students and all those who work with data and are familiar with Python.

## Why should I use Multiplex?

> If Multiplex is based on matplotlib, why not use matplotlib directly?

Multiplex does not replace matplotlib.
Anything that you can do with Multiplex, you can also do with matplotlib.

Multiplex makes it easier to create beautiful visualizations.
This is achieved by providing:

* [4 custom matplotlib styles](https://github.com/NicholasMamo/multiplex-plot/blob/master/examples/0.%20Styles.ipynb);
* Functionality to caption visualizations;
* Functionality to annotate any visualization with text; and
* New types of visualizations not available in matplotlib:
	*  100% bar chart,
	*  Network graph, and
	*  Text-only visualizations.

Multiplex automatically lays out your data so that you can focus on telling your story.

## How do I use Multiplex?

### Prerequisites

Multiplex is based on [matplotlib](https://github.com/matplotlib/matplotlib).
You can install matplotlib using pip: `python -m pip install -U matplotlib`.
More details about it are available in [matplotlib's repository](https://github.com/matplotlib/matplotlib).

Multiplex also uses the following libraries in certain visualizations:

* [networkx](https://github.com/networkx/networkx)
* [pandas](https://github.com/pandas-dev/pandas)

### Installing

You can install Multiplex using pip: `python -m pip install -U multiplex-plot`.

### Quickstart

Creating visualizations with Multiplex is very easy.
For example, you can create a text-only visualization in just 10 lines of code, including all styling options:

```python
import matplotlib.pyplot as plt
from multiplex import drawable
plt.style.use('styles/multiplex.style')
viz = drawable.Drawable(plt.figure(figsize=(10, 2)))
paragraph = """Anthony Lopes is a Portuguese professional footballer who plays for Olympique Lyonnais as a goalkeeper. He came through the youth ranks at Lyon, being called to the first team in 2011 and making his debut the following year."""
style = { 'align': 'justify', 'fontfamily': 'serif', 'alpha': 0.9, 'lineheight': 1.25, 'lpad': 0.1, 'rpad': 0.1 }
viz.draw_text_annotation(paragraph, **style)
viz.set_title('Profile: Anthony Lopes', loc='left')
viz.set_caption("""Wikipedia is a useful repository to get more information about anything. Below is an excerpt from the Wikipedia profile of footballer Anthony Lopes.""")
viz.show()
```

![Example text annotation](https://raw.githubusercontent.com/NicholasMamo/multiplex-plot/master/examples/exports/2-simple-text.png)

All it takes to draw a simple text visualization is 10 lines of code:

1. 3 lines to import matplotlib, Multiplex and the visualization style;
2. 3 lines to set up the visualization object, load the data and set the style;
3. 4 lines to draw and show the visualization, including a title and caption.

Multiplex does all the tedious work for you: the layout, alignment and more.
At the same time, you can take as much control as you want.

Using Multiplex is very easy, but you can get started by checking out the [Jupyter Notebook tutorials](https://github.com/NicholasMamo/multiplex-plot/tree/master/examples) for an easy-to-follow tour of Multiplex's capabilities.

## Example visualizations

![Example bar chart](https://raw.githubusercontent.com/NicholasMamo/multiplex-plot/master/examples/exports/5-natural-gas.png)

![Example time series](https://raw.githubusercontent.com/NicholasMamo/multiplex-plot/master/examples/exports/3-time-series.png)

![Example network graph](https://raw.githubusercontent.com/NicholasMamo/multiplex-plot/master/examples/exports/4-marvel.png)

## Built with

* [matplotlib](https://github.com/matplotlib/matplotlib)
* [networkx](https://github.com/networkx/networkx)
* [pandas](https://github.com/pandas-dev/pandas)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/NicholasMamo/multiplex-plot/tags).

## Authors

* **Nicholas Mamo** - *Library development* - [NicholasMamo](https://github.com/NicholasMamo)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) for this README template
* Cole Nussbaumer Knaflic's [Storytelling with Data](http://www.storytellingwithdata.com/) for the inspiration
