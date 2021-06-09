BNG ⇄ LatLon
------------
Converts british national grid eastings and northings (OSBG36) to latitude and longitude (WGS84) and vice versa as used by https://blocl.uk

Originally authored by `Hannah Fry`_.

**NEW!** importable, installable, PEP8 styled, pure python, doctested, with optional numba compiler support for 10x speed

Documentation
-------------
Package includes:

- `bng_to_latlon.py`_ originally published as "`Converting British National Grid to Latitude and Longitude II`_"
- `latlon_to_bng.py`_ originally "`Converting Latitude and Longitude to British National grid`_"

The mathematical theory used here is set out in "`A guide to coordinate systems in Great Britain`_" by Ordnance Survey.

Installation
------------

Get the latest stable release from PyPi:

::

    pip install bng_latlon

optional but recommend is numba compiler

::

    pip install numba


Usage
-----

::

    >>> from bng_to_latlon import OSGB36toWGS84
    >>> OSGB36toWGS84(538890, 177320)
    (51.47779538331092, -0.0014016837826672265)
    ...
    >>> from latlon_to_bng import WGS84toOSGB36
    >>> WGS84toOSGB36(51.4778, -0.0014)
    (538890.1053365842, 177320.49650700082)


.. _bng_to_latlon.py: https://github.com/fmalina/bng_latlon/blob/master/bng_to_latlon.py
.. _latlon_to_bng.py: https://github.com/fmalina/bng_latlon/blob/master/latlon_to_bng.py
.. _`Hannah Fry`: http://www.hannahfry.co.uk/
.. _`Converting British National Grid to Latitude and Longitude II`: https://web.archive.org/web/20170211043005/http://www.hannahfry.co.uk/blog/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii
.. _`Converting Latitude and Longitude to British National grid`: https://web.archive.org/web/20170212042531/http://www.hannahfry.co.uk/blog/2012/02/01/converting-latitude-and-longitude-to-british-national-grid
.. _`A guide to coordinate systems in Great Britain`: https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf
