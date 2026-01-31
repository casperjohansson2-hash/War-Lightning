"""UI (user-interface) elements for menus and other..."""

from typing import (
    Tuple, List, Dict, Callable, Optional, Protocol, runtime_checkable
)
from dataclasses import dataclass
from threading import Thread
from os import environ
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
        self.rect = rect
        self.config = config
        self.text = text
        self.on_press = on_press

        self.drawn_border = config.bg
        self.drawn_bg = config.bg
        self.hover = False
        self.pressed = False
    
    def handle_event(self, event: pygame.event.Event) -> bool: 
        match event.type:
            case pygame.MOUSEMOTION:
                self.hover = self.rect.collidepoint(event.pos)
            case pygame.MOUSEBUTTONDOWN:
                self.pressed = self.hover
            case pygame.MOUSEBUTTONUP:
                if self.pressed:
                    self.pressed = False
                    self.on_press()
                    return True
            case pygame.WINDOWLEAVE:
                self.pressed = False

    def update(self, dt: float = 1) -> None: 
        if self.pressed:
            self.drawn_bg = self.config.pressed_bg
        elif self.hover:
            self.drawn_bg = self.config.hover_bg
        else:
            self.drawn_bg = self.config.bg
        self.drawn_border = (
            max(min(self.drawn_bg[0] + 30, 255), 0),
            max(min(self.drawn_bg[1] + 30, 255), 0),
            max(min(self.drawn_bg[2] + 30, 255), 0)
        )

    def render(self, surface: pygame.Surface) -> None: 
        if self.config.border_width > 0:
            pygame.draw.rect(surface, self.drawn_bg, self.rect, border_radius=self.config.border_radius)
        pygame.draw.rect(surface, self.drawn_border, self.rect, self.config.border_width, self.config.border_radius)
        self.text.render(surface, center=self.rect.center)

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

class Central: # THIS IS NOT THREAD-SAFE!!!
    uis: Dict[str, "UI"] = {}

    @classmethod
    def add(cls, ui: "UI") -> None:
        cls.uis[ui.name] = ui
    
    @classmethod
    def get(cls, name: str) -> Optional["UI"]:
        return cls.uis.get(name) # graceful

class UI:
    def __init__(self, name: str) -> None:
        self.name = name
        self.elements = []
        Central.add(self)
    
    def add_element(self, element: Element) -> "UI":
        self.elements.append(element)
        return self
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        for element in reversed(self.elements):
            if element.handle_event(event):
                return True
    
    def update(self, dt: float) -> None:
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

def get_mode() -> str:
    """Import this method and call it to retrieve what mode the user has selected."""
    return environ["mode"]

def stop_loading() -> None:
    """Has to be done before pygame.init(), smoothly loads into the game. Must be following the 'get_mode'. 
    DO NOT forget to handle in case the user selected 'exit' afterwards this."""
    loader.stop()
    pygame.display.quit()


pygame.mixer.music.load("assets/music/menu.mp3")

#BUTTON_SOUND = pygame.mixer.Sound("assets/ui/press_button.mp3")

HEADER_FONT = pygame.font.Font("assets/fonts/Smile Delight.ttf", 50)
PRIMARY_FONT = pygame.font.SysFont("assets/fonts/SEEKUW.ttf", 25, bold=True)

MAIN_MENU = UI("Menu")
MODE_MENU = UI("Modes")

TITLE = Text(HEADER_FONT, "War Lightning", (50, 50, 50))
SELECT_MODE_TITLE = Text(HEADER_FONT, "Select Mode", (50, 50, 50))

LOADING_TEXT = Text(PRIMARY_FONT, "Loading...", (50, 50, 50))

class Menu:
    def __init__(self, screen: pygame.Surface) -> None:
        pygame.mixer.music.play(-1)

        self.screen = screen
        self.clock = pygame.time.Clock()
        self.active = False
        self.ui = MAIN_MENU

    def start(self) -> None:
        #BUTTON_SOUND.play()
        self.ui = Central.get("Modes")

    def back_to_start(self) -> None:
        #BUTTON_SOUND.play()
        self.ui = Central.get("Menu")

    def select_solo(self) -> None:
        #BUTTON_SOUND.play()
        self.active = False
        environ["mode"] = "solo"

    def select_vs(self) -> None:
        #BUTTON_SOUND.play()
        self.active = False
        environ["mode"] = "vs"

    def quit(self) -> None:
        #BUTTON_SOUND.play()
        self.active = False
        environ["mode"] = "exit"

    def run(self):
        self.active = True
        while self.active:
            dt = self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                self.ui.handle_event(event)
            
            self.screen.fill((255, 255, 255))

            self.ui.update(dt)
            self.ui.render(self.screen)

            pygame.display.flip()

class Loader:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.active = False
        self.thread = None

        self.text_rect = LOADING_TEXT.text_rect(center=screen.get_rect().center)
    
    def _loop(self) -> None:
        self.active = True
        while self.active:
            for event in pygame.event.get():
                ...
            self.screen.fill((255, 255, 255))

            LOADING_TEXT.render(self.screen, self.text_rect)

            pygame.display.flip()
        pygame.mixer.music.stop()
    
    def run(self) -> None:
        self.thread = Thread(target=self._loop)
        self.thread.start()
            
    def stop(self) -> None:
        self.active = False
        if self.thread:
            self.thread.join()
    
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
        15, 2
    ),
    Text(PRIMARY_FONT, "Start", (50, 50, 50)),
    lambda: menu.start()
))\
.add_element(Button(
    pygame.Rect(350, 500, 100, 25),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        15, 2
    ),
    Text(PRIMARY_FONT, "Exit", (50, 50, 50)),
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
        15, 2
    ),
    Text(PRIMARY_FONT, "Solo", (50, 50, 50)),
    lambda: menu.select_solo()
))\
.add_element(Button(
    pygame.Rect(525, 300, 150, 38),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        15, 2
    ),
    Text(PRIMARY_FONT, "VS", (50, 50, 50)),
    lambda: menu.select_vs()
))\
.add_element(Button(
    pygame.Rect(350, 500, 100, 25),
    ButtonConfig(
        (150, 150, 150),
        (100, 100, 100),
        (255, 0, 0),
        15, 2
    ),
    Text(PRIMARY_FONT, "Go Back", (50, 50, 50)),
    lambda: menu.back_to_start()
))


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("War Lightning")
#pygame.display.set_icon()

menu = Menu(screen)
loader = Loader(screen)

menu.run()
loader.run() # Loading screen, in case you have a slow computer or want to adjust things before the game really starts.