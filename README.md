<p align="center"><img src="https://raw.githubusercontent.com/fmalina/blocl-bnglatlon/main/gb.png" width="557" height="724"></p>
<p align="center">🇬🇧 <em>BNG ⇄ LatLon</em>🌐</p>
<p align="center"><a href="https://pypi.org/project/bng-latlon/"><img alt="pypi" src="https://img.shields.io/pypi/v/bng-latlon.svg"></a></p>

---

Converts british national grid eastings and northings (OSBG36) to
latitude and longitude (WGS84) and vice versa as used by
<https://blocl.uk>

Originally authored by [Hannah Fry](http://www.hannahfry.co.uk/).

**NEW!** importable, installable, PEP8 styled, pure python, doctested,
with optional numba compiler support for 10x speed

Documentation
=============

Package includes:

-   [bng\_to\_latlon.py](https://github.com/fmalina/bng_latlon/blob/master/bng_latlon/bng_to_latlon.py)
    originally published as \"[Converting British National Grid to
    Latitude and Longitude
    II](https://web.archive.org/web/20170211043005/http://www.hannahfry.co.uk/blog/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii)\"
-   [latlon\_to\_bng.py](https://github.com/fmalina/bng_latlon/blob/master/bng_latlon/latlon_to_bng.py)
    originally \"[Converting Latitude and Longitude to British National
    grid](https://web.archive.org/web/20170212042531/http://www.hannahfry.co.uk/blog/2012/02/01/converting-latitude-and-longitude-to-british-national-grid)\"

The mathematical theory used here is set out in \"[A guide to coordinate
systems in Great
Britain](https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf)\"
by Ordnance Survey.

Installation
============

Get the latest stable release from PyPi:

    pip install bng_latlon

optional but recommend is numba compiler

    pip install numba

Usage
=====

    >>> from bng_latlon import OSGB36toWGS84
    >>> OSGB36toWGS84(538890, 177320)
    (51.477795, -0.001402)
    ...
    >>> from bng_latlon import WGS84toOSGB36
    >>> WGS84toOSGB36(51.4778, -0.0014)
    (538890.1053, 177320.4965)

---

<p align="center"><em>MIT licensed. Designed in the UK, published from Slovakia. <a href="https://blocl.uk/schools/">Blocl Schools</a>.</em></p>
