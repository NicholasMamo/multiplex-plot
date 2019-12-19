#!/bin/bash

# Allow relative path calls
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P ) # get the script path
cd "$parent_path" # go to the script path

# Perform the unit tests

python3 -m unittest multiplex.tests.test_drawable
