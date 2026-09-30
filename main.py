import os

from kivy.app import App
from kivy.core.window import Window

from ui import GameView


class TajemnicaApp(App):
    title = "Tajemnica o 3 w Nocy"
    icon = "assets/icon.png"

    def build(self):
        Window.clearcolor = (0.04, 0.04, 0.07, 1)
        return GameView(os.path.join(self.user_data_dir, "save.json"))


if __name__ == "__main__":
    TajemnicaApp().run()
