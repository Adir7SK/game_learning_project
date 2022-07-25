"""Special module for pytest, considered as a local plugin: every feature here is also available in all other test folders and sub-folders."""

#import pytest
#import sys
#sys.path.append('src/Field')

""" Here we found a lot about runing tests with pycharm: 
https://www.jetbrains.com/help/pycharm/performing-tests.html#test-mutliprocessing"""
import pytest
import numpy.testing as npt
from src.Field.MazeGenerator import dim, create_maze
