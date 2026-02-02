import random
import pygame

# --- INSTÄLLNINGAR ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 920

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank War - Fixade Skott")

clock = pygame.time.Clock()

# --- BILDER ---

# 1. AI SPELARE
try:
    img_ai = pygame.image.load("C:/War Lightning/War-Lightning/assets/tanks/Player2.png")
    # Vi sparar originalstorleken för att veta mitten
    original_ai_image = pygame.transform.scale(img_ai, (img_ai.get_width(), img_ai.get_height()))
except:
    original_ai_image = pygame.Surface((50, 70))
    original_ai_image.fill((255, 0, 0)) 

current_ai_image = original_ai_image

# 2. SKOTTET
try:
    raw_bullet = pygame.image.load("C:/War Lightning/War-Lightning/assets/bullets/bullet.png")
    sprite_skott_bild = pygame.transform.scale(raw_bullet, (20, 20))
except:
    sprite_skott_bild = pygame.Surface((10, 10))
    sprite_skott_bild.fill((255, 255, 0))

# --- KLASS FÖR SKOTT ---
class AiSkott:
    def __init__(self, x, y, fart_x, fart_y):
        self.x = x
        self.y = y
        self.fart_x = fart_x 
        self.fart_y = fart_y 
        self.bild = sprite_skott_bild

    def flytta(self):
        self.x = self.x + self.fart_x
        self.y = self.y + self.fart_y

    def rita(self, screen):
        screen.blit(self.bild, (self.x, self.y))

# --- AI VARIABLER ---
ai_x = SCREEN_WIDTH // 2
ai_y = SCREEN_HEIGHT // 2
ai_speed = 4 # Lite snabbare än 1
ai_angle = 0 

target_x = random.randint(50, SCREEN_WIDTH - 100)
target_y = random.randint(50, SCREEN_HEIGHT - 100)

ai_skott_lista = []
ai_skott_räknare = 0

game_plays = True

while game_plays:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_plays = False

    # --- AI RÖRELSE ---
    
    if abs(ai_x - target_x) < 10 and abs(ai_y - target_y) < 10:
        target_x = random.randint(50, SCREEN_WIDTH - 100)
        target_y = random.randint(50, SCREEN_HEIGHT - 100)

    if abs(ai_x - target_x) > ai_speed:
        if ai_x < target_x:
            ai_x += ai_speed
            ai_angle = -90 
        elif ai_x > target_x:
            ai_x -= ai_speed
            ai_angle = 90
    elif abs(ai_y - target_y) > ai_speed:
        if ai_y < target_y:
            ai_y += ai_speed
            ai_angle = 180 
        elif ai_y > target_y:
            ai_y -= ai_speed
            ai_angle = 0

    current_ai_image = pygame.transform.rotate(original_ai_image, ai_angle)

    # --- SKJUT-LOGIK (Här är fixen!) ---
    ai_skott_räknare += 1
    
    if ai_skott_räknare > 60 and random.randint(1, 50) == 1:
        
        skott_speed = 10
        s_dx = 0
        s_dy = 0
        
        # Variabler för var skottet ska starta
        start_x = ai_x
        start_y = ai_y

        # Bestäm riktning OCH startposition
        # Siffrorna (t.ex. +20, +45) är justerade för att hamna i mitten av tanken.
        # Om det fortfarande ser snett ut, ändra dessa siffror lite!
        
        if ai_angle == 0:     # UPP
            s_dy = -skott_speed
            start_x = ai_x + 20  # Centrera i sidled
            start_y = ai_y - 10  # Lite ovanför tanken
            
        elif ai_angle == 180: # NER
            s_dy = skott_speed
            start_x = ai_x + 28  # Centrera i sidled (roterade bilder flyttar sig ibland lite)
            start_y = ai_y + 50  # Nedanför tanken
            
        elif ai_angle == 90:  # VÄNSTER
            s_dx = -skott_speed
            start_x = ai_x - 10  # Till vänster om tanken
            start_y = ai_y + 28  # Centrera i höjdled
            
        elif ai_angle == -90: # HÖGER
            s_dx = skott_speed
            start_x = ai_x + 50  # Till höger om tanken
            start_y = ai_y + 20  # Centrera i höjdled

        # Skapa skottet med de nya start-koordinaterna
        nytt_skott = AiSkott(start_x, start_y, s_dx, s_dy)
        ai_skott_lista.append(nytt_skott)
        ai_skott_räknare = 0

    # --- UPPDATERA SKOTT ---
    for skott in reversed(ai_skott_lista):
        skott.flytta()
        skott.rita(screen)
        if skott.x < -50 or skott.x > SCREEN_WIDTH + 50 or skott.y < -50 or skott.y > SCREEN_HEIGHT + 50:
            ai_skott_lista.remove(skott)

    # --- RITA ---
    screen.fill((0, 0, 30))
    
    screen.blit(current_ai_image, (ai_x, ai_y))
    
    # Rita skotten OVANPÅ tanken om de precis skapats
    for skott in ai_skott_lista:
        skott.rita(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()