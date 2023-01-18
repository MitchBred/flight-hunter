import pywhatkit


def sendImage(image, flightName):
    pywhatkit.sendwhats_image("number", "images/flight.jpg", "Flight: Test")