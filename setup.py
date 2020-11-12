# -*- encoding: utf-8 -*-
from setuptools import setup

setup(
    name='bng_latlon',
    version='1.0.1',
    description='Converts british national grid (OSBG36) to lat lon (WGS84) and vice versa.',
    long_description=open('README.rst').read(),
    license='MIT License',
    platforms=['OS Independent'],
    keywords='GPS, OSGB',
    author='Hannah Fry, F. Malina',
    author_email='hi@blocl.com',
    url='https://github.com/fmalina/blocl-bnglatlon',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    py_modules=['bng_to_latlon', 'latlon_to_bng'],
)
