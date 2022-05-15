import json

import requests
import logging
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')


def geodesic_point_buffer(lon, lat, km):
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lon=lon, lat=lat)),
        proj_wgs84)
    buf = Point(0, 0).buffer(km * 1000)  # distance in metres

    return transform(project, buf).exterior.coords[:]


def check(lons_lats_vect):
    global point
    polygon = Polygon(lons_lats_vect)  # create polygon

    # url = "https://adsbx-flight-sim-traffic.p.rapidapi.com/api/aircraft/json/lat/52.208641/lon/5.96486/dist/25/"
    url = "https://airlabs.co/api/v9/flights?api_key=46c11282-49fb-43e5-8741-554dd3a768ad";
    # headers = {
    #     "X-RapidAPI-Host": "adsbx-flight-sim-traffic.p.rapidapi.com",
    #     "X-RapidAPI-Key": "343a3909c7mshdd02c4b847c51e0p1c1123jsnf35b8149da43"
    # }

    response = requests.request("GET", url)
    r_dict = response.json()

    for each in r_dict['response']:
        point = Point(each['lng'], each['lat'])  # create point

        polygonCheck = point.within(polygon)  # check if a point is in the polygon
        print(polygonCheck)
        print(list(each))
        print(len(r_dict['response']))

    # point = Point(5.2009428, 52.0719623)
    # polygonCheck = point.within(polygon)  # check if a point is in the polygon

        if polygonCheck:
            payload = {
                "test": polygonCheck
            }

            requests.post('http://127.0.0.1:8000/api/flight-data', data=payload)
        else:
            print("No flight data available")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    b = geodesic_point_buffer(5.9648600, 52.2086400, 50)
    check(b)
