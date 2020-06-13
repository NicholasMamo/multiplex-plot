![Multiplex](https://raw.githubusercontent.com/NicholasMamo/multiplex-plot/master/assets/logo.png)

# Multiplex

Multiplex is a visualization library for Python built on [matplotlib](https://github.com/matplotlib/matplotlib/).
Multiplex follows the principle that visualizations should tell a story in a beautiful way.
This package is built with the intent of making it as easy as possible to transform data into beautiful visualizations.

> The instructions in this README.md file will get you a copy of the project up and running.
> For use-cases of Multiplex, check out the [Jupyter Notebook examples](https://github.com/NicholasMamo/multiplex-plot/tree/master/examples).
> To read more about Multiplex, read the [documentation](https://nicholasmamo.github.io/multiplex-plot/).

## Who is Multiplex for?

Multiplex is aimed at data scientists, researchers, students and all those who work with data and are familiar with Python.
This library aims to make it easier to explore and explain data by creating beautiful visualizations.

## Why Multiplex?

> If Multiplex is based on matplotlib, why not use matplotlib directly?

Multiplex does not replace matplotlib.
Anything that you can do with Multiplex, you can also do with matplotlib.
What Multiplex does is make it easier to create beautiful visualizations.
This is achieved by providing:

* Custom matplotlib styles;
* Functionality to caption visualizations;
* Functionality to annotate any visualization with text; and
* New types of visualizations not available in matplotlib, such as the network graph and text-based visualizations.

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

### Creating visualizations

Creating visualizations with Multiplex is very easy.
For example, you can create a text visualization with a simple function call, including all styling options:

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
plt.show()
```

![Example text annotation](https://raw.githubusercontent.com/NicholasMamo/multiplex-plot/master/examples/exports/2-simple-text.png)

All it takes to draw a simple text visualization is 10 lines of code:

1. Three lines to import matplotlib, Multiplex and the visualization style;
2. Three lines to set up the visualization object, load the data and set the style;
3. Four lines to draw and show the visualization, including a title and caption.

Multiplex abstracts the tedious process of manually programming which elements go where, and lets you create beautiful visualizations with ease.

For a quick start, check out the [Jupyter Notebook examples](https://github.com/NicholasMamo/multiplex-plot/tree/master/examples) for an easy-to-follow tour of Multiplex's capabilities.

## Example visualizations

![Example time series](https://raw.githubusercontent.com/NicholasMamo/multiplex-plot/master/examples/exports/3-temperatures.png)

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
