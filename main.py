from UI.themes import custom_themes
from UI.home_screen import TopLeftGroup, BottomLeftGroup, RightSideTitle, RightSideMain
from UI.api import API
import pickle
import os

from textual import on
from textual.app import App, ComposeResult
from textual.reactive import reactive

from textual.widgets import (Header,
                             Select,
                             Label,
                             Footer,
                             )
from textual.containers import (
                                VerticalGroup,
                                HorizontalGroup,
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

###### Main Application ######
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
                yield TopLeftGroup(id="top-left-group")

                yield BottomLeftGroup(id="bottom-left-group")

            # Right side of screen
            with VerticalGroup(id="right-side"):
                yield RightSideTitle(id="right-side-title")
                yield RightSideMain(id="right-side-main")
                yield Label("Theme: " + str(self.selected_theme_str), id="selected-theme")

        yield Footer()

    def on_mount(self) -> None:
        # Load themes
        for theme_name, theme in custom_themes.items():
            self.all_themes.append(theme_name)
            self.register_theme(theme)

        self.theme = self.all_themes[0]
        nasa_api = API(api_key)

    def on_key(self, event) -> None:
        if event.key == "q":
            self.exit()

    def on_button_pressed(self, event) -> None:
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

        if new_value in self.fav_themes:
            self.query_one("#selected-theme").update("Theme: ★" + self.selected_theme)
        else:
            self.query_one("#selected-theme").update("Theme: " + self.selected_theme)

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
