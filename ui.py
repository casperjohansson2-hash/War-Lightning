"""UI (user-interface) elements for menus and other..."""

from typing import (
    Tuple, Dict, Callable, Optional, Protocol, runtime_checkable, Any
)
from dataclasses import dataclass
from functools import cache
import pygame

pygame.init()

@runtime_checkable
class Element(Protocol):
    """Construction drawing for construction drawings"""
    rect: pygame.Rect

    def handle_event(self, event: pygame.event.Event) -> bool: ...
    def update(self, dt: float = 1) -> None: ...
    def render(self, surface: pygame.Surface) -> None: ...

class Text:
    def __init__(
        self, 
        font: pygame.font.Font,
        text: str,
        color: Tuple[int, int, int],
    ) -> None:
        self.font = font
        self.text = text
        self.color = color
        self.surface = font.render(text, True, color)
    
    def edit_text(self, text: str) -> None:
        self.text = text
        self.surface = self.font.render(text, True, self.color)
    
    def text_rect(self, **kwargs) -> pygame.Rect:
        """Usage: 
        Text(...).text_rect(center=(10, 10)) 
        ...or... 
        Text(...).text_rect(topleft=(10, 10))"""
        return self.surface.get_rect(**kwargs)
    
    def render(self, surface: pygame.Surface, rect: Optional[pygame.Rect] = None, **kwargs) -> None:
        surface.blit(self.surface, rect if rect is not None else self.text_rect(**kwargs))

"""
font = pygame.font.SysFont(...)
text = Text(font, "Hello!", (10, 10, 10)) # (r, g, b)
#rect = text.text_rect(center=(10, 10))
#text.render(surface, rect)
text.render(surface, center=(10, 10))
"""

class Label(Element):
    def __init__(self, rect: pygame.Rect, text: Text) -> None:
        self.rect = rect
        self.text = text
    
    def handle_event(self, event: pygame.event.Event) -> bool: ...
    def update(self, dt: float = 1) -> None: ...
    def render(self, surface: pygame.Surface) -> None: 
        self.text.render(surface, self.rect)

class Image(Element):
    def __init__(self, image: pygame.Surface, rect: Optional[pygame.Rect] = None, **kwargs) -> None:
        self.rect = rect or image.get_rect(**kwargs)
        self.image = image
    
    def handle_event(self, event: pygame.event.Event) -> bool: ...
    def update(self, dt: float = 1) -> None: ...
    def render(self, surface: pygame.Surface) -> None: 
        surface.blit(self.image, self.rect)

@dataclass # Simpelt, består BARA data
class ButtonConfig:
    bg: Tuple[int, int, int] # background
    hover_bg: Tuple[int, int, int]
    pressed_bg: Tuple[int, int, int]
    alpha: int
    border_radius: int
    border_width: int

"""
config = ButtonConfig(bg=(50, 50, 50), ...)
print(config.bg) # -> (50, 50, 50)
"""

class Button(Element):
    def __init__(
        self,
        rect: pygame.Rect,
        config: ButtonConfig,
        text: Text,
        on_press: Callable
    ) -> None:
        self.surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.rect = rect
        self.config = config
        self.text = text
        self.on_press = on_press

        self.offset_rect = pygame.Rect(0, 0, rect.width, rect.height)
        self.drawn_border = config.bg
        self.drawn_bg = config.bg
        self.hover = False
        self.pressed = False
        self._fix = True

        self.update()
    
    def handle_event(self, event: pygame.event.Event) -> bool: 
        match event.type:
            case pygame.MOUSEMOTION:
                was_hovered = self.hover
                self.hover = self.rect.collidepoint(event.pos)
                self._fix = not self.hover == was_hovered
            case pygame.MOUSEBUTTONDOWN:
                was_pressed = self.pressed
                self.pressed = self.hover
                self._fix = not self.pressed == was_pressed
            case pygame.MOUSEBUTTONUP:
                if self.pressed:
                    self._fix = True
                    self.pressed = False
                    self.on_press()
                    return True
            case pygame.WINDOWLEAVE:
                self.pressed = False
                self._fix = True

    def update(self, dt: float = 1) -> None: 
        if self._fix:
            if self.pressed:
                self.drawn_bg = self.config.pressed_bg
            elif self.hover:
                self.drawn_bg = self.config.hover_bg
            else:
                self.drawn_bg = self.config.bg
            self.drawn_border = (
                max(min(self.drawn_bg[0] + 50, 255), 0),
                max(min(self.drawn_bg[1] + 60, 255), 0),
                max(min(self.drawn_bg[2] + 70, 255), 0)
            )
            pygame.draw.rect(self.surface, self.drawn_bg, self.offset_rect, border_radius=self.config.border_radius)
            if self.config.border_width > 0:
                pygame.draw.rect(self.surface, self.drawn_border, self.offset_rect, self.config.border_width, self.config.border_radius)
            self.text.render(self.surface, center=self.offset_rect.center)
            self.surface.set_alpha(self.config.alpha)
            self._fix = False

    def render(self, surface: pygame.Surface) -> None: 
        surface.blit(self.surface, self.rect)

