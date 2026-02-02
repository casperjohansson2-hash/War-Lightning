"""Thank me later, and don't thank maxi for making every wall different sizes!"""

from typing import (
    Iterable, Dict, Callable, Generator, Self, Final, Any
)
import cv2
import numpy as np
import pygame

BREAK_LOOP: Final = object()

class Keybinds:
    binds: Dict[str, int]

    def __init__(self, **binds: int) -> None:
        self.binds = binds
    
    def bind(self, name: str, key: int) -> None:
        self.binds[name] = key
    
    def bind_all(self, binds: Dict[str, int]) -> None:
        self.binds.update(binds)
    
    def get_pressed(self) -> Dict[str, bool]:
        all_keys = pygame.key.get_pressed()
        pressed_keys = {}
        for name, key in self.binds.items():
            pressed_keys[name] = all_keys[key]
        return pressed_keys

class Screen:
    surface: pygame.Surface
    clock: pygame.time.Clock
    target_fps: float
    delta_time: float
    active: bool

    def __init__(self, width: int, height: int, target_fps: float = 60.0) -> None:
        self.surface = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.target_fps = target_fps
        self.delta_time = 1.0
        self.active = False
    
    def tick(self) -> None:
        self.delta_time = self.clock.tick(self.target_fps) / 1000
    
    def flip(self) -> None:
        pygame.display.flip()
    
    def stop(self) -> None:
        self.active = False
    
    def run(self, loop: Callable[[float], Any]) -> None:
        self.active = True
        while self.active:
            self.tick()
            if loop(self.delta_time) is BREAK_LOOP:
                self.stop()
            self.flip()

class World:
    objects: Iterable[pygame.Rect]

    def __init__(self, *objects: pygame.Rect) -> None:
        self.objects = objects
    
    def find_collisions(self, rect: pygame.Rect) -> Generator[pygame.Rect, Any, None]:
        for obj in self.objects:
            if obj.colliderect(rect):
                yield obj
    
    def draw_boxes(self, surface: pygame.Surface) -> None:
        for obj in self.objects:
            pygame.draw.rect(surface, (255, 0, 0), obj, 1)
    
class Image:
    base_surface: pygame.Surface
    surface: pygame.Surface
    rect: pygame.Rect
    rotation: int
    cache: Dict[int, pygame.Surface]

    def __init__(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        self.base_surface = surface
        self.surface = surface
        self.rect = rect

        self.rotation = 0
        self.cache = {}
    
    def rotate(self, angle: int) -> None:
        self.surface = self.cache.setdefault(angle, pygame.transform.rotate(self.base_surface, angle))
        self.rotation = angle
    
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.surface, self.rect)
    
    @classmethod
    def new_image(self, path: str, rect: pygame.Rect) -> Self:
        image = pygame.image.load(path)
        scaled = pygame.transform.scale(image, rect.size)
        return Image(scaled, rect)

class Player:
    world: World
    image: Image
    keybinds: Keybinds
    speed: float

    def __init__(self, world: World, image: Image, keybinds: Keybinds, speed: float) -> None:
        self.world = world
        self.image = image
        self.keybinds = keybinds
        self.speed = speed
    
    def update(self, dt: float) -> None:
        pressed_keys = self.keybinds.get_pressed()
        dx = (pressed_keys["right"] - pressed_keys["left"]) * self.speed * dt
        dy = (pressed_keys["down"] - pressed_keys["up"]) * self.speed * dt
        if not dy == 0:
            dummy = self.image.rect.copy()
            dummy.y += dy
            if dy > 0:
                self.image.rotate(180)
                for collision in self.world.find_collisions(dummy):
                    dummy.bottom = collision.top
            elif dy < 0:
                self.image.rotate(0)
                for collision in self.world.find_collisions(dummy):
                    dummy.top = collision.bottom
            self.image.rect = dummy
        elif not dx == 0:
            dummy = self.image.rect.copy()
            dummy.x += dx
            if dx > 0:
                self.image.rotate(270)
                for collision in self.world.find_collisions(dummy):
                    dummy.right = collision.left
            elif dx < 0:
                self.image.rotate(90)
                for collision in self.world.find_collisions(dummy):
                    dummy.left = collision.right
            self.image.rect = dummy
    
    def render(self, surface: pygame.Surface) -> None:
        self.image.render(surface)

def surface_to_gray(surface: pygame.Surface) -> np.ndarray:
    surface = surface.convert()  # remove alpha
    arr = pygame.surfarray.array3d(surface)
    arr = arr.swapaxes(0, 1)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

def merge_rects(rects, padding=4):
    merged = []
    for r in rects:
        r = r.inflate(padding, padding)
        for m in merged:
            if r.colliderect(m):
                break
        else:
            merged.append(r)
    return merged

def find_image(
    template: pygame.Surface,
    source: pygame.Surface,
    threshold: float = 0.15
) -> list[pygame.Rect]:

    tpl = surface_to_gray(template)
    src = surface_to_gray(source)

    result = cv2.matchTemplate(src, tpl, cv2.TM_SQDIFF_NORMED)
    ys, xs = np.where(result <= threshold)

    w, h = template.get_size()
    rects = [pygame.Rect(x, y, w, h) for x, y in zip(xs, ys)]

    return merge_rects(rects)


# Example:

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = Screen(WIDTH, HEIGHT)

background = Image.new_image("assets/tiles/map1.png", pygame.Rect(0, 0, WIDTH, HEIGHT))
wall = pygame.image.load("assets/tiles/wallwall.png").convert()

scales = [(40, 15), (45, 12)]
wall_rects = []

for scale in scales:
    tpl = pygame.transform.smoothscale(wall, scale)
    wall_rects.extend(find_image(tpl, background.surface))

print(wall_rects)

world = World(*wall_rects)

player_image = Image.new_image("assets/tanks/Player1.png", pygame.Rect(600, 300, 50, 50))

player_keybinds = Keybinds(up=pygame.K_w, down=pygame.K_s, left=pygame.K_a, right=pygame.K_d)
player = Player(world, player_image, player_keybinds, 200)

@screen.run
def main_loop(delta_time: float) -> Any:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return BREAK_LOOP
    
    background.render(screen.surface)
    
    screen.surface.blit(wall, (50, 50))
    player.update(delta_time)
    player.render(screen.surface)
    world.draw_boxes(screen.surface)

pygame.quit()