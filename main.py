import base64
import os
from functools import partial
# import whatsapp
# import subprocess
import requests
from dotenv import load_dotenv, find_dotenv
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import transform
import pyproj

from calculations import kilometerToNauticalMile

# diable import for dev
from camera import photo
from camera import video

load_dotenv(find_dotenv())  # load env

script_dir = os.path.dirname(os.path.realpath(__file__))  # raspberry pi
os.chdir(script_dir)

proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')


def geodesic_point_buffer(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(pyproj.transform, pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)), proj_wgs84)
    buf = Point(0, 0).buffer(km * 1000)  # distance in metres

    return transform(project, buf).exterior.coords[:]


def check(lons_lats_vect):
    global flightImage, flightVideo
    polygon = Polygon(lons_lats_vect)  # create polygon
    url = f"https://adsbexchange-com1.p.rapidapi.com/v2/lat/{os.getenv('LAT')}/lon/{os.getenv('LON')}/dist/{kilometerToNauticalMile()}/"
    headers = {
        "X-RapidAPI-Key": os.getenv('X_RAPID_API_KEY'),
        "X-RapidAPI-Host": os.getenv('X_RAPID_API_HOST'),
    }
    response = requests.request("GET", url, headers=headers).json()

    for list in response['ac']:
        print(list['flight'])
        point = Point(list['lon'], list['lat'])  # create point
        polygonCheck = point.within(polygon)  # check if a point is in the polygon
        polygonLower = str(polygonCheck).lower()

        if polygonCheck:
            # disable photo/video capture for dev
            flightImage = "false"
            flightVideo = "false"
            if os.getenv('CAPTURE_IMAGE') is None:
                photo.capture()
            else:
                flightVideo = 'videos/'+str(list['flight']).lower().strip() + '.mp4'
                video.record(flightVideo)

            try:
                payload = {
                    "in_polygon": polygonLower,
                    "lat": list['lat'],
                    "lon": list['lon'],
                    "flight": list['flight'],
                    "image": flightImage,
                    "video": flightVideo,
                }
                requests.post('https://projects.mitchellbreden.nl/api/flight-data', data=payload)
            except:
                pass
        else:
            print("no flights in area")


# Runs scripts
if __name__ == '__main__':
    b = geodesic_point_buffer(os.getenv('LAT'), os.getenv('LON'), int(os.getenv('KM')))
    check(b)

    # config first whatsapp
    # subprocess.run(["python", whatsapp.sendImage()])
