#!/bin/bash

# allow relative path calls
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P ) # get the script path
cd "$parent_path" # go to the script path

# set the colors
DEFAULT='\033[0;39m'
HIGHLIGHT='\033[0;36m'
ERROR='\033[0;31m'

# Perform the unit tests

echo -e "${HIGHLIGHT}Drawable${DEFAULT}"
echo -e "${HIGHLIGHT}========${DEFAULT}"
python3 -m unittest multiplex.tests.test_drawable
python3 -m unittest multiplex.tests.test_legend

echo -e "${HIGHLIGHT}Base classes${DEFAULT}"
echo -e "${HIGHLIGHT}============${DEFAULT}"
python3 -m unittest multiplex.tests.test_visualization
python3 -m unittest multiplex.tests.test_labelled

echo -e "${HIGHLIGHT}Text${DEFAULT}"
echo -e "${HIGHLIGHT}====${DEFAULT}"
python3 -m unittest multiplex.text.tests.test_annotation
python3 -m unittest multiplex.text.tests.test_text

echo -e "${HIGHLIGHT}Visualizations${DEFAULT}"
echo -e "${HIGHLIGHT}==============${DEFAULT}"
python3 -m unittest multiplex.bar.tests.test_bar_100
python3 -m unittest multiplex.graph.tests.test_graph
python3 -m unittest multiplex.population.tests.test_population
python3 -m unittest multiplex.slope.tests.test_slope
python3 -m unittest multiplex.timeseries.tests.test_time_series

echo -e "${HIGHLIGHT}Utility${DEFAULT}"
echo -e "${HIGHLIGHT}=======${DEFAULT}"
python3 -m unittest multiplex.tests.test_text_util
python3 -m unittest multiplex.tests.test_util
