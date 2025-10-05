from pprint import pprint
import logging
import os

import requests
import pandas as pd
import rich
from textual import on
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import (Header,
                             Select,
                             Label,
                             Button,
                             Static,
                             Placeholder,
                             Footer,
                             DataTable,
                             )
from textual.containers import (Container,
                                Vertical,
                                VerticalGroup,
                                VerticalScroll,
                                HorizontalGroup,
                                Center, Horizontal,
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


class API():
    def __init__(self, api_key):
        self.api_key = api_key

    # @staticmethod
    # def get_rover_photos(rover="curiosity", camera="all", sol=1, earth_date=None):
    #     """Get all photo data from the NASA Rover API"""
    #
    #     nasa_test_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&earth_date={earth_date}&api_key={api_key}"
    #
    #     response = requests.get(nasa_test_url)
    #
    #     print(response.status_code)
    #     pprint(response.json())

    def get_rover_manifest_json(self, rover_name="curiosity"):
        """Return API response with Rover Manifest"""
        manifest_url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover_name}?api_key={self.api_key}"
        response = requests.get(manifest_url)
        return response.json()


    def create_manifest_table(self, manifest_json):
        """Create Manifest Table"""
        photo_manifest = manifest_json.get("photo_manifest")

        name = photo_manifest.get("name")
        landing_date = photo_manifest.get("landing_date")
        launch_date = photo_manifest.get("launch_date")
        status = photo_manifest.get("status")
        max_sol = photo_manifest.get("max_sol")
        max_date = photo_manifest.get("max_date")
        total_photos = photo_manifest.get("total_photos")

        rows = [("Name", "Landing Date", "Launch Date", "Status", "Max Sol", "Max Date", "Total Photos"),
                (name, landing_date, launch_date, status, max_sol, max_date, total_photos)]

        table = DataTable()
        table.add_column(rows[0])
        table.add_rows(rows[1])

        return table

    def get_rover_manifest_data_table(self, rover_name: str):
        rover_json = self.get_rover_manifest_json(rover_name)

        manifest_data_table = self.create_manifest_table(rover_json)

        return manifest_data_table


class Box(Placeholder):
    pass


class TopLeftGroup(VerticalGroup):
    def compose(self):
        with Center():
            self.border_title = "Rover Manifest"

            curiosity_button = Button(label="Curiosity", classes="left-top-button")
            opportunity_button = Button(label="Opportunity", classes="left-top-button")
            spirit_button = Button(label="Spirit", classes="left-top-button")

            yield curiosity_button
            yield opportunity_button
            yield spirit_button

    def on_button_pressed(self, event: Button.Pressed):
        self.border_title = event.button.label


class BottomLeftGroup(VerticalGroup):
    def compose(self):
        with Center():
            self.border_title = "NASA Endpoints"

            yield Button(label="Get Rover Photos", classes="left-bottom-button")
            yield Button(label="Get Martian Weather", classes="left-bottom-button")
            yield Button(label="Get Solar Weather", classes="left-bottom-button")
            yield Button(label="Sun Status", classes="left-bottom-button")
            yield Button(label="NASA Photos", classes="left-bottom-button")
            yield Button(label="NASA Videos", classes="left-bottom-button")
            yield Button(label="Science Data Repository", classes="left-bottom-button")


class RightSideMain(Vertical):
    def compose(self):
        yield Static()


class RightSideTitle(Horizontal):
    def compose(self):
        with Center():
            yield Label("SELECTED ROVER OR OTHER TITLE")

###### Custom Widgets ######
top_left_group = TopLeftGroup(id="top-left-group")
bottom_left_group = BottomLeftGroup(id="bottom-left-group")

right_side_title = RightSideTitle(id="right-side-title")
right_side_main = RightSideMain(id="right-side-main")
############################

###### Main Application ######
class NasaApp(App):
    CSS_PATH = "select.tcss"
    TITLE = "NASA Rover API"
    SUB_TITLE = "Explore the NASA API!"
    selected_rover = reactive("NASA API")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nasa_api = API(api_key)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="☾")

        # Main Screen Area
        #  --HorizontalGroup with 2 Widget, 1:2 ratio layout
        with HorizontalGroup(id="main-content"):
            # Left side of screen
            with VerticalGroup(id="left-side"):
                yield top_left_group

                yield bottom_left_group

            # Right side of screen
            with VerticalGroup(id="right-side"):
                yield right_side_title
                yield right_side_main

        yield Footer()

    def on_mount(self) -> None:
        # self.screen.styles.background = "black"
        # self.screen.styles.border = ("dashed", "maroon")
        self.theme = "flexoki"
        nasa_api = API(api_key)


    def on_key(self, event) -> None:
        if event.key == "q":
            self.exit()

    def on_button_pressed(self, event) -> None:
        print("Button Pressed")
        print(event)
        print(type(event))
        if event.button.label == "Curiosity":
            self.selected_rover = event.button.label
            rover_manifest_table = self.nasa_api.get_rover_manifest_data_table(self.selected_rover)
            self.mount(rover_manifest_table, after="right-side-title")
        elif event.button.label == "Opportunity":
            self.selected_rover = event.button.label
        elif event.button.label == "Spirit":
            self.selected_rover = event.button.label





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

    def get_rover_manifest_json(self, param):
        pass


if __name__ == "__main__":
    app = NasaApp()
    app.run()





