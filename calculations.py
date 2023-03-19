import os


def kilometerToNauticalMile():
    kilometers = int(os.getenv('KM_RADIUS'))
    degreesPerMin = 90 * 60
    oneKilo = degreesPerMin / 10000
    nauticalMile = oneKilo * kilometers
    roundNauticalMile = round(nauticalMile)
    return roundNauticalMile