@dataclass
class SliderConfig:
    slider_bg: Tuple[int, int, int]
    bg: Tuple[int, int, int] # background
    hover_bg: Tuple[int, int, int]
    pressed_bg: Tuple[int, int, int]
    alpha: int
    slider_radius: int
    slider_width: int
    border_radius: int
    border_width: int

class Slider(Element):
    def __init__(
        self,
        rect: pygame.Rect,
        config: SliderConfig,
        initial: float,
        range: Tuple[float, float],
        on_change: Callable[[float], Any]
    ) -> None:
        self.surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.button_rect = pygame.Rect(0, 0, rect.height, rect.height)
        height_diff = (rect.height - rect.height / 2)
        self.slider_rect = pygame.Rect(height_diff, rect.height / 4, rect.width - height_diff * 2, rect.height / 2)
        self.rect = rect
        self.config = config
        self.range = range
        self.on_change = on_change

        self.factor = initial / (self.range[1] - self.range[0]) - range[0]
        self.drawn_border = config.bg
        self.drawn_bg = config.bg
        self.hover = False
        self.pressed = False
    
    @property
    def value(self) -> float:
        return self.range[0] + (self.range[1] - self.range[0]) * self.factor
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False

        elif event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
            if self.pressed:
                local_x = event.pos[0] - self.rect.x
                self.factor = max(0.0, min(1.0, local_x / self.rect.width))
                self.on_change(self.value)
                return True

        return False

    def update(self, dt=1):
        self.surface.fill((0, 0, 0, 0))

        if self.pressed:
            bg = self.config.pressed_bg
        elif self.hover:
            bg = self.config.hover_bg
        else:
            bg = self.config.bg

        border = (
            min(bg[0] + 50, 255),
            min(bg[1] + 60, 255),
            min(bg[2] + 70, 255),
        )

        slider_border = (
            min(self.config.slider_bg[0] + 50, 255),
            min(self.config.slider_bg[1] + 60, 255),
            min(self.config.slider_bg[2] + 70, 255),
        )

        self.button_rect.x = int(
            self.factor * (self.rect.width - self.button_rect.width)
        )

        pygame.draw.rect(self.surface, self.config.slider_bg, self.slider_rect, border_radius=self.config.slider_radius)

        if self.config.slider_width > 0:
            pygame.draw.rect(
                self.surface, 
                slider_border, 
                self.slider_rect, 
                self.config.slider_width,
                self.config.slider_radius
            )

        pygame.draw.rect(self.surface, bg, self.button_rect, border_radius=self.config.border_radius)

        if self.config.border_width > 0:
            pygame.draw.rect(
                self.surface,
                border,
                self.button_rect,
                self.config.border_width,
                self.config.border_radius,
            )

        self.surface.set_alpha(self.config.alpha)

    def render(self, surface: pygame.Surface) -> None: 
        surface.blit(self.surface, self.rect)

"""
def func():
    print("Hello")

button = Button(
    rect = pygame.Rect(x, y, width, height)
    config = ButtonConfig(
        bg = (r, g, b),
        hover_bg = (r, g, b),
        pressed_bg = (r, g, b)
        border_color = (r, g, b)
        border_radius = 5
        border_width = 1
    ),
    text = Text(
        font = <font>,
        text = "Text",
        color = (r, g, b)
    ),
    on_press = func
)
"""

class UI:
    def __init__(self, name: str) -> None:
        self.name = name
        self.elements = []
    
    def add_element(self, element: Element) -> "UI":
        self.elements.append(element)
        return self
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        for element in reversed(self.elements):
            if element.handle_event(event):
                return True
    
    def update(self, dt: float = 1) -> None:
        for element in self.elements:
            element.update(dt)
    
    def render(self, surface: pygame.Surface) -> None:
        for element in self.elements:
            element.render(surface)

