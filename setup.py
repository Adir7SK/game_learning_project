"""This file configures how to build and install the python code into an executable package."""

from setuptools import setup, find_packages

setup(
    name='Armor Maze Game',
    version='0.1.0',
    description='Solve maze and defeate enemies to finish a level.',
    packages=find_packages('src')                                   # Denotes that the source code is kept in the src folder
    package_dir={'':'src'},                                         # Denotes that the source code is kept in the src folder
    entry_points={
        'console_scripts': ['AMG=AMG.cli:main'],        # Specifies the main file from the upper directory
    },

    # metadata
    author='Adir Saly-Kaufmann'
    author_email='adir7saly@gmail.com'
    license='proprietary',
    install_requires=['pytest']                                     # We have a dependency on pytest
)
