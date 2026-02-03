"""Thank me later, and don't thank maxi for making every wall different sizes!"""

from typing import (
    Tuple, List, Dict, Callable, Generator, Self, Final, Any
)
from particles import Particles
import random
import cv2
import numpy as np
import pygame
import time
import ui

mode = ui.get_mode()
if mode == "exit":
    exit()

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
    objects: List[pygame.Rect]
    players: List["Player"]

    def __init__(self, *objects: pygame.Rect) -> None:
        self.objects = list(objects)
        self.players = []
    
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
    
    def copy(self) -> Self:
        return Image(self.base_surface.copy(), self.rect.copy())
    
    def rotate(self, angle: int) -> None:
        self.surface = self.cache.setdefault(angle, pygame.transform.rotate(self.base_surface, angle))
        self.rotation = angle
    
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.surface, self.surface.get_rect(center=self.rect.center))
    
    @classmethod
    def new_image(self, path: str, rect: pygame.Rect, scale: Tuple[int, int] = (0, 0)) -> Self:
        image = pygame.image.load(path)
        scaled = pygame.transform.scale(image, (rect.size[0] + scale[0], rect.size[1] + scale[1]))
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

        world.players.append(self)
    
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

class TankWorld(World):
    bullets: List["Bullet"]

    def __init__(self, *objects: pygame.Rect) -> None:
        super().__init__(*objects)
        self.bullets = []

class Bullet:
    world: TankWorld
    image: Image
    players: List["Player"]
    velocity: Tuple[int, int]
    damage: float

    def __init__(self, world: TankWorld, image: Image, players: List["Player"], velocity: Tuple[int, int], damage: float) -> None:
        self.world = world
        self.image = image
        self.players = players
        self.velocity = velocity
        self.damage = damage
    
    def update(self, dt: float) -> bool:
        self.image.rect.x += self.velocity[0] * dt
        self.image.rect.y += self.velocity[1] * dt
        
        for player in self.players:
            if self.image.rect.colliderect(player.image.rect):
                explosions.emit(*self.image.rect.center, 50)
                if self.damage >= 0.2:
                    crit_hit_sound.play()
                else:
                    normal_hit_sound.play()
                player.health -= self.damage
                if not player.is_alive:
                    death_explosions.emit(*player.image.rect.center, 200)
                    explosion_sound.play()
                return True
        
        for collision in self.world.find_collisions(self.image.rect):
            explosions.emit(*self.image.rect.center, 50)
            normal_hit_sound.play()
            return True
    
    def render(self, surface: pygame.Surface) -> None:
        self.image.render(surface)

class Tank(Player):
    bullet_speed: float
    health: float
    shoot_interval: float
    damage_func: Callable[[], float]
    bullet_image: Image

    def __init__(self, world: TankWorld, image: Image, keybinds: Keybinds, speed: float, bullet_speed: float, health: float, shoot_interval: float, bullet_image: Image, damage_func: Callable[[], float]) -> None:
        super().__init__(world, image, keybinds, speed)
        self.bullet_speed = bullet_speed
        self.health = health
        self.shoot_interval = shoot_interval
        self.damage_func = damage_func
        self.bullet_image = bullet_image

        self.last_shot = 0.0
    
    @property
    def is_alive(self) -> bool:
        return self.health > 0.0
    
    def update(self, dt: float) -> None:
        super().update(dt)
        pressed_keys = self.keybinds.get_pressed()
        now = time.monotonic()
        if pressed_keys["shoot"] and now - self.last_shot > self.shoot_interval:
            shoot_sound.play()
            self.last_shot = now
            if self.image.rotation == 0:
                vel = (0, -self.bullet_speed)
            elif self.image.rotation == 270:
                vel = (self.bullet_speed, 0)
            elif self.image.rotation == 180:
                vel = (0, self.bullet_speed)
            elif self.image.rotation == 90:
                vel = (-self.bullet_speed, 0)
            players = [player for player in self.world.players if player.is_alive and not player is self]
            bullet = Bullet(self.world, self.bullet_image.copy(), players, vel, self.damage_func())
            bullet.image.rect.center = self.image.rect.center
            self.world.bullets.append(bullet)


def surface_to_cv(surface: pygame.Surface) -> np.ndarray:
    return pygame.surfarray.array3d(surface).swapaxes(0, 1)

