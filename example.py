"""General purpose module. Replace the code below when you want to showcase any code. Keep it short."""

from ui import Text, get_mode, stop_loading
import pygame

mode = get_mode() # Automatically stops loading-screen
if mode == "exit": # In case we have to free memory (C++, C, C#, Java and a lot of other languages concerns later on in your careers guys)
    stop_loading()
    exit()

WIDTH, HEIGHT = (1920, 1080) # Define width and height as the first thing you do. You won't have any screen until everything below is loaded.

clock = pygame.time.Clock()
target_fps = 60.0
active = True

primary_font = pygame.font.SysFont("assets/fonts/SEEKUW.ttf", 25, bold=True)

text = Text(primary_font, str(mode), (50, 50, 50)) # We can literaly use any element I have provided, guys! Enjoy.

# Be aware that loading is a really cool effect, but oftentimes the computer loads resources to fast to see the loading-screen.
# Although the game should actually be loading for some milliseconds longer, that might actually be seen.
stop_loading() # Only now stop loading.
pygame.display.init() # Only reinitialize the screen

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Create the window as the last thing you do. Now the menu will load until the game is actually ready.
screen_rect = screen.get_rect()

pygame.display.set_caption("War Lightning")

while active:
    dt = clock.tick(target_fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    
    screen.fill((255, 255, 255))

    text.render(screen, center=screen_rect.center)

    pygame.display.flip()

pygame.quit()