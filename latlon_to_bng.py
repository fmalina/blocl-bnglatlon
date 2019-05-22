"""
Converts lat lon (WGS84) to british national grid (OSBG36)
Author: Hannah Fry
http://www.hannahfry.co.uk/blog/2012/02/01/converting-latitude-and-longitude-to-british-national-grid
"""
from math import sqrt, pi, sin, cos, tan, atan2
from numba import jit


@jit(nopython=True)
def WGS84toOSGB36(lat, lon):
    """ Accept latitude and longitude as used in GPS.
    Return OSGB grid coordinates: eastings and northings.

    Usage:
    >>> from latlon_to_bng import WGS84toOSGB36
    >>> WGS84toOSGB36(51.4778, -0.0014)
    (538890.1053365842, 177320.49650700082)
    >>> WGS84toOSGB36(53.50713, -2.71766)
    (352500.19520169357, 401400.01483428996)
    """
    # First convert to radians
    # These are on the wrong ellipsoid currently: GRS80. (Denoted by _1)
    lat_1 = lat*pi/180.0
    lon_1 = lon*pi/180.0

    # Want to convert to the Airy 1830 ellipsoid, which has the following:
    # The GSR80 semi-major and semi-minor axes used for WGS84(m)
    a_1, b_1 = 6378137.000, 6356752.3141
    e2_1 = 1.0 - (b_1*b_1)/(a_1*a_1)  # The eccentricity of the GRS80 ellipsoid
    nu_1 = a_1/sqrt(1.0-e2_1*sin(lat_1)**2.0)

    # First convert to cartesian from spherical polar coordinates
    H = 0.0  # Third spherical coord.
    x_1 = (nu_1 + H)*cos(lat_1)*cos(lon_1)
    y_1 = (nu_1 + H)*cos(lat_1)*sin(lon_1)
    z_1 = ((1.0-e2_1)*nu_1 + H)*sin(lat_1)

    # Perform Helmut transform (to go between GRS80 (_1) and Airy 1830 (_2))
    s = 20.4894*10.0**-6.0  # The scale factor -1
    # The translations along x,y,z axes respectively
    tx, ty, tz = -446.448, 125.157, -542.060
    # The rotations along x,y,z respectively, in seconds
    rxs, rys, rzs = -0.1502, -0.2470, -0.8421
    # In radians
    rx, ry, rz = rxs*pi/(180.0*3600.0), rys*pi/(180.0*3600.0), rzs*pi/(180.0*3600.0)
    x_2 = tx + (1.0+s)*x_1 + (-rz)*y_1 + (ry)*z_1
    y_2 = ty + (rz)*x_1 + (1.0+s)*y_1 + (-rx)*z_1
    z_2 = tz + (-ry)*x_1 + (rx)*y_1 + (1.0+s)*z_1

    # Back to spherical polar coordinates from cartesian
    # Need some of the characteristics of the new ellipsoid
    # The GSR80 semi-major and semi-minor axes used for WGS84(m)
    a, b = 6377563.396, 6356256.909
    e2 = 1.0 - (b*b)/(a*a)  # The eccentricity of the Airy 1830 ellipsoid
    p = sqrt(x_2**2.0 + y_2**2.0)

    # Lat is obtained by an iterative proceedure:
    lat = atan2(z_2, (p*(1.0-e2)))  # Initial value
    latold = 2.0*pi
    while abs(lat - latold) > 10.0**-16.0:
        lat, latold = latold, lat
        nu = a/sqrt(1.0-e2*sin(latold)**2.0)
        lat = atan2(z_2+e2*nu*sin(latold), p)

    # Lon and height are then pretty easy
    lon = atan2(y_2, x_2)
    H = p/cos(lat) - nu

    # E, N are the British national grid coordinates - eastings and northings
    F0 = 0.9996012717  # scale factor on the central meridian
    lat0 = 49.0*pi/180.0  # Latitude of true origin (radians)
    lon0 = -2.0*pi/180.0  # Longtitude of true origin and central meridian (radians)
    N0, E0 = -100000.0, 400000.0  # Northing & easting of true origin (m)
    n = (a-b)/(a+b)

    # meridional radius of curvature
    rho = a*F0*(1.0-e2)*(1.0-e2*sin(lat)**2.0)**(-1.5)
    eta2 = nu*F0/rho-1.0

    M1 = (1.0 + n + (5.0/4.0)*n**2.0 + (5.0/4.0)*n**3.0) * (lat-lat0)
    M2 = (3.0*n + 3.0*n**2.0 + (21.0/8.0)*n**3.0) * sin(lat-lat0) * cos(lat+lat0)
    M3 = ((15.0/8.0)*n**2.0 + (15.0/8.0)*n**3.0) * sin(2.0*(lat-lat0)) * cos(2*(lat+lat0))
    M4 = (35.0/24.0)*n**3.0 * sin(3.0*(lat-lat0)) * cos(3.0*(lat+lat0))

    # meridional arc
    M = b * F0 * (M1 - M2 + M3 - M4)

    I = M + N0
    II = nu*F0*sin(lat)*cos(lat)/2.0
    III = nu*F0*sin(lat)*cos(lat)**3.0*(5.0 - tan(lat)**2.0 + 9.0*eta2)/24.0
    IIIA = nu*F0*sin(lat)*cos(lat)**5.0*(61.0 - 58.0*tan(lat)**2.0 + tan(lat)**4.0)/720.0
    IV = nu*F0*cos(lat)
    V = nu*F0*cos(lat)**3.0*(nu/rho - tan(lat)**2.0)/6.0
    VI = nu*F0*cos(lat)**5.0*(5.0 - 18.0*tan(lat)**2.0 + tan(lat)**4.0 + 14.0*eta2 - 58.0*eta2*tan(lat)**2.0)/120.0

    N = I + II*(lon-lon0)**2.0 + III*(lon-lon0)**4.0 + IIIA*(lon-lon0)**6.0
    E = E0 + IV*(lon-lon0) + V*(lon-lon0)**3.0 + VI*(lon-lon0)**5.0

    # Job's a good'n.
    return E, N


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import csv

    # Read in from a file
    lat_lon = csv.reader(open('LatLon.csv', 'rU'), delimiter=',')
    next(lat_lon)

    # Get the output file ready
    # Issue encountered: https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
    output_file = open('LatLonandBNG.csv', 'w+', newline='')
    output = csv.writer(output_file, delimiter=',')
    output.writerow(['Lat', 'Lon', 'E', 'N'])

    # Loop through the data
    for line in lat_lon:
        lat = line[0]
        lon = line[1]
        E, N = WGS84toOSGB36(float(lat), float(lon))
        output.writerow([str(lat), str(lon), str(E), str(N)])

    # Close the output file
    output_file.close()
