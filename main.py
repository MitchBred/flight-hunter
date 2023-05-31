import os

import pyproj
import requests
from dotenv import load_dotenv, find_dotenv
from pyproj import CRS, Transformer
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import transform

from calculations import kilometer_to_nautical_mile
# disable import for dev
from camera import video

load_dotenv(find_dotenv())  # load env

script_dir = os.path.dirname(os.path.realpath(__file__))  # raspberry pi
os.chdir(script_dir)

proj_wgs84 = pyproj.Proj("+proj=longlat +datum=WGS84")


def geodesic_point_buffer(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = CRS.from_proj4(
        f"+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0")
    tfmr = Transformer.from_proj(aeqd_proj, aeqd_proj.geodetic_crs)
    buf = Point(0, 0).buffer(km * 1000)  # distance in metres

    return transform(tfmr.transform, buf).exterior.coords[:]


def check(lons_lats_vect):
    global flight_image, flight_video
    polygon = Polygon(lons_lats_vect)  # create polygon
    url = f"https://adsbexchange-com1.p.rapidapi.com/v2/lat/{os.getenv('LAT')}/lon/{os.getenv('LON')}/dist/{kilometer_to_nautical_mile()}/"
    headers = {
        "X-RapidAPI-Key": os.getenv("X_RAPID_API_KEY"),
        "X-RapidAPI-Host": os.getenv("X_RAPID_API_HOST"),
    }
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        flights = response.json()
        if flights['ac'] is not None:
            for item in flights['ac']:
                # if condition to ignore small flights
                if item['category'] is not None or item['category'] != "A0":
                    print(item['flight'])
                    point = Point(item['lon'], item['lat'])  # create point
                    polygon_check = point.within(polygon)  # check if a point is in the polygon
                    polygon_lower = str(polygon_check).lower()

                    if polygon_check:
                        flight_image = "false"
                        flight_video = "videos/" + str(item["flight"]).lower().strip() + ".mp4"

                        try:
                            payload = {
                                "in_polygon": polygon_lower,
                                "lat": item["lat"],
                                "lon": item["lon"],
                                "flight": item["flight"],
                                "image": flight_image,
                                "video": flight_video,
                            }
                            requests.post({os.getenv("PROJECT_URL")}, data=payload)
                        except:
                            pass

                        video.record(flight_video)

                else:
                    print('Flights | no flights in polygon area.', response.status_code)
        else:
            print(f'Flights | no flights in kilometer area of {os.getenv("KM_RADIUS")} KM.', response.status_code)
    elif response.status_code == 503:
        print('Server down | the server is not ready to handle the request.', response.status_code)
    else:
        print('Server down | check request.', response.status_code)


# Runs scripts
if __name__ == "__main__":
    buffer = geodesic_point_buffer(os.getenv("LAT"), os.getenv("LON"), int(os.getenv("KM_RADIUS")))
    check(buffer)
