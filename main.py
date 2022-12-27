import requests
from camera import camera
from calculations import kilometerToNauticalMile
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import base64
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # load env

script_dir = os.path.dirname(os.path.realpath(__file__))  # raspberry pi
os.chdir(script_dir)

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
    polygon = Polygon(lons_lats_vect)  # create polygon
    url = f"https://adsbexchange-com1.p.rapidapi.com/v2/lat/{os.getenv('LAT')}/lon/{os.getenv('LON')}/dist/{kilometerToNauticalMile()}/"
    headers = {
        "X-RapidAPI-Key": os.getenv('X-RAPID-API-KEY'),
        "X-RapidAPI-Host": os.getenv('X-RAPID-API-HOST'),
    }
    response = requests.request("GET", url, headers=headers).json()

    for list in response['ac']:
        point = Point(list['lon'], list['lat'])  # create point
        polygonCheck = point.within(polygon)  # check if a point is in the polygon
        polygonLower = str(polygonCheck).lower()

        if polygonCheck:
            camera.capture()

            with open("camera/images/flight.jpg", "rb") as img_file:
                data_uri = base64.b64encode(img_file.read())

            try:
                print('flight:', list['flight'])
                payload = {
                    "in_polygon": polygonLower,
                    "lat": list['lat'],
                    "lon": list['lon'],
                    "flight": list['flight'],
                    "image": data_uri
                }
                requests.post('https://huis.mitchellbreden.nl/api/flight-data', data=payload)
            except:
                pass
        else:
            print("No flights in area")


# Runs scripts
if __name__ == '__main__':
    # todo import km from os env
    b = geodesic_point_buffer(os.getenv('LAT'), os.getenv('LON'), 5)
    check(b)
