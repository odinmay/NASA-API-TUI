from pprint import pprint
import logging
import os

import requests
import pandas as pd
import rich
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import (Header,
                             Select,
                             Label,
                             TextArea,
                             Button,
                             Welcome,
                             Footer,
                             Static,
                             )
from textual.containers import (Container,
                                VerticalScroll,
                                HorizontalScroll,
                                VerticalGroup,
                                HorizontalGroup,
                                ScrollableContainer,
                                Vertical,
                                Horizontal,
                                )


api_key = os.getenv("API_KEY")

ROVERS = ("curiosity", "opportunity", "spirit")
CAMERAS = ("all", "FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM", "PANCAM", "MINITES")

SELECTABLE_ROVERS = (("Curiosity", "Curiosity"), ("Opportunity", "Opportunity"), ("Spirit", "Spirit"))

SELECTABLE_CAMERAS = (
    ("All", "all"),
    ("Front Hazard Camera", "FHAZ"),
    ("Rear Hazard Camera", "RHAZ"),
    ("Mars Aspect Camera", "MAST"),
    ("Chemcam", "CHEMCAM"),
    ("Mars Hemisphere Laser Camera", "MAHLI"),
    ("Mariner 1 Camera", "MARDI"),
    ("Navcam", "NAVCAM"),
)

class NasaApp(App):
    CSS_PATH = "select.tcss"
    TITLE = "NASA Rover API"
    SUB_TITLE = "Explore the NASA API!"
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="☾")

        with Container(id = "main_content"):
            with Vertical(id="vertical_group"):
                yield Static(content="View Rover Manifest", id="static_content")
                yield Select(choice for choice in SELECTABLE_ROVERS)
            with Horizontal(id="horizontal_group"):
                yield Button(label="Get Manifest")
                yield Button(label="TEST")


        
    def on_mount(self) -> None:
        # self.screen.styles.background = "black"
        self.screen.styles.border = ("dashed", "maroon")

    def on_key(self, event) -> None:
        if event.key == "q":
            self.exit()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)

        # Mount new widget based on selection
        # TODO - Make a loading bar while API call is in progress
        match event.value:
            case "Curiosity":
                self.mount(Label("Curiosity"))
            case "Spirit":
                self.mount(Label("Spirit"))
            case "Opportunity":
                self.mount(Label("Opportunity"))
            case _:
                self.title = "NASA Rover API"




if __name__ == "__main__":
    app = NasaApp()
    app.run()




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


def get_rover_manifest_json(rover_name="curiosity"):
    """Return API response with Rover Manifest"""
    manifest_url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover_name}?api_key={api_key}"
    response = requests.get(manifest_url)
    return response.json()




# manifest_resp = get_rover_manifest_json()
# print(manifest_resp)