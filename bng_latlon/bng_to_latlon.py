from math import sqrt, pi, sin, cos, tan, atan2
from constants import a, b, e2, n, a_1, e2_1, F0, N0, E0, lat0, lon0, helmert_transform, convert_csv
try:
    from numba import jit
except ImportError:
    def jit(*args, **kwargs):
        """Dummy decorator to use if numba not installed"""
        def decorator(func): return func
        return decorator


@jit(nopython=True)
def bng_to_latlon(E, N):
    """
    Converts british national grid to lat lon
    Accepts The Ordnance Survey National Grid eastings and northings.
    Return latitude and longitude coordinates.
    """
    # Initialise the iterative variables
    lat = lat0
    M = 0

    while N-N0-M >= 0.00001:  # Accurate to 0.01mm
        lat = (N-N0-M)/(a*F0) + lat
        M1 = (1 + n + (5./4)*n**2 + (5./4)*n**3) * (lat-lat0)
        M2 = (3*n + 3*n**2 + (21./8)*n**3) * sin(lat-lat0) * cos(lat+lat0)
        M3 = ((15./8)*n**2 + (15./8)*n**3) * sin(2*(lat-lat0)) * cos(2*(lat+lat0))
        M4 = (35./24)*n**3 * sin(3*(lat-lat0)) * cos(3*(lat+lat0))
        # meridional arc
        M = b * F0 * (M1 - M2 + M3 - M4)

    # transverse radius of curvature
    nu = a*F0/sqrt(1-e2*sin(lat)**2)

    # meridional radius of curvature
    rho = a*F0*(1-e2)*(1-e2*sin(lat)**2)**(-1.5)
    eta2 = nu/rho-1

    sec_lat = 1./cos(lat)
    VII = tan(lat)/(2*rho*nu)
    VIII = tan(lat)/(24*rho*nu**3)*(5+3*tan(lat)**2+eta2-9*tan(lat)**2*eta2)
    IX = tan(lat)/(720*rho*nu**5)*(61+90*tan(lat)**2+45*tan(lat)**4)
    X = sec_lat/nu
    XI = sec_lat/(6*nu**3)*(nu/rho+2*tan(lat)**2)
    XII = sec_lat/(120*nu**5)*(5+28*tan(lat)**2+24*tan(lat)**4)
    XIIA = sec_lat/(5040*nu**7)*(61+662*tan(lat)**2+1320*tan(lat)**4+720*tan(lat)**6)
    dE = E-E0

    # These are on the wrong ellipsoid currently: Airy 1830 (denoted by _1)
    lat_1 = lat - VII*dE**2 + VIII*dE**4. - IX*dE**6.
    lon_1 = lon0 + X*dE - XI*dE**3 + XII*dE**5. - XIIA*dE**7.

    # Want to convert to the GRS80 ellipsoid.
    # First convert to cartesian from spherical polar coordinates
    H = 0  # Third spherical coord.
    x_1 = (nu/F0 + H)*cos(lat_1)*cos(lon_1)
    y_1 = (nu/F0 + H)*cos(lat_1)*sin(lon_1)
    z_1 = ((1-e2)*nu/F0 + H)*sin(lat_1)

    x_2, y_2, z_2 = helmert_transform(x_1, y_1, z_1)

    # Back to spherical polar coordinates from cartesian
    # Need some of the characteristics of the new ellipsoid
    p = sqrt(x_2**2 + y_2**2)

    # Lat is obtained by an iterative procedure:
    lat = atan2(z_2, (p*(1-e2_1)))  # Initial value
    latold = 2*pi
    while abs(lat - latold) > 10**-16:
        lat, latold = latold, lat
        nu_2 = a_1/sqrt(1-e2_1*sin(latold)**2)
        lat = atan2(z_2+e2_1*nu_2*sin(latold), p)

    # Lon and height are then pretty easy
    lon = atan2(y_2, x_2)
    H = p/cos(lat) - nu_2

    # Uncomment this line if you want to print the results
    # print([(lat-lat_1)*180/pi, (lon - lon_1)*180/pi])

    # Convert to degrees
    lat = lat*180/pi
    lon = lon*180/pi

    return round(lat, 6), round(lon, 6)


if __name__ == "__main__":
    assert bng_to_latlon(538890, 177320) == (51.477795, -0.001402)
    assert bng_to_latlon(352500.2, 401400) == (53.50713, -2.71766)
    convert_csv('../csv/BNG.csv', '../csv/BNGandLatLon.csv', bng_to_latlon)
