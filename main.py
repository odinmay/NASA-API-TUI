from UI.themes import custom_themes
from pprint import pprint
import logging
import pickle
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
                             Markdown,
                             )
from textual.containers import (Container,
                                Vertical,
                                VerticalGroup,
                                VerticalScroll,
                                HorizontalGroup,
                                Center,
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


    def format_manifest_to_markdown(self, manifest_json, rover_name: str) -> Markdown:
        """Create Manifest Table"""
        photo_manifest = manifest_json.get("photo_manifest")

        manifest_dict = {}
        manifest_dict["Name"] = photo_manifest.get("name")
        manifest_dict["Landing Date"] = photo_manifest.get("landing_date")
        manifest_dict["Launch Date"] = photo_manifest.get("launch_date")
        manifest_dict["Status"] = photo_manifest.get("status")
        manifest_dict["Max Sol"] = photo_manifest.get("max_sol")
        manifest_dict["Max Date"] = photo_manifest.get("max_date")
        manifest_dict["Total Photos"] = photo_manifest.get("total_photos")


        curiosity_description = """
        Curiosity is a car-sized Mars rover that is exploring Gale crater and Mount Sharp on Mars as 
        part of NASA's Mars Science Laboratory (MSL) mission. Launched in 2011 and landed the following year,
        the rover continues to operate more than a decade after its original two-year mission.

        Curiosity was launched from Cape Canaveral (CCAFS) on November 26, 2011, at 15:02:00 UTC and 
        landed on Aeolis Palus inside Gale crater on Mars on August 6, 2012, 05:17:57 UTC. 
        The Bradbury Landing site was less than 2.4 km (1.5 mi) from the center of the rover's touchdown
        target after a 560 million km (350 million mi) journey.

        Mission goals include an investigation of the Martian climate and geology, an assessment of
        whether the selected field site inside Gale has ever offered environmental conditions favorable
        for microbial life (including investigation of the role of water), and planetary habitability 
        studies in preparation for human exploration.
        """

        descriptions = {
            "curiosity": curiosity_description,
            "opportunity": "PLACEHOLDER",
            "spirit": "PLACEHOLDER"
            }

        markdown_str = f"""
        ## {manifest_dict["Name"]} Rover Manifest.
        # Launch Date: {manifest_dict["Launch Date"]}
        # Landing Date: {manifest_dict["Landing Date"]}
        # Status" {manifest_dict["Status"]}
        # Max Sol: {manifest_dict["Max Sol"]}
        # Max Date: {manifest_dict["Max Date"]}
        # Total Photos: {manifest_dict["Total Photos"]}
        
        {descriptions[rover_name]}
        
        """
        manifest_markdown = Markdown(markdown_str)

        return manifest_markdown

    def get_rover_markdown(self, rover_name: str):
        rover_json = self.get_rover_manifest_json(rover_name)

        manifest_markdown = self.format_manifest_to_markdown(rover_json)

        return manifest_markdown


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
def get_or_create_fav_themes() -> list:
    """Returns a list of all favorite themes, using a serial object for persistence"""
    if os.path.exists('fav_themes.pkl'):
        with open('fav_themes.pkl', 'rb') as f:
            fav_themes = pickle.load(f)
    else:
        fav_themes = []
        with open('fav_themes.pkl', 'wb') as f:
            pickle.dump(fav_themes, f)

    return fav_themes

def pickle_themes(fav_themes: list):
    """Save the fav theme list to a serial file for persistence"""
    with open('fav_themes.pkl', 'wb') as f:
        pickle.dump(fav_themes, f)


class NasaApp(App):
    CSS_PATH = "select.tcss"
    TITLE = "NASA Rover API"
    SUB_TITLE = "Explore the NASA API!"
    BINDINGS = [('t', 'cycle_theme', 'Cycle Theme'),
                ('f', 'favorite_theme', 'Favorite Theme'),
                ('T', 'cycle_fav_themes', 'Cycle Fav Themes'),
                ]

    selected_rover = reactive("NASA API")
    all_themes = ['gruvbox', 'textual-dark', 'flexoki', 'catppuccin-mocha']
    current_theme_index = 0
    fav_theme_index = 0
    selected_theme = reactive(all_themes[0], init=False, recompose=False)
    selected_theme_str = all_themes[current_theme_index]
    fav_themes = get_or_create_fav_themes()


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
                yield Label("Theme: " + str(self.selected_theme_str), id="selected-theme")

        yield Footer()

    def on_mount(self) -> None:
        # self.screen.styles.background = "black"
        # self.screen.styles.border = ("dashed", "maroon")
        for theme_name, theme in custom_themes.items():
            self.all_themes.append(theme_name)
            self.register_theme(theme)

        self.theme = self.all_themes[0]
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

            manifest_markdown = self.nasa_api.get_rover_markdown(self.selected_rover)

            # self.mount(rover_manifest_table, after="right-side-title")
        elif event.button.label == "Opportunity":
            self.selected_rover = event.button.label
        elif event.button.label == "Spirit":
            self.selected_rover = event.button.label

    def watch_selected_theme(self, old_value, new_value) -> None:
        self.selected_theme = new_value
        self.selected_theme_str = self.all_themes[self.current_theme_index]

        if new_value in self.fav_themes:
            self.query_one("#selected-theme").update("Theme: ★" + self.selected_theme_str)
        else:
            self.query_one("#selected-theme").update("Theme: " + self.selected_theme_str)

    def action_cycle_theme(self):
        """Cycle to the next theme defined in the Class variable Tuple all_themes"""
        if self.current_theme_index + 1 > len(self.all_themes) - 1:
            self.current_theme_index = 0

        else:
            self.current_theme_index += 1

        self.theme = (self.all_themes[self.current_theme_index])
        # Reactive var which is used in ui
        self.selected_theme = self.all_themes[self.current_theme_index]


    def action_cycle_fav_themes(self):
        """Cycle to the next theme defined in the Class variable Tuple all_themes"""
        if len(self.fav_themes) == 0:
            return

        if self.fav_theme_index + 1 > len(self.fav_themes) - 1:
            self.fav_theme_index = 0
        else:
            self.fav_theme_index += 1

        self.theme = (self.fav_themes[self.fav_theme_index])

        # Reactive var which is used in ui
        self.selected_theme = self.fav_themes[self.fav_theme_index]

    def action_favorite_theme(self):
        """Add or remove the theme from the favorite themes list. If it is in the list, remove, otherwise, add"""
        if self.all_themes[self.current_theme_index] in self.fav_themes:
            self.fav_themes.remove(self.all_themes[self.current_theme_index])
            pickle_themes(self.fav_themes)

        else:
            self.fav_themes.append(self.all_themes[self.current_theme_index])

            pickle_themes(self.fav_themes)
            # Reactive var which is used in ui
            self.selected_theme = self.all_themes[self.current_theme_index]

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





