import os


def kilometer_to_nautical_mile():
    kilometers = int(os.getenv('KM_RADIUS'))
    degreesPerMin = 90 * 60
    oneKilo = degreesPerMin / 10000
    nauticalMile = oneKilo * kilometers
    roundNauticalMile = round(nauticalMile)
    return roundNauticalMile
