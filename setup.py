from setuptools import setup, find_packages

setup(
    name="home-energy-manager-fronius",
    version="0.9.0",
    description="package for reading Fronius devices",
    url="https://github.com/Hans-4/home-energy-manager-fronius",
    author="Hannes",
    license="MIT",
    packages=find_packages(),
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "requests"
    ]
)