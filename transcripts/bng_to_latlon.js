//Written by Chris Dack

function bng_to_latlon(E, N) {

    //E, N are the British national grid coordinates - eastings and northings
    var a = 6377563.396;
    var b = 6356256.909; //The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
    var F0 = 0.9996012717; //scale factor on the central meridian
    var lat0 = 49 * Math.PI / 180; //Latitude of true origin (radians)
    var lon0 = -2 * Math.PI / 180; //Longtitude of true origin and central meridian (radians)
    var N0 = -100000;
    var E0 = 400000; //Northing & easting of true origin (m)
    var e2 = 1 - (b * b) / (a * a); //eccentricity squared
    var n = (a - b) / (a + b);

    //Initialise the iterative variables
    lat = lat0;
    M = 0;

    while (N - N0 - M >= 0.00001) { //Accurate to 0.01mm

        lat = (N - N0 - M) / (a * F0) + lat;
        M1 = (1 + n + (5. / 4) * Math.pow(n, 2) + (5. / 4) * Math.pow(n, 3)) * (lat - lat0);
        M2 = (3 * n + 3 * Math.pow(n, 2) + (21. / 8) * Math.pow(n, 3)) * Math.sin(lat - lat0) * Math.cos(lat + lat0);
        M3 = ((15. / 8) * Math.pow(n, 2) + (15. / 8) * Math.pow(n, 3)) * Math.sin(2 * (lat - lat0)) * Math.cos(2 * (lat + lat0));
        M4 = (35. / 24) * Math.pow(n, 3) * Math.sin(3 * (lat - lat0)) * Math.cos(3 * (lat + lat0));
        //meridional arc
        M = b * F0 * (M1 - M2 + M3 - M4);
    }
    //transverse radius of curvature
    var nu = a * F0 / Math.sqrt(1 - e2 * Math.pow(Math.sin(lat), 2));

    //meridional radius of curvature

    var rho = a * F0 * (1 - e2) * Math.pow((1 - e2 * Math.pow(Math.sin(lat), 2)), (-1.5));
    var eta2 = nu / rho - 1
    var secLat = 1. / Math.cos(lat);
    var VII = Math.tan(lat) / (2 * rho * nu);
    var VIII = Math.tan(lat) / (24 * rho * Math.pow(nu, 3)) * (5 + 3 * Math.pow(Math.tan(lat), 2) + eta2 - 9 * Math.pow(Math.tan(lat), 2) * eta2);
    var IX = Math.tan(lat) / (720 * rho * Math.pow(nu, 5)) * (61 + 90 * Math.pow(Math.tan(lat), 2) + 45 * Math.pow(Math.tan(lat), 4));
    var X = secLat / nu;
    var XI = secLat / (6 * Math.pow(nu, 3)) * (nu / rho + 2 * Math.pow(Math.tan(lat), 2));
    var XII = secLat / (120 * Math.pow(nu, 5)) * (5 + 28 * Math.pow(Math.tan(lat), 2) + 24 * Math.pow(Math.tan(lat), 4));
    var XIIA = secLat / (5040 * Math.pow(nu, 7)) * (61 + 662 * Math.pow(Math.tan(lat), 2) + 1320 * Math.pow(Math.tan(lat), 4) + 720 * Math.pow(Math.tan(lat), 6));
    var dE = E - E0;

    //These are on the wrong ellipsoid currently: Airy1830. (Denoted by _1)
    var lat_1 = lat - VII * Math.pow(dE, 2) + VIII * Math.pow(dE, 4) - IX * Math.pow(dE, 6);
    var lon_1 = lon0 + X * dE - XI * Math.pow(dE, 3) + XII * Math.pow(dE, 5) - XIIA * Math.pow(dE, 7);

    //Want to convert to the GRS80 ellipsoid.
    //First convert to cartesian from spherical polar coordinates
    var H = 0 //Third spherical coord.
    var x_1 = (nu / F0 + H) * Math.cos(lat_1) * Math.cos(lon_1);
    var y_1 = (nu / F0 + H) * Math.cos(lat_1) * Math.sin(lon_1);
    var z_1 = ((1 - e2) * nu / F0 + H) * Math.sin(lat_1);

    //Perform Helmut transform (to go between Airy 1830 (_1) and GRS80 (_2))
    var s = -20.4894 * Math.pow(10, -6); //The scale factor -1
    var tx = 446.448; //The translations along x,y,z axes respectively
    var ty = -125.157;
    var tz = 542.060;
    var rxs = 0.1502;
    var rys = 0.2470;
    var rzs = 0.8421; //The rotations along x,y,z respectively, in seconds
    var rx = rxs * Math.PI / (180 * 3600);
    var ry = rys * Math.PI / (180 * 3600);
    var rz = rzs * Math.PI / (180 * 3600); //In radians
    var x_2 = tx + (1 + s) * x_1 + (-rz) * y_1 + (ry) * z_1;
    var y_2 = ty + (rz) * x_1 + (1 + s) * y_1 + (-rx) * z_1;
    var z_2 = tz + (-ry) * x_1 + (rx) * y_1 + (1 + s) * z_1;

    //Back to spherical polar coordinates from cartesian
    //Need some of the characteristics of the new ellipsoid
    var a_2 = 6378137.000;
    var b_2 = 6356752.3141; //The GSR80 semi-major and semi-minor axes used for WGS84(m)
    var e2_2 = 1 - (b_2 * b_2) / (a_2 * a_2); //The eccentricity of the GRS80 ellipsoid
    var p = Math.sqrt(Math.pow(x_2, 2) + Math.pow(y_2, 2));

    //Lat is obtained by an iterative proceedure:
    var lat = Math.atan2(z_2, (p * (1 - e2_2))); //Initial value
    var latold = 2 * Math.PI;

    while (Math.abs(lat - latold) > Math.pow(10, -16)) {
        //console.log(Math.abs(lat - latold));
        var temp;
        var temp2;
        var nu_2;
        temp1 = lat;
        temp2 = latold;
        latold = temp1;
        lat = temp2;

        lat = latold;
        latold = lat;
        nu_2 = a_2 / Math.sqrt(1 - e2_2 * Math.pow(Math.sin(latold), 2));
        lat = Math.atan2(z_2 + e2_2 * nu_2 * Math.sin(latold), p);
    }
    //Lon and height are then pretty easy
    var lon = Math.atan2(y_2, x_2);
    var H = p / Math.cos(lat) - nu_2;

    //Convert to degrees
    lat = lat * 180 / Math.PI;
    lon = lon * 180 / Math.PI;

    //Job's a good'n.
    return [lat, lon];
}
