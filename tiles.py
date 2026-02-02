from typing import (
    Tuple, Dict, Literal, Optional, Self, Any
)
from typing import TypedDict
from enum import Enum, auto
import pygame

class KeyBinds(TypedDict):
    up: int = pygame.K_w
    down: int = pygame.K_s
    left: int = pygame.K_a
    right: int = pygame.K_d

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

REQUIRED_ANGLE = {
    # Base, Desired
    (Direction.UP, Direction.UP): 0,
    (Direction.UP, Direction.RIGHT): 270,
    (Direction.UP, Direction.DOWN): 180,
    (Direction.UP, Direction.LEFT): 90,
    (Direction.RIGHT, Direction.UP): 90,
    (Direction.RIGHT, Direction.RIGHT): 0,
    (Direction.RIGHT, Direction.DOWN): 270,
    (Direction.RIGHT, Direction.LEFT): 180,
    (Direction.DOWN, Direction.UP): 180,
    (Direction.DOWN, Direction.RIGHT): 90,
    (Direction.DOWN, Direction.DOWN): 0,
    (Direction.DOWN, Direction.LEFT): 270,
    (Direction.LEFT, Direction.UP): 270,
    (Direction.LEFT, Direction.RIGHT): 180,
    (Direction.LEFT, Direction.DOWN): 90,
    (Direction.LEFT, Direction.LEFT): 0,
}

class Tile:
    def __init__(self, image: pygame.Surface, direction: Direction, rect: Optional[pygame.Rect]) -> None:
        self.base_image = image
        self.base_direction = direction

        self.image = image
        self.direction = direction
        self.rect = rect

        self.cache = {}
    
    def get_rect(self, **kwargs: Any) -> pygame.Rect:
        return self.rect or self.image.get_rect(**kwargs)
    
    def rotate(self, angle: Literal[0, 90, 180, 270]) -> None:
        self.direction = self.base_direction
        steps = range(int(angle / 90))
        for _ in steps:
            match self.direction:
                case Direction.UP:
                    self.direction = Direction.RIGHT
                case Direction.RIGHT:
                    self.direction = Direction.DOWN
                case Direction.LEFT:
                    self.direction = Direction.UP
        self.image = self.cache.setdefault(angle, pygame.transform.rotate(self.base_image, angle))
    
    def render(self, surface: pygame.Surface, rect: Optional[pygame.Rect] = None, **kwargs: Any) -> None:
        surface.blit(self.image, rect or self.get_rect(**kwargs))

    @classmethod
    def new_tile(self, path: str, size: Tuple[int, int], direction: Direction, rect: Optional[pygame.Rect] = None) -> Self:
        image = pygame.image.load(path)
        scaled_image = pygame.transform.smoothscale(image, size)
        return Tile(scaled_image, direction, rect)

"""
Usage:

sand = Tile.new_tile("assets/sand_texture.png", (100, 100), Direction.UP, pygame.Rect(10, 10, 100, 100))
sand.render(surface)
"""

class Player:
    def __init__(self, tile: Tile, x: Optional[int] = None, y: Optional[int] = None, keybinds: KeyBinds = None, speed: int = 2, data: Optional[Dict[str, Any]] = None, rect: Optional[pygame.Rect] = None) -> None:
        self.tile = tile
        self.pos_x = x
        self.pos_y = y
        self.keybinds = keybinds or {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d}
        self.speed = speed
        self.data = data or {}
        self.rect = rect
    
    def get_rect(self, **kwargs: Any) -> None:
        return self.rect or (self.tile.get_rect(**kwargs) if len(kwargs) > 0 else self.tile.get_rect(topleft=(self.pos_x, self.pos_y)))
    
    def move(self, direction: Direction, distance: float) -> None:
        required_angle = REQUIRED_ANGLE[(self.tile.base_direction, direction)]
        self.tile.rotate(required_angle)
        match direction:
            case Direction.UP:
                self.pos_y -= distance
            case Direction.DOWN:
                self.pos_y += distance
            case Direction.RIGHT:
                self.pos_x += distance
            case Direction.LEFT:
                self.pos_x -= distance
    
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        dy = (keys[self.keybinds['down']] - keys[self.keybinds['up']]) * self.speed
        dx = (keys[self.keybinds['right']] - keys[self.keybinds['left']]) * self.speed
        direction = None
        if not dy == 0:
            direction, speed = (Direction.UP, -dy) if dy < 0 else (Direction.DOWN, dy)
        elif not dx == 0:
            direction, speed = (Direction.LEFT, -dx) if dx < 0 else (Direction.RIGHT, dx)
        if direction:
            self.move(direction, speed * dt)
    
    def render(self, surface: pygame.Surface, rect: Optional[pygame.Rect] = None, **kwargs: Any) -> None:
        surface.blit(self.tile.image, rect or self.get_rect(**kwargs))

class Map(pygame.Surface):
    def __init__(self, size: Tuple[int, int], rect: pygame.Rect) -> None:
        self.size = size
        self.rect = rect
    
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self, self.rect)
    
"""
Usage:

map = Map((WIDTH, HEIGHT), pygame.Rect(0, 0, WIDTH, HEIGHT))
sand.render(map)

map.render(surface)
"""