def find_image(template: pygame.Surface, source: pygame.Surface, threshold: float = 0.5) -> List[pygame.Rect]:
    tpl = surface_to_cv(template)
    src = surface_to_cv(source)

    result = cv2.matchTemplate(src, tpl, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    rects = []
    w, h = template.get_size()

    for pt in zip(*locations[::-1]):
        rects.append(pygame.Rect(pt[0], pt[1], w, h))

    return rects

pygame.display.init()

WIDTH, HEIGHT = 1920, 1080
screen = Screen(WIDTH, HEIGHT)
pygame.display.set_caption("War Lightning")
pygame.display.set_icon(pygame.image.load("assets/ui/war_lightning.png"))

explosions = Particles(
    size=(WIDTH, HEIGHT),
    vel_x=(-400, 400),
    vel_y=(-400, 400),
    acc_x=(-50, 50),
    acc_y=(-50, 50),
    decay_x=(0.5, 0.85),
    decay_y=(0.5, 0.85),
    decay_size=(0.75, 0.95),
    radius=(3, 9)
)

death_explosions = Particles(
    size=(WIDTH, HEIGHT),
    vel_x=(-800, 800),
    vel_y=(-800, 800),
    acc_x=(-50, 50),
    acc_y=(-50, 50),
    decay_x=(0.3, 0.85),
    decay_y=(0.3, 0.85),
    decay_size=(0.65, 0.95),
    radius=(6, 12)
)

shoot_sound = pygame.mixer.Sound("assets/audio/Tank_shot.mp3")
normal_hit_sound = pygame.mixer.Sound("assets/audio/Metal_hit.mp3")
crit_hit_sound = pygame.mixer.Sound("assets/audio/Metal_pierce.mp3")
explosion_sound = pygame.mixer.Sound("assets/audio/Tank_kaboom.mp3")
pygame.mixer.music.load("assets/audio/Match_start.mp3")

volume = ui.get_setting("volume")
shoot_sound.set_volume(volume)
normal_hit_sound.set_volume(volume)
crit_hit_sound.set_volume(volume)
explosion_sound.set_volume(volume)
pygame.mixer.music.set_volume(volume)

pygame.mixer.music.play()

background = Image.new_image("assets/tiles/map1.png", pygame.Rect(0, 0, WIDTH, HEIGHT))
wall = pygame.image.load("assets/tiles/wallwall.png").convert()
wall2 = pygame.transform.smoothscale(wall, (86, 27))

scales = [(86, 27)]
wall_rects = []

for scale in scales:
    tpl = pygame.transform.smoothscale(wall, scale)
    wall_rects.extend(find_image(tpl, background.surface))

rotated_wall = pygame.transform.rotate(wall, 90)

for scale in scales:
    tpl = pygame.transform.smoothscale(rotated_wall, (scale[1], scale[0]))
    wall_rects.extend(find_image(tpl, background.surface))

world = TankWorld(*wall_rects)# + [pygame.Rect(0, 0, 100, 25)])

bullet_image = Image.new_image("assets/bullets/bullet.png", pygame.Rect(0, 0, 10, 10))

player1_image = Image.new_image("assets/tanks/Player1.png", pygame.Rect(600, 300, 30, 30), (20, 20))
player2_image = Image.new_image("assets/tanks/Player2.png", pygame.Rect(600, 300, 30, 30), (20, 20))

player1_keybinds = Keybinds(up=pygame.K_w, down=pygame.K_s, left=pygame.K_a, right=pygame.K_d, shoot=pygame.K_SPACE)
player1 = Tank(world, player1_image, player1_keybinds, 200, 500, 1.0, 1.0, bullet_image, lambda: 0.2 if random.random() < 0.3 else 0.1)

player2_keybinds = Keybinds(up=pygame.K_UP, down=pygame.K_DOWN, left=pygame.K_LEFT, right=pygame.K_RIGHT, shoot=pygame.K_RETURN)
player2 = Tank(world, player2_image, player2_keybinds, 200, 500, 1.0, 1.0, bullet_image, lambda: 0.2 if random.random() < 0.3 else 0.1)

players = [player1, player2]

other_font = pygame.font.Font("assets/fonts/SEEKUW.ttf", 100)
dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
dim.fill((50, 50, 50, 150))
countdown = 4

@screen.run
def main_loop(delta_time: float) -> Any:
    global countdown
    if countdown > 0:
        for event in pygame.event.get(): ...
        background.render(screen.surface)
        screen.surface.blit(dim, (0, 0))

        text_surf = other_font.render(f"{countdown-1}".replace("0", "Fight!"), True, (255, 255, 255))
        screen.surface.blit(text_surf, text_surf.get_rect(center=(WIDTH//2, HEIGHT//2)))

        pygame.display.flip()
        countdown -= 1
        time.sleep(1.0)
        return

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return BREAK_LOOP
    
    background.render(screen.surface)

    screen.surface.blit(wall2, (340, 115))
    pygame.draw.rect(screen.surface, (255, 0, 0), wall2.get_rect(topleft=(340, 115)), 1)

    explosions.update(delta_time)
    explosions.render(screen.surface)

    death_explosions.update(delta_time)
    death_explosions.render(screen.surface)

    for bullet in world.bullets.copy():
        if bullet.update(delta_time):
            world.bullets.remove(bullet)
        bullet.render(screen.surface)

    if player1.is_alive:
        player1.update(delta_time)
        player1.render(screen.surface)
    
    if player2.is_alive:
        player2.update(delta_time)
        player2.render(screen.surface)

    if ui.get_setting("hitboxes"):
        pygame.draw.rect(screen.surface, (0, 0, 255), player1.image.rect, 1)
        pygame.draw.rect(screen.surface, (0, 0, 255), player2.image.rect, 1)
        world.draw_boxes(screen.surface)

pygame.quit()