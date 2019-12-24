# Multiplex

A Python library that builds on matplotlib, providing new types of visualizations to help you explore your data and explain it better.

## Getting Started

These instructions will get you a copy of the project up and running.
For use-cases of Multiplex, check out the Jupyter Notebook examples in the [examples](examples) directory.
To read more about Multiplex, read the [documentation](https://nicholasmamo.github.io/multiplex-plot/).

### Prerequisites

Multiplex is based on [matplotlib](https://github.com/matplotlib/matplotlib).
You can install matplotlib using `python -m pip install -U matplotlib`.
More details about it are available in [matplotlib's repository](https://github.com/matplotlib/matplotlib).

### Installing

Multiplex is not currently distributed with pip since it is still in early development.
Until then, download or clone the repository and place the library wherever you plan on using it.

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
