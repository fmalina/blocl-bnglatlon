BNG ⇄ LatLon
------------
Converts british national grid (OSBG36) to lat lon (WGS84) and vice versa.

Originally authored by `Hannah Fry`_.

**NEW!** importable, installable, PEP8 styled, pure python and doctested

Included
--------

- `bng_to_latlon.py`_ originally published as `Converting British National Grid to Latitude and Longitude II`_
- `latlon_to_bng.py`_ originally `Converting Latitude and Longitude to British National grid`_

Installation
------------

To get the latest stable release from PyPi

::

    pip install bng_latlon

or a latest version:
::

    pip install -e git+git://github.com/fmalina/bng_latlon.git#egg=bng_latlon


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

To Do
-------

- PYPI listing
- notify devs, share
- common importable constants and separate util functions (Helmut transform...)
- CLI to accept filename or value pair as args


.. _bng_to_latlon.py: bng_to_latlon.py
.. _latlon_to_bng.py: latlon_to_bng.py
.. _`Hannah Fry`: http://www.hannahfry.co.uk/
.. _`Converting British National Grid to Latitude and Longitude II`: http://www.hannahfry.co.uk/blog/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii
.. _`Converting Latitude and Longitude to British National grid`: http://www.hannahfry.co.uk/blog/2012/02/01/converting-latitude-and-longitude-to-british-national-grid
