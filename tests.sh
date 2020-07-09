#!/bin/bash

# Allow relative path calls
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P ) # get the script path
cd "$parent_path" # go to the script path

# Perform the unit tests

python3 -m unittest multiplex.text.tests.test_annotation
python3 -m unittest multiplex.bar.tests.test_bar_100
python3 -m unittest multiplex.tests.test_drawable
python3 -m unittest multiplex.tests.test_graph
python3 -m unittest multiplex.tests.test_labelled
python3 -m unittest multiplex.tests.test_legend
python3 -m unittest multiplex.text.tests.test_text
python3 -m unittest multiplex.timeseries.tests.test_time_series
