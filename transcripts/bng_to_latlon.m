// Written by David Gibson http://bangmeansdoit.co.uk
// Convert OSGB36 easting/northing to WSG84 latitude and longitude
– (CLLocation*) latLon_WSG84
{
double E = self.easting;
double N = self.northing;

// E, N are the British national grid coordinates – eastings and northings
double a = 6377563.396, b = 6356256.909; // The Airy 180 semi-major and semi-minor axes used for OSGB36 (m)
double F0 = 0.9996012717; // scale factor on the central meridian
double lat0 = 49*M_PI/180; // Latitude of true origin (radians)
double lon0 = -2*M_PI/180; // Longtitude of true origin and central meridian (radians)
double N0 = -100000, E0 = 400000; // Northing & easting of true origin (m)
double e2 = 1 – (b*b)/(a*a); // eccentricity squared
double n = (a-b)/(a+b);

// Initialise the iterative variables
double lat = lat0, M = 0;

while(N-N0-M >= 0.00001) // Accurate to 0.01mm
{
lat = (N-N0-M)/(a*F0) + lat;
double M1 = (1. + n + (5/4)*pow(n,2) + (5/4)*pow(n, 3)) * (lat-lat0);
double M2 = (3.*n + 3.*pow(n,2) + (21/8)*pow(n,3)) * sin(lat-lat0) * cos(lat+lat0);
double M3 = ((15/8)*pow(n,2) + (15/8)*pow(n,3)) * sin(2*(lat-lat0)) * cos(2*(lat+lat0));
double M4 = (35/24)*pow(n,3) * sin(3*(lat-lat0)) * cos(3*(lat+lat0));

// meridional arc
M = b * F0 * (M1 – M2 + M3 – M4);
}

// transverse radius of curvature
double nu = a*F0/sqrt(1-e2*pow(sin(lat),2));

// meridional radius of curvature
double rho = a*F0*(1-e2)*pow((1-e2*pow(sin(lat),2)),(-1.5));
double eta2 = nu/rho-1.;

double secLat = 1./cos(lat);
double VII = tan(lat)/(2*rho*nu);
double VIII = tan(lat)/(24*rho*pow(nu,3))*(5+3*pow(tan(lat),2)+eta2-9*pow(tan(lat),2)*eta2);
double IX = tan(lat)/(720*rho*pow(nu,5))*(61+90*pow(tan(lat),2)+45*pow(tan(lat),4));
double X = secLat/nu;
double XI = secLat/(6*pow(nu,3))*(nu/rho+2*pow(tan(lat),2));
double XII = secLat/(120*pow(nu,5))*(5+28*pow(tan(lat),2)+24*pow(tan(lat),4));
double XIIA = secLat/(5040*pow(nu,7))*(61+662*pow(tan(lat),2)+1320*pow(tan(lat),4)+720*pow(tan(lat),6));
double dE = E-E0;

// These are on the wrong ellipsoid currently: Airy1830. (Denoted by _1)
double lat_1 = lat – VII*pow(dE,2) + VIII*pow(dE,4) – IX*pow(dE,6);
double lon_1 = lon0 + X*dE – XI*pow(dE,3) + XII*pow(dE,5) – XIIA*pow(dE,7);

// Obj-C log
NSLog(@”Firstbash %f, %f”, lat_1*180/M_PI, lon_1*180/M_PI);

// Want to convert to the GRS80 ellipsoid.
// First convert to cartesian from spherical polar coordinates
double H = 0; // Third spherical coord.
double x_1 = (nu/F0 + H)*cos(lat_1)*cos(lon_1);
double y_1 = (nu/F0+ H)*cos(lat_1)*sin(lon_1);
double z_1 = ((1-e2)*nu/F0 +H)*sin(lat_1);

// Perform Helmut transform (to go between Airy 1830 (_1) and GRS80 (_2))
double s = -20.4894*pow(10,-6); // The scale factor -1
double tx = 446.448, ty = -125.157, tz = 542.060; // The translations along x,y,z axes respectively
double rxs = 0.1502, rys = 0.2470, rzs = 0.8421; // The rotations along x,y,z respectively, in seconds
double rx = rxs*M_PI/(180*3600.), ry = rys*M_PI/(180*3600.), rz = rzs*M_PI/(180*3600.); // In radians
double x_2 = tx + (1+s)*x_1 + (-rz)*y_1 + (ry)*z_1;
double y_2 = ty + (rz)*x_1 + (1+s)*y_1 + (-rx)*z_1;
double z_2 = tz + (-ry)*x_1 + (rx)*y_1 + (1+s)*z_1;

// Back to spherical polar coordinates from cartesian
// Need some of the characteristics of the new ellipsoid
double a_2 =6378137.000, b_2 = 6356752.3141; // The GSR80 semi-major and semi-minor axes used for WGS84(m)
double e2_2 = 1- (b_2*b_2)/(a_2*a_2); // The eccentricity of the GRS80 ellipsoid
double p = sqrt(pow(x_2,2) + pow(y_2,2));

// Lat is obtained by an iterative proceedure:
lat = atan2(z_2,(p*(1-e2_2))); // Initial value
double latold = 2*M_PI;

double nu_2 = 0.;

while(abs(lat – latold)>pow(10,-16))
{
double latTemp = lat;
lat = latold;
latold = latTemp;
nu_2 = a_2/sqrt(1-e2_2*pow(sin(latold),2));
lat = atan2(z_2+e2_2*nu_2*sin(latold), p);
}

// Lon and height are then pretty easy
double lon = atan2(y_2,x_2);
H = p/cos(lat) – nu_2;

// Obj-C log
NSLog(@”%f, %f”, (lat-lat_1)*180/M_PI, (lon – lon_1)*180/M_PI);

// Convert to degrees
lat = lat*180/M_PI;
lon = lon*180/M_PI;

// create Obj-C location object – alternatively, output the ‘lat’ and ‘lon’ variables above
CLLocation* loc = [[CLLocation alloc] initWithLatitude:lat longitude:lon];

return loc;
}