import math


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # Distance in kilometers
    return distance


def calculate_time_to_location(current_lat, current_lon, destination_lat, destination_lon, airspeed_knots):
    distance = haversine(current_lat, current_lon, destination_lat, destination_lon)
    time_hours = distance / airspeed_knots
    time_minutes = time_hours * 60
    return time_minutes


def distance_in_minutes(airplane_lat, airplane_lon, airspeed_knots):
    my_location = (float(airplane_lat), float(airplane_lon))  # Example location (New York)
    airplane_position = (airplane_lat, airplane_lon)
    airspeed_knots = airspeed_knots

    time_to_my_location = calculate_time_to_location(airplane_position[0], airplane_position[1], my_location[0],
                                                     my_location[1], airspeed_knots)

    return print(f"The airplane will reach your location in approximately {time_to_my_location:.2f} minutes.")