"""
Usage:
button = Button(...)
menu = UI("Menu")
menu.add_element(button)
...
menu.handle_event(event)
...
menu.update(dt)
menu.render(screen el. surface)
...
m = Central.get("Menu")
"""

class AppState:
    mode: Optional[str] = None
    kind: Optional[str] = None
    settings: Dict[str, Any] = {
        "hitboxes": False,
        "volume": 1.0,
        "particles": True
    }

@cache # Faster retrieval
def get_mode() -> str:
    """Import this method and call it to retrieve what mode the user has selected."""
    return AppState.mode

@cache
def get_setting(name: str) -> Dict[str, Any]:
    """Import this method and call it to retireve the settings."""
    return AppState.settings[name]

pygame.mixer.music.load("assets/music/menu.mp3")

BACKGROUND_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/ui/test.png"), (800, 600))
DIM = pygame.Surface((800, 600), pygame.SRCALPHA)
DIM.fill((50, 50, 50, 150))

BUTTON_SOUND = pygame.mixer.Sound("assets/audio/press button.mp3")

HEADER_FONT = pygame.font.Font("assets/fonts/Smile Delight.ttf", 50)
PRIMARY_FONT = pygame.font.Font("assets/fonts/SEEKUW.ttf", 15)

MAIN_MENU = UI("Menu")
MODE_MENU = UI("Modes")
KIND_MENU = UI("Kinds")
SETTINGS = UI("Settings")
CREDIBILITY = UI("Cred")

TITLE = Text(HEADER_FONT, "War Lightning", (255, 255, 255))
SELECT_MODE_TITLE = Text(HEADER_FONT, "Select Mode", (255, 255, 255))
SETTINGS_TITLE = Text(HEADER_FONT, "Settings", (255, 255, 255))
CRED_TITLE = Text(HEADER_FONT, "Creds", (255, 255, 255))

HITBOX_TEXT = Text(PRIMARY_FONT, "Disabled", (255, 255, 255))
PARTICLE_TEXT = Text(PRIMARY_FONT, "Enabled", (255, 255, 255))
VOLUME_TEXT = Text(PRIMARY_FONT, "Volume: 100%", (255, 255, 255))

