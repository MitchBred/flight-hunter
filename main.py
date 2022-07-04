import requests
import logging
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')


def geodesic_point_buffer(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
        proj_wgs84)
    buf = Point(0, 0).buffer(km * 1000)  # distance in metres

    return transform(project, buf).exterior.coords[:]


def check(lons_lats_vect):
    # test purpose
    # print(lons_lats_vect)
    point = Point(5.9648594, 52.2086425)
    # polygon = Polygon(lons_lats_vect)
    # print(polygon.contains(point))

    polygon = Polygon(lons_lats_vect)  # create polygon

    url = "https://adsbexchange-com1.p.rapidapi.com/v2/lat/52.2086425/lon/5.9648594/dist/3/"
    # url = "https://airlabs.co/api/v9/flights?api_key=46c11282-49fb-43e5-8741-554dd3a768ad";

    headers = {
        "X-RapidAPI-Key": "343a3909c7mshdd02c4b847c51e0p1c1123jsnf35b8149da43",
        "X-RapidAPI-Host": "adsbexchange-com1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    result = response.json()

    for l in result['ac']:
        point = Point(l['lon'], l['lat'])  # create point
        polygonCheck = point.within(polygon)  # check if a point is in the polygon
        print(l)
        if polygonCheck:
            payload = {
                "inPolygon": polygonCheck,
                "lat": l['lat'],
                "lon": l['lon'],
                "flight": l['flight']
            }

            requests.post('http://127.0.0.1:8000/api/flight-data', data=payload)
        else:
            print("No flight data available")


# Runs scripts
if __name__ == '__main__':
    b = geodesic_point_buffer(52.2086425, 5.9648594, 100.0)
    check(b)
