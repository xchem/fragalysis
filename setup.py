import os
from setuptools import setup, find_packages

setup(
   name='xchem-fragalysis',
   version=os.environ.get('GITHUB_REF_NAME', '0.0.0'),
   description='Python module to interact with Fragalysis',
   author='Diamond Light Source / Informatics Matters',
   author_email='max.winokan@diamond.ac.uk',
   packages=find_packages(),
   install_requires=['ipywidgets', 'pandas', 'mpytools'], #external packages as dependencies
)
