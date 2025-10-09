"""This holds all custom UI Widgets"""
from textual.containers import VerticalGroup, Vertical, Center, Horizontal
from textual.widgets import Button, Static, Label


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
