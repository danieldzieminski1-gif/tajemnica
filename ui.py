import json
import os

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from story import STORY, START

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
TOTAL = sum(1 for n in STORY.values() if n.get("end"))
TXT = (0.32, 0.05, 0.22, 1)


class Pink(FloatLayout):
    """Różowy panel w stylu Doki Doki."""

    def __init__(self, color=(1, 0.74, 0.87, 0.93), **kw):
        super().__init__(**kw)
        with self.canvas.before:
            Color(*color)
            self.r = RoundedRectangle(radius=[16])
            Color(1, 1, 1, 0.95)
            self.l = Line(rounded_rectangle=(0, 0, 1, 1, 16), width=2)
        self.bind(pos=self._u, size=self._u)

    def _u(self, *_):
        self.r.pos, self.r.size = self.pos, self.size
        self.l.rounded_rectangle = (*self.pos, *self.size, 16)


class GameView(FloatLayout):
    def __init__(self, save_path, **kw):
        super().__init__(**kw)
        self.save_path = save_path
        self.found = self._load()
        self.node, self.i, self.full, self.pos_i = None, 0, "", 0
        self.auto = False

        self.bg = Image(fit_mode="cover", size_hint=(1, 1))
        self.sprite = Image(fit_mode="contain", size_hint=(0.32, 0.97),
                            pos_hint={"center_x": 0.5, "y": 0}, opacity=0)
        self.box = Pink(size_hint=(0.8, 0.28), pos_hint={"center_x": 0.5, "y": 0.09})
        self.text = Label(color=TXT, font_size="17sp", halign="left", valign="top",
                          size_hint=(0.94, 0.78), pos_hint={"x": 0.03, "top": 0.9})
        self.text.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.box.add_widget(self.text)
        self.tag = Pink(color=(1, 0.55, 0.78, 0.97), size_hint=(0.17, 0.075),
                        pos_hint={"x": 0.11, "y": 0.35})
        self.name = Label(color=(1, 1, 1, 1), bold=True, font_size="16sp")
        self.tag.add_widget(self.name)
        self.name.size_hint, self.name.pos_hint = (1, 1), {"x": 0, "y": 0}
        self.choices = BoxLayout(orientation="vertical", spacing=10,
                                 size_hint=(0.55, 0.4), pos_hint={"center_x": 0.5, "center_y": 0.6})
        menu = BoxLayout(size_hint=(0.3, 0.07), pos_hint={"center_x": 0.5, "y": 0.01})
        self.auto_btn = self._flat("Auto", self._toggle_auto)
        menu.add_widget(self.auto_btn)
        menu.add_widget(self._flat("Od nowa", lambda *_: self.show(START)))
        for w in (self.bg, self.sprite, self.box, self.tag, self.choices, menu):
            self.add_widget(w)
        self.show(START)

    # ---- zapis ----
    def _load(self):
        try:
            with open(self.save_path) as f:
                return set(json.load(f))
        except Exception:
            return set()

    def _save(self):
        try:
            with open(self.save_path, "w") as f:
                json.dump(sorted(self.found), f)
        except Exception:
            pass

    # ---- UI helpery ----
    def _flat(self, text, cb):
        b = Button(text=text, font_size="15sp", background_normal="", background_color=(0, 0, 0, 0),
                   color=(1, 1, 1, 1), outline_width=2, outline_color=(0.8, 0.3, 0.55, 1))
        b.bind(on_release=cb)
        return b

    def _pink_btn(self, label, nxt):
        b = Button(text=label, font_size="17sp", halign="center", valign="middle",
                   background_normal="", background_color=(1, 0.78, 0.89, 0.96), color=TXT)
        b.bind(size=lambda w, s: setattr(w, "text_size", (s[0] - 20, None)))
        b.bind(on_release=lambda *_: self.show(nxt))
        return b

    def _toggle_auto(self, *_):
        self.auto = not self.auto
        self.auto_btn.text = "Auto ✓" if self.auto else "Auto"
        self._auto_next()

    # ---- logika ----
    def show(self, nid):
        Clock.unschedule(self._tick)
        Clock.unschedule(self._auto)
        self.node, self.i = STORY[nid], -1
        self.bg.source = os.path.join(ASSETS, self.node["bg"] + ".png")
        self.bg.opacity = 0
        Animation(opacity=1, duration=0.7).start(self.bg)
        self.sprite.opacity = 0
        self.choices.clear_widgets()
        if self.node.get("end"):
            self.found.add(nid)
            self._save()
        self.next_line()

    def next_line(self):
        self.i += 1
        lines = self.node["lines"]
        if self.i >= len(lines):
            self._end_of_node()
            return
        who, text, spr = lines[self.i]
        self.name.text = who
        self.tag.opacity = 1 if who else 0
        if spr == "-":
            self.sprite.opacity = 0
        elif spr:
            self.sprite.source = os.path.join(ASSETS, f"ziomek_{spr}.png")
            self.sprite.opacity = 1
        self.full, self.pos_i, self.text.text = text, 0, ""
        Clock.unschedule(self._tick)
        Clock.schedule_interval(self._tick, 0.02)

    def _tick(self, dt):
        self.pos_i += 1
        self.text.text = self.full[:self.pos_i]
        if self.pos_i >= len(self.full):
            self._auto_next()
            return False

    def _auto_next(self):
        Clock.unschedule(self._auto)
        if self.auto and self.pos_i >= len(self.full) and not self.choices.children:
            Clock.schedule_once(self._auto, 1.8)

    def _auto(self, *_):
        if not self.choices.children:
            self.next_line()

    def _end_of_node(self):
        self.choices.clear_widgets()
        n = self.node
        if n.get("end"):
            self.name.text, self.tag.opacity = "", 0
            self.text.text = ""
            self.choices.add_widget(Label(text=f"ZAKOŃCZENIE: {n['end']}", bold=True, font_size="24sp",
                                          color=(1, 0.9, 0.5, 1), outline_width=3, outline_color=(0.4, 0, 0.2, 1)))
            self.choices.add_widget(Label(text=f"Odkryte zakończenia: {len(self.found)}/{TOTAL}",
                                          font_size="16sp", outline_width=2, outline_color=(0, 0, 0, 1)))
            self.choices.add_widget(self._pink_btn("Zagraj jeszcze raz", START))
        else:
            for label, nxt in n["choices"]:
                self.choices.add_widget(self._pink_btn(label, nxt))

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        if self.choices.children:
            return False
        if self.pos_i < len(self.full):  # dokończ pisanie
            Clock.unschedule(self._tick)
            self.pos_i, self.text.text = len(self.full), self.full
            self._auto_next()
        else:
            self.next_line()
        return True
