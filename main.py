import os
import requests
from dotenv import load_dotenv, find_dotenv
from pyproj import CRS, Transformer
from shapely.geometry import Point, Polygon
from shapely.ops import transform
from calculations.nauticalmile import kilometer_to_nautical_mile
from calculations.position_and_speed import distance_in_minutes
# disable import for dev
from camera import video
import weather.api
import status

# Load environment variables
load_dotenv(find_dotenv())

# Set script directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))


def geodesic_point_buffer(lat, lon, km):
    """Generate a geodesic buffer around a point."""
    aeqd_proj = CRS.from_proj4(f"+proj=aeqd +lat_0={lat} +lon_0={lon}")
    tfmr = Transformer.from_proj(aeqd_proj, aeqd_proj.geodetic_crs)
    buffer = Point(0, 0).buffer(km * 1000)  # Convert km to meters
    return transform(tfmr.transform, buffer).exterior.coords[:]


def check(flight_area):
    """Check for flights within the defined polygon."""
    polygon = Polygon(flight_area)
    url = (f"https://adsbexchange-com1.p.rapidapi.com/v2/lat/{os.getenv('LAT')}/"
           f"lon/{os.getenv('LON')}/dist/{kilometer_to_nautical_mile()}/")
    headers = {
        "X-RapidAPI-Key": os.getenv("X_RAPID_API_KEY"),
        "X-RapidAPI-Host": os.getenv("X_RAPID_API_HOST"),
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        error_messages = {
            503: "Server down | RAPID server is unavailable.",
            429: "Server down | Too many requests.",
        }
        print(error_messages.get(response.status_code, "Server error | Invalid request or missing license."))
        return

    flights = response.json().get('ac', [])
    if not flights:
        print(f'Flights | No flights in a {os.getenv("KM_RADIUS")} KM radius.')
        return

    for item in flights:
        if 'flight' not in item or 'ias' not in item:
            print("Incomplete flight data:", item)
            continue

        point = Point(item['lon'], item['lat'])
        if point.within(polygon):
            # flight_video = "videos/preview.mp4"
            flight_video = "videos/" + str(item["flight"]).lower().strip() + ".mp4"
            payload = {
                "flight": item["flight"],
                "category": item['category'],
                "distance_in_minutes": distance_in_minutes(item['lat'], item['lon'], item['ias']),
                "in_polygon": 1,
                "lat": item["lat"],
                "lon": item["lon"],
                "image": "false",
                "video": flight_video
            }
            print(payload)
            requests.post(os.getenv('PROJECT_URL'), data=payload)

        if distance_in_minutes(item['lat'], item['lon'], item['ias']) < int(
                os.getenv("RECORD_VIDEO_LESS_THAN_DISTANCE")):
            print('Recording video')
            video.record(flight_video)


if __name__ == "__main__":
    # clouds = weather.api.clouds()
    # status.run(clouds)
    # if clouds <= int(os.getenv('WEATHER_CLOUD_PERCENTAGE')):
    buffer = geodesic_point_buffer(os.getenv("LAT"), os.getenv("LON"), int(os.getenv("KM_RADIUS")))
    check(buffer)
