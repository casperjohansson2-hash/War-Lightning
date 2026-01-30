"""UI (user-interface) elements for menus and other..."""

from typing import (
    Callable, Optional, Protocol, runtime_checkable
)
from dataclasses import dataclass
import pygame

@runtime_checkable
class Element(Protocol):
    """Construction drawing for construction drawings"""
    rect: pygame.Rect

    def handle_event(self, event: pygame.event.Event) -> None: ...
    def update(self, dt: float) -> None: ...
    def render(self, surface: pygame.Surface) -> None: ...

class Text:
    def __init__(
        self, 
        font: pygame.font.Font,
        text: str,
        color: tuple[int, int, int],
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

@dataclass # Simpelt, består BARA data
class ButtonConfig:
    bg: tuple[int, int, int] # background
    hover_bg: tuple[int, int, int]
    pressed_bg: tuple[int, int, int]
    border_color: tuple[int, int, int]
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

        self.drawn_bg = config.bg
        self.hover = False
        self.pressed = False
    
    def handle_event(self, event: pygame.event.Event) -> None: 
        match event.type:
            case pygame.MOUSEMOTION:
                self.hover = self.rect.collidepoint(event.pos)
            case pygame.MOUSEBUTTONDOWN:
                self.pressed = self.hover
            case pygame.MOUSEBUTTONUP:
                if self.pressed:
                    self.on_press()
                self.pressed = False
            case pygame.WINDOWLEAVE:
                self.pressed = False

    def update(self, dt: float) -> None: 
        if self.pressed:
            self.drawn_bg = self.config.pressed_bg
        elif self.hover:
            self.drawn_bg = self.config.hover_bg
        else:
            self.drawn_bg = self.config.bg

    def render(self, surface: pygame.Surface) -> None: 
        pygame.draw.rect(surface, self.drawn_bg, self.rect, border_radius=self.config.border_radius)
        pygame.draw.rect(surface, self.drawn_bg, self.rect, self.config.border_width, self.config.border_radius)
        self.text.render(surface, center=self.rect.center)