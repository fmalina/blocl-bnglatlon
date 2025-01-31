from math import pi
import csv


F0 = 0.9996012717  # scale factor on the central meridian

# The Airy 1830 ellipsoid semi-major and semi-minor axes used for OSGB36
a, b = 6377563.396, 6356256.909
e2 = 1 - (b*b)/(a*a)  # The eccentricity
n = (a - b) / (a + b)

# The GSR80 semi-major and semi-minor axes used for WGS84
a_1, b_1 = 6378137.000, 6356752.3141
e2_1 = 1 - (b_1 * b_1) / (a_1 * a_1)  # The eccentricity

# Northing & easting of true origin
N0, E0 = -100000, 400000

lat0 = 49 * pi / 180  # Latitude of true origin (radians)
lon0 = -2 * pi / 180  # Longitude of true origin and central meridian (radians)


def helmert_transform(x_1, y_1, z_1, forward=True):
    """
    Perform Helmert transform between Airy 1830 and GRS80.
    forward converts from Airy 1830 to GRS80 or reverses the transformation.
    """
    s = -20.4894 * 10 ** -6  # The scale factor -1
    # The translations along x, y, z axes respectively
    tx, ty, tz = 446.448, -125.157, 542.060
    # The rotations along x, y, z respectively (in seconds)
    rxs, rys, rzs = 0.1502, 0.2470, 0.8421

    if not forward:
        s, tx, ty, tz, rxs, rys, rzs = -s, -tx, -ty, -tz, -rxs, -rys, -rzs

    # Convert seconds to radians
    def sec_to_rad(x): return x * pi / (180 * 3600.)

    rx, ry, rz = [sec_to_rad(x) for x in (rxs, rys, rzs)]

    x_2 = tx + (1 + s) * x_1 + (-rz) * y_1 + (ry) * z_1
    y_2 = ty + (rz) * x_1 + (1 + s) * y_1 + (-rx) * z_1
    z_2 = tz + (-ry) * x_1 + (rx) * y_1 + (1 + s) * z_1

    return x_2, y_2, z_2


def convert_csv(input_file, output_file, conversion_func):
    """Converts coordinates from one system to another using a given conversion function."""
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter=',')
        writer = csv.writer(outfile, delimiter=',')
        next(reader)  # Skip header row

        # input headers ['Lat', 'Lon'] or ['E', 'N']
        writer.writerow(['Lat', 'Lon', 'E', 'N'])  # Write output headers

        for row in reader:
            converted_coords = conversion_func(float(row[0]), float(row[1]))
            writer.writerow([row[0], row[1], *converted_coords])