class Menu:
    def __init__(self, screen: pygame.Surface) -> None:
        pygame.mixer.music.play(-1)

        self.screen = screen
        self.clock = pygame.time.Clock()
        self.active = False
        self.ui = MAIN_MENU

    def start(self) -> None:
        BUTTON_SOUND.play()
        self.ui = MODE_MENU
    
    def open_settings(self) -> None:
        BUTTON_SOUND.play()
        self.ui = SETTINGS
    
    def open_credits(self) -> None:
        BUTTON_SOUND.play()
        self.ui = CREDIBILITY
    
    def toggle_hitboxes(self) -> None:
        BUTTON_SOUND.play()
        was_active = AppState.settings["hitboxes"]
        AppState.settings["hitboxes"] = not was_active
        HITBOX_TEXT.edit_text("Disabled" if was_active else "Enabled")
    
    def edit_volume(self, volume: float) -> None:
        AppState.settings["volume"] = volume
        BUTTON_SOUND.set_volume(volume)
        pygame.mixer.music.set_volume(volume)
        VOLUME_TEXT.edit_text(f"Volume: {round(volume * 100)}%")
    
    def toggle_particles(self) -> None:
        BUTTON_SOUND.play()
        was_active = AppState.settings["particles"]
        AppState.settings["particles"] = not was_active
        PARTICLE_TEXT.edit_text("Disabled" if was_active else "Enabled")

    def back_to_start(self) -> None:
        BUTTON_SOUND.play()
        self.ui = MAIN_MENU

    def select_solo(self) -> None:
        BUTTON_SOUND.play()
        self.ui = KIND_MENU
        AppState.mode = "solo"

    def select_vs(self) -> None:
        BUTTON_SOUND.play()
        self.ui = KIND_MENU
        AppState.mode = "vs"
    
    def select_kingofhill(self) -> None:
        BUTTON_SOUND.play()
        self.active = False
        AppState.kind = "king of hill"
    
    def select_deathmatch(self) -> None:
        BUTTON_SOUND.play()
        self.active = False
        AppState.kind = "king of hill"

    def quit(self) -> None:
        BUTTON_SOUND.play()
        self.active = False
        AppState.mode = "exit"

    def run(self):
        self.active = True
        while self.active:
            dt = self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                self.ui.handle_event(event)
            
            self.screen.fill((255, 255, 255))
            self.screen.blit(BACKGROUND_IMAGE, (0, 0))
            self.screen.blit(DIM, (0, 0))

            self.ui.update(dt)
            self.ui.render(self.screen)

            pygame.display.flip()
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    
MAIN_MENU\
.add_element(Label(
    TITLE.text_rect(center=(400, 30)), TITLE
))\
.add_element(Button(
    pygame.Rect(325, 300, 150, 38),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Start", (200, 235, 220)),
    lambda: menu.start()
))\
.add_element(Button(
    pygame.Rect(325, 350, 150, 38),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Settings", (200, 235, 220)),
    lambda: menu.open_settings()
))\
.add_element(Button(
    pygame.Rect(325, 400, 150, 38),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Creds", (200, 235, 220)),
    lambda: menu.open_credits()
))\
.add_element(Button(
    pygame.Rect(350, 500, 100, 25),
    ButtonConfig(
        (190, 150, 150),
        (140, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Exit", (200, 235, 220)),
    lambda: menu.quit()
))

MODE_MENU\
.add_element(Label(
    SELECT_MODE_TITLE.text_rect(center=(400, 30)), SELECT_MODE_TITLE
))\
.add_element(Button(
    pygame.Rect(125, 300, 150, 38),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Solo", (200, 235, 220)),
    lambda: menu.select_solo()
))\
.add_element(Button(
    pygame.Rect(525, 300, 150, 38),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Versus", (200, 235, 220)),
    lambda: menu.select_vs()
))\
.add_element(Button(
    pygame.Rect(350, 500, 100, 25),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Go Back", (200, 235, 220)),
    lambda: menu.back_to_start()
))

KIND_MENU\
.add_element(Label(
    SELECT_MODE_TITLE.text_rect(center=(400, 30)), SELECT_MODE_TITLE
))\
.add_element(Button(
    pygame.Rect(125, 300, 150, 38),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Deathmatch", (200, 235, 220)),
    lambda: menu.select_deathmatch()
))\
.add_element(Button(
    pygame.Rect(525, 300, 150, 38),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "King Of The Hill", (200, 235, 220)),
    lambda: menu.select_kingofhill()
))\
.add_element(Button(
    pygame.Rect(350, 500, 100, 25),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Go Back", (200, 235, 220)),
    lambda: menu.back_to_start()
))

SETTINGS\
.add_element(Label(
    SETTINGS_TITLE.text_rect(center=(400, 30)), SETTINGS_TITLE
))\
.add_element(Label(
    HITBOX_TEXT.text_rect(center=(550, 200)), HITBOX_TEXT
))\
.add_element(Button(
    pygame.Rect(325, 180, 150, 38),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Toggle Hitboxes", (200, 235, 220)),
    lambda: menu.toggle_hitboxes()
))\
.add_element(Label(
    VOLUME_TEXT.text_rect(center=(550, 250)), VOLUME_TEXT
))\
.add_element(Slider(
    pygame.Rect(325, 240, 150, 25),
    SliderConfig(
        (150, 150, 250),
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 5, 2, 15, 2
    ),
    1.0,
    (0.0, 1.0),
    lambda vol: menu.edit_volume(vol)
))\
.add_element(Label(
    PARTICLE_TEXT.text_rect(center=(550, 300)), PARTICLE_TEXT
))\
.add_element(Button(
    pygame.Rect(325, 280, 150, 38),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Toggle Particles", (200, 235, 220)),
    lambda: menu.toggle_particles()
))\
.add_element(Button(
    pygame.Rect(350, 500, 100, 25),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Go Back", (200, 235, 220)),
    lambda: menu.back_to_start()
))

CREDIBILITY\
.add_element(Label(
    CRED_TITLE.text_rect(center=(400, 30)), CRED_TITLE
))\
.add_element(Button(
    pygame.Rect(350, 500, 100, 25),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        200, 15, 2
    ),
    Text(PRIMARY_FONT, "Go Back", (200, 235, 220)),
    lambda: menu.back_to_start()
))

with open("credits.txt", "r") as f:
    credits = f.readlines()
for index, line in enumerate(credits):
    line = line.replace("\n", "").strip()
    text = Text(PRIMARY_FONT, line, (255, 255, 255))
    label = Label(text.text_rect(center=(400, 100+20*index)), text)
    CREDIBILITY.add_element(label)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("War Lightning")
pygame.display.set_icon(pygame.image.load("assets/ui/war_lightning.png"))

menu = Menu(screen)

menu.run()

pygame.display.quit()