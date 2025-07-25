from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Footer
from ascii_magic import AsciiArt

plane = AsciiArt.from_image('plane.png').to_file("plane.txt", monochrome=True)
with open("plane.txt", "r") as file:
    plane = file.read()

class Sim(App):
    TITLE = "Flight Physics Simulator"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Label(plane)

if __name__ == "__main__":
    app = Sim()
    app.run()