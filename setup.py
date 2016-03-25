# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
import upload as app

setup(
    name="bng_latlon",
    version=1.0,
    description='Converts british national grid (OSBG36) to lat lon (WGS84) and vice versa.',
    long_description=open('README.rst').read(),
    license='MIT License',
    platforms=['OS Independent'],
    keywords='GPS, OSGB',
    author='Hannah Fry, fmalina',
    author_email='fmalina@gmail.com',
    url="https://github.com/fmalina/bng_latlon",
    packages=find_packages(),
    include_package_data=True
)
