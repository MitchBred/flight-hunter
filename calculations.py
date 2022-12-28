import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # load env


def kilometerToNauticalMile():
    kilometers = int(os.getenv('KM'))
    degreesPerMin = 90 * 60
    oneKilo = degreesPerMin / 10000
    nauticalMile = oneKilo * kilometers
    roundNauticalMile = round(nauticalMile)
    return roundNauticalMile
