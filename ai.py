import random
import pygame

# --- INSTÄLLNINGAR ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank War - Du mot AI")

clock = pygame.time.Clock()


# --- BILDER ---

# 1. DIN TANK (SPELAREN)
try:
    # Vi testar att ladda från sprites-mappen
    img_p1 = pygame.image.load("C:/War Lightning/assets/tanks/Player1.png")
    original_p1_image = pygame.transform.scale(img_p1, (img_p1.get_width(), img_p1.get_height()))
except:
    original_p1_image = pygame.Surface((50, 70))
    original_p1_image.fill((0, 255, 0)) # Grön

current_p1_image = original_p1_image

# 2. AI TANK (FIENDEN)
try:
    img_ai = pygame.image.load("C:/War Lightning/assets/tanks/Player2.png")
    original_ai_image = pygame.transform.scale(img_ai, (img_ai.get_width(), img_ai.get_height()))
except:
    original_ai_image = pygame.Surface((50, 70))
    original_ai_image.fill((255, 0, 0)) # Röd

current_ai_image = original_ai_image

map_1 = pygame.image.load("C:/War Lightning/assets/tiles/map1.png")
background = pygame.transform.smoothscale(map_1, (SCREEN_WIDTH, SCREEN_HEIGHT))


# 3. SKOTTET
try:
    raw_bullet = pygame.image.load("C:/War Lightning/assets/bullets/bullet.png")
    sprite_skott_bild = pygame.transform.scale(raw_bullet, (20, 20))
except:
    sprite_skott_bild = pygame.Surface((20, 20))
    sprite_skott_bild.fill((255, 255, 0))

# --- GEMENSAM KLASS FÖR SKOTT ---
class Bullet:
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

# --- SPELARENS VARIABLER ---
p1_x = 200
p1_y = 200
p1_speed = 2
p1_angle = 0  # Håller koll på vilket håll du tittar åt

p1_skott_lista = []
p1_skott_delay = 0 # För att inte spam-skjuta
p1_cooldown = 20   # Hur snabbt du kan skjuta

# --- AI VARIABLER ---
ai_x = SCREEN_WIDTH - 200
ai_y = SCREEN_HEIGHT - 200
ai_speed = 1
ai_angle = 0 

ai_skott_lista = []
ai_skott_räknare = 0


walls = [
    pygame.Rect(796, 24, 28, 86),
    pygame.Rect(794, 169, 28, 86),
    pygame.Rect(794, 336, 28, 86),
    pygame.Rect(822, 394, 172, 28),
    pygame.Rect(880, 730, 172, 28),
    pygame.Rect(794, 504, 28, 86),
    pygame.Rect(795, 672, 28, 86),
    pygame.Rect(794, 862, 28, 86),
    pygame.Rect(1135, 24, 28, 86),
    pygame.Rect(1135, 169, 28, 86),
    pygame.Rect(1135, 336, 28, 86),
    pygame.Rect(1135, 504, 28, 86),
    pygame.Rect(1136, 672, 28, 86),
    pygame.Rect(1105, 842, 28, 86),
    pygame.Rect(1190, 815, 86, 28),
    pygame.Rect(1360, 815, 86, 28),
    pygame.Rect(1530, 815, 86, 28),
    pygame.Rect(1020, 815, 86, 28),
    pygame.Rect(850, 815, 86, 28),
    pygame.Rect(680, 815, 86, 28),
    pygame.Rect(510, 815, 86, 28),
    pygame.Rect(340, 815, 86, 28),
    pygame.Rect(424, 891, 86, 28),
    pygame.Rect(596, 891, 86, 28),
    pygame.Rect(1274, 891, 86, 28),
    pygame.Rect(1444, 891, 86, 28),
    pygame.Rect(1335, 420, 28, 86),
    pygame.Rect(1420, 250, 28, 86),
    pygame.Rect(1425, 672, 28, 86),
    pygame.Rect(480, 420, 28, 86),
    pygame.Rect(510, 252, 28, 86),
    pygame.Rect(510, 672, 28, 86),
    pygame.Rect(314, 506, 28, 86),
    pygame.Rect(1582, 505, 28, 86),
    pygame.Rect(-1, 479, 172, 28),
    pygame.Rect(-1, 588, 172, 28),
    pygame.Rect(1747, 479, 172, 28),
    pygame.Rect(1747, 588, 172, 28),
    pygame.Rect(1590, 24, 28, 86),
    pygame.Rect(254, 24, 28, 86),
    pygame.Rect(340, 141, 86, 28),
    pygame.Rect(1445, 141, 86, 28),
    pygame.Rect(1020, 970, 28, 86),
    pygame.Rect(909, 970, 28, 86),
    pygame.Rect(267, 970, 28, 86),
    pygame.Rect(0, 0, SCREEN_WIDTH, 28),
    pygame.Rect(SCREEN_WIDTH - 27, 0, 28, SCREEN_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT - 27, SCREEN_WIDTH, 28),
    pygame.Rect(-1, 0, 28, SCREEN_HEIGHT),
        ]   













game_plays = True

