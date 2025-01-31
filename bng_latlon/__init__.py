from bng_latlon.bng_to_latlon import bng_to_latlon
from bng_latlon.latlon_to_bng import latlon_to_bng
from bng_latlon.bng_to_latlon import bng_to_latlon as OSGB36toWGS84
from bng_latlon.latlon_to_bng import latlon_to_bng as WGS84toOSGB36

__all__ = [
    'bng_to_latlon',
    'latlon_to_bng',
    'OSGB36toWGS84',
    'WGS84toOSGB36',
]
