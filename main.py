from pprint import pprint
import logging
import os

import requests
import pandas as pd


api_key = os.getenv("API_KEY")






def get_rover_photos(rover="curiosity", camera="all", sol=1, earth_date=None):
    """Get all photo data from the NASA Rover API
    rover options:
        curiosity
        opportunity
        spirit
    camera options and rover that can use them [curiosity, opportunity, spirit] (c,o,s):
        all
        FHAZ(c,o,s)
        RHAZ(c,o,s)
        MAST(c)
        CHEMCAM(c)
        MAHLI(c)
        MARDI(c)
        NAVCAM(c,o,s)
        PANCAM(o,s)
        MINITES(o,s)
    """

    nasa_test_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&earth_date={earth_date}&api_key={api_key}"

    response = requests.get(nasa_test_url)

    print(response.status_code)
    pprint(response.json())


def get_rover_manifest(rover_name="curiosity"):
    """Return API response with Rover Manifest"""
    pass



get_rover_photos(rover="curiosity")
get_rover_manifest()