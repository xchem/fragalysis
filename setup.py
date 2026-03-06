import os
from setuptools import setup

setup(
   name='xchem-fragalysis',
   version=os.environ.get('GITHUB_REF_NAME', '0.0.0'),
   description='Python module to interact with Fragalysis',
   author='Diamond Light Source / Informatics Matters',
   author_email='max.winokan@diamond.ac.uk',
   packages=['fragalysis'],  #same as name
   install_requires=['ipywidgets', 'mpytools'], #external packages as dependencies
)
