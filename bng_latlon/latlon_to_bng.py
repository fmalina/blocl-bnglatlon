from math import sqrt, pi, sin, cos, tan, atan2
from constants import a, b, e2, n, a_1, e2_1, F0, N0, E0, lat0, lon0, helmert_transform, convert_csv
# numba jit with fallback to dummy decorator if not installed
from bng_to_latlon import jit


@jit(nopython=True)
def latlon_to_bng(lat, lon):
    """
    Converts lat lon (WGS84) to british national grid (OSBG36)
    Accept latitude and longitude as used in GPS.
    Return OSGB grid coordinates: eastings and northings.
    """
    # First convert to radians
    # These are on the wrong ellipsoid currently: GRS80. (Denoted by _1)
    lat_1 = lat*pi/180
    lon_1 = lon*pi/180

    nu_1 = a_1/sqrt(1-e2_1*sin(lat_1)**2)

    # First convert to cartesian from spherical polar coordinates
    H = 0  # Third spherical coord.
    x_1 = (nu_1 + H)*cos(lat_1)*cos(lon_1)
    y_1 = (nu_1 + H)*cos(lat_1)*sin(lon_1)
    z_1 = ((1-e2_1)*nu_1 + H)*sin(lat_1)

    x_2, y_2, z_2 = helmert_transform(x_1, y_1, z_1, forward=False)

    # Back to spherical polar coordinates from cartesian
    # Need some of the characteristics of the new ellipsoid
    p = sqrt(x_2**2 + y_2**2)

    # Lat is obtained by an iterative procedure:
    lat = atan2(z_2, (p*(1-e2)))  # Initial value
    latold = 2*pi
    while abs(lat - latold) > 10**-16:
        lat, latold = latold, lat
        nu = a/sqrt(1-e2*sin(latold)**2)
        lat = atan2(z_2+e2*nu*sin(latold), p)

    # Lon and height are then pretty easy
    lon = atan2(y_2, x_2)
    H = p/cos(lat) - nu

    # meridional radius of curvature
    rho = a*F0*(1-e2)*(1-e2*sin(lat)**2)**(-1.5)
    eta2 = nu*F0/rho-1

    M1 = (1 + n + (5/4)*n**2 + (5/4)*n**3) * (lat-lat0)
    M2 = (3*n + 3*n**2 + (21/8)*n**3) * sin(lat-lat0) * cos(lat+lat0)
    M3 = ((15/8)*n**2 + (15/8)*n**3) * sin(2*(lat-lat0)) * cos(2*(lat+lat0))
    M4 = (35/24)*n**3 * sin(3*(lat-lat0)) * cos(3*(lat+lat0))

    # meridional arc
    M = b * F0 * (M1 - M2 + M3 - M4)

    I = M + N0  # noqa E741, use roman numerals
    II = nu*F0*sin(lat)*cos(lat)/2
    III = nu*F0*sin(lat)*cos(lat)**3*(5 - tan(lat)**2 + 9*eta2)/24
    IIIA = nu*F0*sin(lat)*cos(lat)**5*(61 - 58*tan(lat)**2 + tan(lat)**4)/720
    IV = nu*F0*cos(lat)
    V = nu*F0*cos(lat)**3*(nu/rho - tan(lat)**2)/6
    VI = nu*F0*cos(lat)**5*(5 - 18*tan(lat)**2 + tan(lat)**4 + 14*eta2 - 58*eta2*tan(lat)**2)/120

    # E, N are the British national grid coordinates - eastings and northings
    N = I + II*(lon-lon0)**2 + III*(lon-lon0)**4 + IIIA*(lon-lon0)**6
    E = E0 + IV*(lon-lon0) + V*(lon-lon0)**3 + VI*(lon-lon0)**5

    return round(E, 4), round(N, 4)


if __name__ == "__main__":
    # tests
    assert latlon_to_bng(51.4778, -0.0014) == (538890.1053, 177320.4965)
    assert latlon_to_bng(53.50713, -2.71766) == (352500.1952, 401400.0148)

    convert_csv('../csv/LatLon.csv', '../csv/LatLonandBNG.csv', latlon_to_bng)
