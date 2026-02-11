from setuptools import setup

setup(
    name="fragalysis",
    version="1.0",
    description="Python module to interact with Fragalysis",
    author="Diamond Light Source / Informatics Matters",
    author_email="max.winokan@diamond.ac.uk",
    packages=["fragalysis"],  # same as name
    install_requires=[
        "ipywidgets",
        "mrich",
        "typer",
    ],  # external packages as dependencies
)
