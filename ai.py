import random
import pygame


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 920

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank War - AI Player 2")

clock = pygame.time.Clock()

#    AI Tankens Grafik
raw_image = pygame.image.load("C:/War Lightning/assets/tanks/Player2.png")

original_ai_player = pygame.transform.scale(raw_image, (raw_image.get_width(), raw_image.get_height()))

current_image = original_ai_player

ai_player_x = SCREEN_WIDTH // 2 - 120
ai_player_y = SCREEN_HEIGHT - 200
ai_player_speed = 1

current_angle = 0 

#    AI Tankens Mål
target_x = random.randint(50, SCREEN_WIDTH - 100)
target_y = random.randint(50, SCREEN_HEIGHT - 100)

game_plays = True

while game_plays:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_plays = False

    #    RÖRELSE
    moving_x = False 

    if abs(ai_player_x - target_x) > ai_player_speed:
        moving_x = True
        if ai_player_x < target_x:
            ai_player_x += ai_player_speed
            current_angle = -90 
        elif ai_player_x > target_x:
            ai_player_x -= ai_player_speed
            current_angle = 90
            
    elif abs(ai_player_y - target_y) > ai_player_speed:
        if ai_player_y < target_y:
            ai_player_y += ai_player_speed
            current_angle = 180 
        elif ai_player_y > target_y:
            ai_player_y -= ai_player_speed
            current_angle = 0

    #     ROTATION
    current_image = pygame.transform.rotate(original_ai_player, current_angle)

    #     KOLLA AVSTÅND
    diff_x = abs(ai_player_x - target_x)
    diff_y = abs(ai_player_y - target_y)

    if diff_x < 10 and diff_y < 10:
        target_x = random.randint(50, SCREEN_WIDTH - 100)
        target_y = random.randint(50, SCREEN_HEIGHT - 100)

    #    Rita ut sakerna på skärmen
    screen.fill((0, 0, 30))
    screen.blit(current_image, (ai_player_x, ai_player_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()