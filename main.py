import requests
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import base64
from picamera2 import Picamera2

picam2 = Picamera2()
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

    url = "https://adsbexchange-com1.p.rapidapi.com/v2/lat/52.2086425/lon/5.9648594/dist/20/"

    headers = {
        "X-RapidAPI-Key": "343a3909c7mshdd02c4b847c51e0p1c1123jsnf35b8149da43",
        "X-RapidAPI-Host": "adsbexchange-com1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    result = response.json()

    for l in result['ac']:
        point = Point(l['lon'], l['lat'])  # create point
        polygonCheck = point.within(polygon)  # check if a point is in the polygon
        polygonLower = str(polygonCheck).lower()

        if polygonCheck:

            picam2.start_and_capture_file("images/flight.jpg") # capture

            with open("images/small.jpg", "rb") as img_file:
                data_uri = base64.b64encode(img_file.read())

            try:
                print('flight:', l['flight'])
                payload = {
                    "in_polygon": polygonLower,
                    "lat": l['lat'],
                    "lon": l['lon'],
                    "flight": l['flight'],
                    "image": data_uri
                }
                requests.post('https://huis.mitchellbreden.nl/api/flight-data', data=payload)
            except:
                pass
        else:
            print("No flight data available")


# Runs scripts
if __name__ == '__main__':
    b = geodesic_point_buffer(52.2086425, 5.9648594, 150.0)
    check(b)
