![Multiplex](https://raw.githubusercontent.com/NicholasMamo/multiplex-plot/master/assets/logo.png)

# Multiplex

Multiplex is a Python library that builds on matplotlib, providing new visualizations to help you explore your data and explain it better.

Creating narrative-driven visualizations involves re-imagining matplotlib's plots.
Multiplex follows best-practices to help you create visualizations.
The library adds the capability to add a description to visualizations and moves the legend to the top.

In addition, Multiplex includes:

- A brand new text visualization modul to create text graphics or to annotate data anywhere on the plot,
- A brand new graph visualization,
- New matplotlib styles to make your data stand out.

![Example time series](https://raw.githubusercontent.com/NicholasMamo/multiplex-plot/master/examples/exports/3-temperatures.png)

The instructions in this README.md file will get you a copy of the project up and running.
For use-cases of Multiplex, check out the Jupyter Notebook examples in the [examples](https://github.com/NicholasMamo/multiplex-plot/tree/master/examples) directory.
To read more about Multiplex, read the [documentation](https://nicholasmamo.github.io/multiplex-plot/).

### Prerequisites

Multiplex is based on [matplotlib](https://github.com/matplotlib/matplotlib).
You can install matplotlib using `python -m pip install -U matplotlib`.
More details about it are available in [matplotlib's repository](https://github.com/matplotlib/matplotlib).

### Installing

You can install Multiplex using `python -m pip install -U multiplex-plot`.

## Running the tests

The tests use [unittest](https://docs.python.org/3/library/unittest.html).
Each visualization has its own unit tests.
You can run the tests individually:

```
python3 -m unittest multiplex.tests.test_drawable
```

Or you can run the tests using the `tests.sh` script:

```
chmod +x tests.sh
./tests.sh
```

## Built With

* [matplotlib](https://github.com/matplotlib/matplotlib)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/NicholasMamo/multiplex-plot/tags).

## Authors

* **Nicholas Mamo** - *Library development* - [NicholasMamo](https://github.com/NicholasMamo)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) for this README template
* Cole Nussbaumer Knaflic's [Storytelling with Data](http://www.storytellingwithdata.com/) for the inspiration
