"""General purpose module. Replace the code below when you want to showcase any code. Keep it short."""

from ui import Text, get_mode
import pygame

mode = get_mode()
if mode == "exit": # In case we have to free memory (C++, C, C#, Java and a lot of other languages concerns later on in your careers guys)
    exit()

pygame.init() # Init afterwards to preserve memory intact!

WIDTH, HEIGHT = (1920, 1080)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()

pygame.display.set_caption("War Lightning")

clock = pygame.time.Clock()
target_fps = 60.0
active = True

primary_font = pygame.font.SysFont("assets/fonts/SEEKUW.ttf", 25, bold=True)

text = Text(primary_font, str(mode), (50, 50, 50)) # We can literaly use any element I have provided, guys! Enjoy.

while active:
    dt = clock.tick(target_fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    
    screen.fill((255, 255, 255))

    text.render(screen, center=screen_rect.center)

    pygame.display.flip()

pygame.quit()