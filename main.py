import os
from functools import partial

import pyproj
import requests
from dotenv import load_dotenv, find_dotenv
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import transform

from calculations import kilometer_to_nautical_mile
from camera import video

# disable import for dev
# from camera import photo

load_dotenv(find_dotenv())  # load env

script_dir = os.path.dirname(os.path.realpath(__file__))  # raspberry pi
os.chdir(script_dir)

proj_wgs84 = pyproj.Proj("+proj=longlat +datum=WGS84")


def geodesic_point_buffer(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = "+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0"
    project = partial(pyproj.transform, pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)), proj_wgs84)
    buf = Point(0, 0).buffer(km * 1000)  # distance in meters

    return transform(project, buf).exterior.coords[:]


def check(lons_lats_vect):
    global flight_image, flight_video
    polygon = Polygon(lons_lats_vect)  # create polygon
    url = f"https://adsbexchange-com1.p.rapidapi.com/v2/lat/{os.getenv('LAT')}/lon/{os.getenv('LON')}/dist/{kilometer_to_nautical_mile()}/"
    headers = {
        "X-RapidAPI-Key": os.getenv("X_RAPID_API_KEY"),
        "X-RapidAPI-Host": os.getenv("X_RAPID_API_HOST"),
    }
    response = requests.request("GET", url, headers=headers).json()

    for item in response["ac"]:
        print(item["flight"])
        point = Point(item["lon"], item["lat"])  # create point
        polygon_check = point.within(polygon)  # check if a point is in the polygon
        polygon_lower = str(polygon_check).lower()

        if polygon_check:
            # disable photo/video capture for dev
            flight_image = "false"
            flight_video = "false"
            if os.getenv("OS") == "pi":
                if os.getenv("CAPTURE") == "video":
                    flight_video = "videos/" + str(item["flight"]).lower().strip() + ".mp4"
                    video.record(flight_video)
                else:
                    photo.capture()  # disable import for dev
            else:
                flight_video = "videos/preview.mp4"
                video.record(flight_video)

            try:
                payload = {
                    "in_polygon": polygon_lower,
                    "lat": item["lat"],
                    "lon": item["lon"],
                    "flight": item["flight"],
                    "image": flight_image,
                    "video": flight_video,
                }
                requests.post("https://projects.mitchellbreden.nl/api/flight-data", data=payload)
            except:
                pass
        else:
            print("no flights in area")


# Runs scripts
if __name__ == "__main__":
    buffer = geodesic_point_buffer(os.getenv("LAT"), os.getenv("LON"), int(os.getenv("KM_RADIUS")))
    check(buffer)
