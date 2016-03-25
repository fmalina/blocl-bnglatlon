using System;

namespace Whatever.Namespace.You.Want {
 //adapted from the python script by Andy Nichols
 //where variables have non-descriptive names it's because I couldn't see what they represent
 public static class GeoCoordinatesConverter {
  private
  const double Airy180SemiMajorAxis = 6377563.396;
  private
  const double Airy180SemiMinorAxis = 6356256.909;
  private
  const double ScaleFactorOnCentralMeridian = 0.9996012717;
  private
  const int NorthingOfTrueOrigin = -100000;
  private
  const int EastingOfTrueOrigin = 400000;
  private
  const double LatitudeOfTrueOrigin = 49 * Math.PI / 180;
  private
  const double LongtitudeOfTrueOrigin = -2 * Math.PI / 180;
  private
  const double N = (Airy180SemiMajorAxis - Airy180SemiMinorAxis) / (Airy180SemiMajorAxis + Airy180SemiMinorAxis);
  private
  const double Grs80SemiMajorAxis = 6378137.000;
  private
  const double Grs80SemiMinorAxis = 6356752.3141;
  private
  const double ScaleFactor = -0.0000204894;
  private
  const double XRadians = 0.1502 * Math.PI / 648000;
  private
  const double YRadians = 0.2470 * Math.PI / 648000;
  private
  const double ZRadians = 0.8421 * Math.PI / 648000;

  public static WGS84 Convert(OSGB36 coordinates) {
   var latitude = InitializeLatitude(coordinates);
   var grs80 = CalculateGrs80(coordinates, latitude);
   latitude = RecalculateLatitude(grs80);

   return new WGS84 {
    Latitude = latitude * 180 / Math.PI,
     Longtitude = Math.Atan2(grs80.Y, grs80.X) * 180 / Math.PI
   };
  }

  private static double InitializeLatitude(OSGB36 coordinates) {
   var latitude = LatitudeOfTrueOrigin;
   var meridionalArc = 0.0;
   while (coordinates.Northing - NorthingOfTrueOrigin - meridionalArc >= 0.00001) {
    latitude += (coordinates.Northing - NorthingOfTrueOrigin - meridionalArc) /
     (Airy180SemiMajorAxis * ScaleFactorOnCentralMeridian);
    var meridionalArc1 = (1.0 + N + (1.25 * Math.Pow(N, 2)) + (1.25 * Math.Pow(N, 3))) *
     (latitude - LatitudeOfTrueOrigin);
    var meridionalArc2 = ((3 * N) + (3 * Math.Pow(N, 2)) + ((21.0 / 8) * Math.Pow(N, 3))) *
     Math.Sin(latitude - LatitudeOfTrueOrigin) *
     Math.Cos(latitude + LatitudeOfTrueOrigin);
    var meridionalArc3 = ((15.0 / 8) * Math.Pow(N, 2) + (15.0 / 8) * Math.Pow(N, 3)) *
     Math.Sin(2 * (latitude - LatitudeOfTrueOrigin)) *
     Math.Cos(2 * (latitude + LatitudeOfTrueOrigin));
    var meridionalArc4 = (35.0 / 24) * Math.Pow(N, 3) * Math.Sin(3 * (latitude - LatitudeOfTrueOrigin)) *
     Math.Cos(3 * (latitude + LatitudeOfTrueOrigin));
    meridionalArc = Airy180SemiMinorAxis * ScaleFactorOnCentralMeridian *
     (meridionalArc1 - meridionalArc2 + meridionalArc3 - meridionalArc4);
   }
   return latitude;
  }

  private static Cartesian CalculateGrs80(OSGB36 coordinates, double latitude) {
   var eccentricitySquared = 1 - (Math.Pow(Airy180SemiMinorAxis, 2) / Math.Pow(Airy180SemiMajorAxis, 2));
   var transverseRadiusOfCurvature = Airy180SemiMajorAxis * ScaleFactorOnCentralMeridian /
    Math.Sqrt(1 - (eccentricitySquared * latitude.SinToPower(2)));

   var airy1830 = CalculateAiry1830(coordinates, latitude, transverseRadiusOfCurvature, eccentricitySquared);
   var cartesian = new Cartesian {
    X = (transverseRadiusOfCurvature / ScaleFactorOnCentralMeridian) * Math.Cos(airy1830.Latitude) * Math.Cos(airy1830.Longtitude),
     Y = (transverseRadiusOfCurvature / ScaleFactorOnCentralMeridian) * Math.Cos(airy1830.Latitude) * Math.Sin(airy1830.Longtitude),
     Z = ((1 - eccentricitySquared) * transverseRadiusOfCurvature / ScaleFactorOnCentralMeridian) * Math.Sin(airy1830.Latitude)
   };
   var grs80 = new Cartesian {
    X = 446.448 + (1 + ScaleFactor) * cartesian.X - ZRadians * cartesian.Y + YRadians * cartesian.Z,
     Y = -125.157 + ZRadians * cartesian.X + (1 + ScaleFactor) * cartesian.Y - XRadians * cartesian.Z,
     Z = 542.060 - YRadians * cartesian.X + XRadians * cartesian.Y + (1 + ScaleFactor) * cartesian.Z
   };
   return grs80;
  }