while game_plays:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_plays = False

    # ==========================
    # 1. STYR SPELAREN (WASD)
    # ==========================
    keys = pygame.key.get_pressed()
    
    
    
    # Vi sparar om vi rör oss för att veta vilken bild vi ska visa
    moving = False

    if keys[pygame.K_a]: # Vänster
        p1_x -= p1_speed
        p1_angle = 90
        moving = True
    elif keys[pygame.K_d]: # Höger
        p1_x += p1_speed
        p1_angle = -90
        moving = True
    elif keys[pygame.K_w]: # Upp
        p1_y -= p1_speed
        p1_angle = 0
        moving = True
    elif keys[pygame.K_s]: # Ner
        p1_y += p1_speed
        p1_angle = 180
        moving = True
    
    # Uppdatera spelarens bildrotation
    current_p1_image = pygame.transform.rotate(original_p1_image, p1_angle)

    # --- SPELAREN SKJUTER (SPACE) ---
    if p1_skott_delay > 0:
        p1_skott_delay -= 1

    if keys[pygame.K_SPACE] and p1_skott_delay == 0:
        p1_skott_delay = p1_cooldown # Återställ timer
        
        skott_speed = 12
        s_dx = 0
        s_dy = 0
        
        # Matematik för att hitta mitten på DIN tank
        p_center_x = p1_x + current_p1_image.get_width() // 2
        p_center_y = p1_y + current_p1_image.get_height() // 2
        bullet_offset = sprite_skott_bild.get_width() // 2
        
        start_x = 0
        start_y = 0

        # Samma logik som för AI men för dig
        if p1_angle == 0:     # UPP
            s_dy = -skott_speed
            start_x = p_center_x - bullet_offset
            start_y = p1_y - 20
        elif p1_angle == 180: # NER
            s_dy = skott_speed
            start_x = p_center_x - bullet_offset
            start_y = p1_y + current_p1_image.get_height()
        elif p1_angle == 90:  # VÄNSTER
            s_dx = -skott_speed
            start_x = p1_x - 20
            start_y = p_center_y - bullet_offset
        elif p1_angle == -90: # HÖGER
            s_dx = skott_speed
            start_x = p1_x + current_p1_image.get_width()
            start_y = p_center_y - bullet_offset

        p1_skott_lista.append(Bullet(start_x, start_y, s_dx, s_dy))


    # ==========================
    # 2. AI LOGIK (JAGA DIG)
    # ==========================
    
    # AI:n siktar nu på dig (p1_x, p1_y) istället för slumpen
    target_x = p1_x
    target_y = p1_y
    
    # Rörelse
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

    # --- AI SKJUTER ---
    ai_skott_räknare += 1
    
    # Skjuter var 60:e frame (ca 1 sekund) om den är nära
    dist_x = abs(ai_x - p1_x)
    dist_y = abs(ai_y - p1_y)
    
    if ai_skott_räknare > 60 and (dist_x + dist_y) < 600:
        
        skott_speed = 10
        s_dx = 0
        s_dy = 0
        
        # Matematik för att hitta mitten på AI tank
        ai_center_x = ai_x + current_ai_image.get_width() // 2
        ai_center_y = ai_y + current_ai_image.get_height() // 2
        bullet_offset = sprite_skott_bild.get_width() // 2

        start_x = 0
        start_y = 0

        if ai_angle == 0:     # UPP
            s_dy = -skott_speed
            start_x = ai_center_x - bullet_offset
            start_y = ai_y - 20
        elif ai_angle == 180: # NER
            s_dy = skott_speed
            start_x = ai_center_x - bullet_offset
            start_y = ai_y + current_ai_image.get_height()
        elif ai_angle == 90:  # VÄNSTER
            s_dx = -skott_speed
            start_x = ai_x - 20
            start_y = ai_center_y - bullet_offset
        elif ai_angle == -90: # HÖGER
            s_dx = skott_speed
            start_x = ai_x + current_ai_image.get_width()
            start_y = ai_center_y - bullet_offset

        ai_skott_lista.append(Bullet(start_x, start_y, s_dx, s_dy))
        ai_skott_räknare = 0

    # ==========================
    # 3. UPPDATERA SKOTT
    # ==========================
    
    # Uppdatera DINA skott
    for skott in reversed(p1_skott_lista):
        skott.flytta()
        if skott.x < -50 or skott.x > SCREEN_WIDTH or skott.y < -50 or skott.y > SCREEN_HEIGHT:
            p1_skott_lista.remove(skott)

    # Uppdatera AI skott
    for skott in reversed(ai_skott_lista):
        skott.flytta()
        if skott.x < -50 or skott.x > SCREEN_WIDTH or skott.y < -50 or skott.y > SCREEN_HEIGHT:
            ai_skott_lista.remove(skott)


    # ==========================
    # 4. RITA ALLT
    # ==========================
    screen.blit(background, (0, 0))
    
    # Rita tankarna
    screen.blit(current_p1_image, (p1_x, p1_y))
    screen.blit(current_ai_image, (ai_x, ai_y))
    
    # Rita alla skott
    for skott in p1_skott_lista:
        skott.rita(screen)
        
    for skott in ai_skott_lista:
        skott.rita(screen)


    


    pygame.display.update()
    clock.tick(60)

pygame.quit()