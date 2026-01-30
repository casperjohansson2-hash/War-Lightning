import random
import pygame




SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 920
pygame.init()


clock = pygame.time.Clock()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


ai_player = pygame.image.load("C:/War Lightning/War-Lightning/assets/sprites/tankitank.png")


sprite_ai_player = pygame.transform.scale(ai_player, (ai_player.get_width() // 2, ai_player.get_height() // 2))



ai_player_x = SCREEN_WIDTH // 2 - 120
ai_player_y = SCREEN_HEIGHT - 200

ai_player_speed = 1

target_x = random.randint(0, SCREEN_WIDTH - 100)
target_y = random.randint(0, SCREEN_HEIGHT - 100)








game_plays = True



while (game_plays == True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_plays = False

    # 2. --- AI RÖRELSE ---
    
    # Om tanken är till vänster om målet -> Åk höger
    if ai_player_x < target_x:
        ai_player_x += ai_player_speed
    # Om tanken är till höger om målet -> Åk vänster
    elif ai_player_x > target_x:
        ai_player_x -= ai_player_speed

    # Om tanken är ovanför målet -> Åk ner
    if ai_player_y < target_y:
        ai_player_y += ai_player_speed
    # Om tanken är nedanför målet -> Åk upp
    elif ai_player_y > target_y:
        ai_player_y -= ai_player_speed

    # 3. --- KOLLA OM VI ÄR FRAMME ---
    # Vi kollar avståndet (skillnaden) mellan tanken och målet
    diff_x = abs(ai_player_x - target_x)
    diff_y = abs(ai_player_y - target_y)

    # Om avståndet är litet (vi är framme), välj ett nytt mål!
    if diff_x < 5 and diff_y < 5:
        target_x = random.randint(50, SCREEN_WIDTH - 100)
        target_y = random.randint(50, SCREEN_HEIGHT - 100)

    # 4. --- RITA ALLT ---
    
    # VIKTIGT: Sudda skärmen först!
    screen.fill((0, 0, 30))

    # Rita tanken på sin nya position
    screen.blit(sprite_ai_player, (ai_player_x, ai_player_y))

    # Uppdatera skärmen
    pygame.display.update()

    # Lås spelet till 60 FPS (så den rör sig mjukt)
    clock.tick(60)

pygame.quit()