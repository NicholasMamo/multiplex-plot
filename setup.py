import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multiplex-plot", # Replace with your own username
    version="0.1.2",
    author="Nicholas Mamo",
    author_email="nicholasmamo@gmail.com",
    description="Multiplex: visualizations that tell stories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NicholasMamo/multiplex-plot",
    packages=setuptools.find_packages(),
    classifiers=[
		"Development Status :: 3 - Alpha",
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
		"Topic :: Scientific/Engineering :: Visualization",
		"Intended Audience :: Developers",
		"Intended Audience :: Science/Research",
    ],
    python_requires='>=3',
)