  private static LatitudeLongtitude CalculateAiry1830(OSGB36 coordinates, double latitude,
   double transverseRadiusOfCurvature, double eccentricitySquared) {
   var meridionalRadiusOfCurvature = Airy180SemiMajorAxis * ScaleFactorOnCentralMeridian * (1 - eccentricitySquared) * Math.Pow((1 - (eccentricitySquared * latitude.SinToPower(2))), -1.5);
   var eta2 = (transverseRadiusOfCurvature / meridionalRadiusOfCurvature) - 1;
   var secLat = 1.0 / Math.Cos(latitude);
   var vii = Math.Tan(latitude) / (2 * meridionalRadiusOfCurvature * transverseRadiusOfCurvature);
   var viii = Math.Tan(latitude) / (24 * meridionalRadiusOfCurvature * Math.Pow(transverseRadiusOfCurvature, 3)) *
    (5 + 3 * latitude.TanToPower(2) + eta2 - 9 * latitude.TanToPower(2) * eta2);
   var ix = Math.Tan(latitude) / (720 * meridionalRadiusOfCurvature * Math.Pow(transverseRadiusOfCurvature, 5)) *
    (61 + 90 * latitude.TanToPower(2) + 45 * latitude.TanToPower(4));
   var x = secLat / transverseRadiusOfCurvature;
   var xi = secLat / (6 * Math.Pow(transverseRadiusOfCurvature, 3)) *
    (transverseRadiusOfCurvature / meridionalRadiusOfCurvature + 2 * latitude.TanToPower(2));
   var xii = secLat / (120 * Math.Pow(transverseRadiusOfCurvature, 5)) *
    (5 + 28 * latitude.TanToPower(2) + 24 * latitude.TanToPower(4));
   var xiia = secLat / (5040 * Math.Pow(transverseRadiusOfCurvature, 7)) *
    (61 + 662 * latitude.TanToPower(2) + 1320 * latitude.TanToPower(4) + 720 * latitude.TanToPower(6));

   var eastingDifference = coordinates.Easting - EastingOfTrueOrigin;
   return new LatitudeLongtitude {
    Latitude = latitude - vii * Math.Pow(eastingDifference, 2) + viii * Math.Pow(eastingDifference, 4) -
     ix * Math.Pow(eastingDifference, 6),
     Longtitude = LongtitudeOfTrueOrigin + x * eastingDifference - xi * Math.Pow(eastingDifference, 3) +
     xii * Math.Pow(eastingDifference, 5) - xiia * Math.Pow(eastingDifference, 7)
   };
  }

  private static double RecalculateLatitude(Cartesian grs80) {
   var eccentricityOfGrs80Ellipsoid = 1 - Math.Pow(Grs80SemiMinorAxis, 2) / Math.Pow(Grs80SemiMajorAxis, 2);
   var sphericalPolar = Math.Sqrt(Math.Pow(grs80.X, 2) + Math.Pow(grs80.Y, 2));

   var latitude = Math.Atan2(grs80.Z, (sphericalPolar * (1 - eccentricityOfGrs80Ellipsoid)));
   var latitudeOld = 2 * Math.PI;
   while (Math.Abs(latitude - latitudeOld) > 0.0000000000000001) {
    latitudeOld = latitude;
    var transverseRadiusOfCurvature2 = Grs80SemiMajorAxis /
     Math.Sqrt(1 - eccentricityOfGrs80Ellipsoid * latitudeOld.SinToPower(2));
    latitude = Math.Atan2(grs80.Z + eccentricityOfGrs80Ellipsoid * transverseRadiusOfCurvature2 * Math.Sin(latitudeOld),
     sphericalPolar);
   }
   return latitude;
  }

  private static double SinToPower(this double number, double power) {
   return Math.Pow(Math.Sin(number), power);
  }

  private static double TanToPower(this double number, double power) {
   return Math.Pow(Math.Tan(number), power);
  }

  private class LatitudeLongtitude {
   public double Longtitude {
    get;
    set;
   }
   public double Latitude {
    get;
    set;
   }
  }

  private class Cartesian {
   public double X {
    get;
    set;
   }
   public double Y {
    get;
    set;
   }
   public double Z {
    get;
    set;
   }
  }

  public class WGS84 {
   public double Longtitude {
    get;
    set;
   }
   public double Latitude {
    get;
    set;
   }
  }

  public class OSGB36 {
   public double Easting {
    get;
    set;
   }
   public double Northing {
    get;
    set;
   }
  }
 }
}
