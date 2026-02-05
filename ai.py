whole_game = True

import random
import time
import pygame
import ui
import math

while whole_game:
    pygame.init()
    
    # --- LJUD ---
    try:
        shot = pygame.mixer.Sound("C:/War Lightning/assets/audio/Tank shot.mp3")
        normal_hit = pygame.mixer.Sound("C:/War Lightning/assets/audio/Metal hit.mp3")
        crit_hit = pygame.mixer.Sound("C:/War Lightning/assets/audio/Metal pierce.mp3")
        dead = pygame.mixer.Sound("C:/War Lightning/assets/audio/Tank kaboom.mp3")
        pygame.mixer.music.load("assets/audio/Match start.mp3")
        pygame.mixer.music.play()
        volume = ui.get_setting("volume")
        pygame.mixer.music.set_volume(volume)
    except:
        pass

    color_list = [(255, 50, 50), (255, 150, 50), (255, 255, 50)]
    explosions = []

    if ui.get_mode() == "exit":
        pygame.quit()
        exit()
        whole_game = False
    else:
        #Skärm inställningar
        width = 1920
        height = 1080
        player_health = 100
        center_y = height // 2
        center_x = width // 2
        
        # --- BILDER ---
        try:
            original_background1 = pygame.image.load("C:/War Lightning/assets/tiles/map1.png")
            original_background2 = pygame.image.load("C:/War Lightning/assets/tiles/map2.png")
            original_bullet = pygame.image.load("C:/War Lightning/assets/bullets/bullet.png")
            original_player1 = pygame.image.load("C:/War Lightning/assets/tanks/Player1.png")
            original_player2 = pygame.image.load("C:/War Lightning/assets/tanks/Player2.png")
        except:
            original_background1 = pygame.Surface((width, height))
            original_background2 = pygame.Surface((width, height))
            original_bullet = pygame.Surface((10, 10))
            original_player1 = pygame.Surface((50, 50))
            original_player1.fill((0, 255, 0))
            original_player2 = pygame.Surface((50, 50))
            original_player2.fill((255, 0, 0))
        
        background1 = pygame.transform.smoothscale(original_background1, (width, height))
        background2 = pygame.transform.smoothscale(original_background2, (width, height))
        sprite_bullet = pygame.transform.smoothscale(original_bullet, (original_bullet.get_width() + 1, original_bullet.get_height() + 1))
        sprite_player1 = pygame.transform.smoothscale(original_player1, (original_player1.get_width(), original_player1.get_height()))
        sprite_player2 = pygame.transform.smoothscale(original_player2, (original_player2.get_width(), original_player2.get_height()))
        
        clock = pygame.time.Clock()
        game = True
        maps = [background1, background2]
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("War Lightning")
        
        def damage():
            chans = random.randint(1, 3)
            if chans == 1:
                player_damage = 20
                crit_hit.play()
            else:
                player_damage = 10
                normal_hit.play()
            return player_damage
        
        # --- KLASSER ---
        class Particle:
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.lifetime = random.randint(20, 40)
                self.speed_x = random.uniform(-2, 2)
                self.speed_y = random.uniform(-2, 2)
                self.radius = random.randint(1, 3)
                self.color = random.choice(color_list)

            def update(self):
                self.x += self.speed_x
                self.y += self.speed_y
                self.lifetime -= 1

            def draw(self, screen):
                if self.lifetime > 0:
                    pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        class Bullet:
            def __init__(self, x, y, direction):
                self.x = x
                self.y = y
                self.speed = 20
                self.bild = sprite_bullet
                self.direction = direction
                self.collision_rectangle = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())
                
                if self.direction == "LEFT":
                    self.bild = pygame.transform.rotate(sprite_bullet, 90)
                elif self.direction == "DOWN":
                    self.bild = pygame.transform.rotate(sprite_bullet, 180)
                elif self.direction == "RIGHT":
                    self.bild = pygame.transform.rotate(sprite_bullet, -90)

            def move(self):
                if self.direction == "UP": self.y -= self.speed
                elif self.direction == "DOWN": self.y += self.speed
                elif self.direction == "LEFT": self.x -= self.speed
                elif self.direction == "RIGHT": self.x += self.speed
                self.collision_rectangle.topleft = (self.x, self.y)

            def draw(self, screen):
                if self.direction == "UP" or self.direction == "DOWN":
                    screen.blit(self.bild, (self.x + 8, self.y))
                else:
                    screen.blit(self.bild, (self.x, self.y + 28))

        # --- PLAYER 1 KLASS (Används av alla, men hastighet sätts olika) ---
        class Player1:
            def __init__(self, speed_val):
                self.player1_x = 30
                self.player1_y = (height // 2) - 20
                self.sprite_player1 = sprite_player1
                self.health = player_health
                self.damage = damage()
                self.speed = speed_val # HÄR SÄTTS HASTIGHETEN
                self.original_image = sprite_player1
                self.sprite_player1 = self.original_image
                self.direction = "UP"
                self.exploded = False
                hitbox_width = self.sprite_player1.get_width() - 25
                hitbox_height = self.sprite_player1.get_height() - 25
                self.offset_x = (self.sprite_player1.get_width() - hitbox_width) // 2
                self.offset_y = (self.sprite_player1.get_height() - hitbox_height) // 2
                self.collision_rectangle = pygame.Rect(self.player1_x + self.offset_x, self.player1_y + self.offset_y, hitbox_width, hitbox_height)
                self.sprite_player1 = pygame.transform.rotate(self.original_image, 270)

            def move(self, walls):
                keys = pygame.key.get_pressed()
                dx = 0
                dy = 0
                if keys[pygame.K_w] and self.health > 0:
                    dy = -self.speed
                    self.sprite_player1 = pygame.transform.rotate(self.original_image, 0)
                    self.direction = "UP"
                elif keys[pygame.K_s] and self.health > 0:
                    dy = self.speed
                    self.sprite_player1 = pygame.transform.rotate(self.original_image, 180)
                    self.direction = "DOWN"
                elif keys[pygame.K_a] and self.health > 0:
                    dx = -self.speed
                    self.sprite_player1 = pygame.transform.rotate(self.original_image, 90)
                    self.direction = "LEFT"
                elif keys[pygame.K_d] and self.health > 0:
                    dx = self.speed
                    self.sprite_player1 = pygame.transform.rotate(self.original_image, 270)
                    self.direction = "RIGHT"
                
                self.player1_x += dx
                self.collision_rectangle.x = self.player1_x + self.offset_x
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if dx > 0: self.collision_rectangle.right = wall.left
                        if dx < 0: self.collision_rectangle.left = wall.right
                        self.player1_x = self.collision_rectangle.x - self.offset_x
                self.player1_y += dy
                self.collision_rectangle.y = self.player1_y + self.offset_y
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if dy > 0: self.collision_rectangle.bottom = wall.top
                        if dy < 0: self.collision_rectangle.top = wall.bottom
                        self.player1_y = self.collision_rectangle.y - self.offset_y
                self.collision_rectangle.topleft = (self.player1_x + self.offset_x, self.player1_y + self.offset_y)

            def draw(self, screen):
                if not self.exploded:
                    screen.blit(self.sprite_player1, (self.player1_x, self.player1_y))
                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (0, 0, 255), self.collision_rectangle, 2)
            
            def collide(self, bullet_rect):
                if not self.exploded:
                    if self.collision_rectangle.colliderect(bullet_rect):
                        if ui.get_setting("particles"):
                            explosions.append([Particle(self.player1_x + 34, self.player1_y + 30) for _ in range(100)])
                        self.health -= damage()
                        return True
                return False

        # --- SETUP UI & VÄGGAR ---
        primary_font = pygame.font.Font("assets/fonts/SEEKUW.ttf", 20)
        other_font = pygame.font.Font("assets/fonts/SEEKUW.ttf", 100)
        dim = pygame.Surface((width, height), pygame.SRCALPHA)
        dim.fill((50, 50, 50, 150))
        countdown = 4

        if ui.get_map() == "Idrilyn": background = background1
        elif ui.get_map() == "Nebrodu": background = background2
        elif ui.get_map() == "Random": background = random.choice(maps)

        if background == background1:
            walls = [pygame.Rect(796, 24, 28, 86), pygame.Rect(794, 169, 28, 86), pygame.Rect(794, 336, 28, 86), pygame.Rect(822, 394, 172, 28), pygame.Rect(880, 730, 172, 28), pygame.Rect(794, 504, 28, 86), pygame.Rect(795, 672, 28, 86), pygame.Rect(794, 862, 28, 86), pygame.Rect(1135, 24, 28, 86), pygame.Rect(1135, 169, 28, 86), pygame.Rect(1135, 336, 28, 86), pygame.Rect(1135, 504, 28, 86), pygame.Rect(1136, 672, 28, 86), pygame.Rect(1105, 842, 28, 86), pygame.Rect(1190, 815, 86, 28), pygame.Rect(1360, 815, 86, 28), pygame.Rect(1530, 815, 86, 28), pygame.Rect(1020, 815, 86, 28), pygame.Rect(850, 815, 86, 28), pygame.Rect(680, 815, 86, 28), pygame.Rect(510, 815, 86, 28), pygame.Rect(340, 815, 86, 28), pygame.Rect(424, 891, 86, 28), pygame.Rect(596, 891, 86, 28), pygame.Rect(1274, 891, 86, 28), pygame.Rect(1444, 891, 86, 28), pygame.Rect(1335, 420, 28, 86), pygame.Rect(1420, 250, 28, 86), pygame.Rect(1425, 672, 28, 86), pygame.Rect(480, 420, 28, 86), pygame.Rect(510, 252, 28, 86), pygame.Rect(510, 672, 28, 86), pygame.Rect(314, 506, 28, 86), pygame.Rect(1582, 505, 28, 86), pygame.Rect(-1, 479, 172, 28), pygame.Rect(-1, 588, 172, 28), pygame.Rect(1747, 479, 172, 28), pygame.Rect(1747, 588, 172, 28), pygame.Rect(1590, 24, 28, 86), pygame.Rect(254, 24, 28, 86), pygame.Rect(340, 141, 86, 28), pygame.Rect(1445, 141, 86, 28), pygame.Rect(1020, 970, 28, 86), pygame.Rect(909, 970, 28, 86), pygame.Rect(267, 970, 28, 86), pygame.Rect(0, 0, width, 28), pygame.Rect(width - 27, 0, 28, height), pygame.Rect(0, height - 27, width, 28), pygame.Rect(-1, 0, 28, height)]
        elif background == background2:
            walls = [pygame.Rect(0, 0, width, 28), pygame.Rect(width - 27, 0, 28, height), pygame.Rect(0, height - 27, width, 28), pygame.Rect(-1, 0, 28, height)]   

        original_hp_bar_back = pygame.image.load("assets/ui/hp_bar_back.png")
        original_hp_bar_health = pygame.image.load("assets/ui/hp_bar_health.png")
        original_hp_bar_overlay = pygame.image.load("assets/ui/hp_bar_overlay.png")
        hp_bar_back = pygame.transform.smoothscale(original_hp_bar_back, (215, 50))
        hp_bar_overlay = pygame.transform.smoothscale(original_hp_bar_overlay, (215, 50))
        hp_bar_health1 = pygame.transform.smoothscale(original_hp_bar_health, (215, 50))
        hp_bar_health2 = pygame.transform.smoothscale(original_hp_bar_health, (215, 50))
        hp_bar_rect1 = pygame.Rect(10, 10, 215, 50)
        hp_bar_rect2 = pygame.Rect(width-225, 10, 215, 50)
        last_health1 = 100
        last_health2 = 100

        bullet_counter1 = 0
        bullet_counter2 = 0
        bullet_list1 = []
        bullet_list2 = []

        # =====================================================================
        # SOLO MODE (Mot AI) - UPPDATERAD MED SMART AI (INGA DIAGONALER/FASTNA)
        # =====================================================================
        if ui.get_mode() == "solo":
            player_1 = Player1(speed_val=2) # SPELARENS HASTIGHET ÄR 2
            
            class Player2:
                def __init__(self):
                    self.player2_x = width - 90
                    self.player2_y = (height // 2) - 20
                    self.health = player_health
                    self.damage = damage()
                    self.speed = 1 # AI HASTIGHET ÄR 1
                    self.direction = "UP"
                    self.exploded = False
                    self.original_image = sprite_player2
                    self.sprite_player2 = self.original_image
                    hitbox_width = self.sprite_player2.get_width() - 25
                    hitbox_height = self.sprite_player2.get_height() - 25
                    self.offset_x = (self.sprite_player2.get_width() - hitbox_width) // 2
                    self.offset_y = (self.sprite_player2.get_height() - hitbox_height) // 2
                    self.collision_rectangle = pygame.Rect(self.player2_x + self.offset_x, self.player2_y + self.offset_y, hitbox_width, hitbox_height)
                    
                    self.patrol_target_x = random.randint(50, width - 50)
                    self.patrol_target_y = random.randint(50, height - 50)
                    self.mode = "PATROL" 
                    self.patrol_timer = 0 

                def move(self, walls, target_player_x, target_player_y):
                    if self.health <= 0: return

                    # 1. VÄLJ MÅL
                    dist_to_player_x = self.player2_x - target_player_x
                    dist_to_player_y = self.player2_y - target_player_y
                    total_distance = math.sqrt(dist_to_player_x**2 + dist_to_player_y**2)

                    if total_distance < 500: # JAGA
                        self.mode = "CHASE"
                        target_x = target_player_x
                        target_y = target_player_y
                        self.patrol_timer = 0 
                    else: # PATRULLERA
                        self.mode = "PATROL"
                        target_x = self.patrol_target_x
                        target_y = self.patrol_target_y
                        self.patrol_timer += 1
                        arrived = abs(self.player2_x - self.patrol_target_x) < 60 and abs(self.player2_y - self.patrol_target_y) < 60
                        
                        if arrived or self.patrol_timer > 180:
                            self.patrol_target_x = random.randint(50, width - 50)
                            self.patrol_target_y = random.randint(50, height - 50)
                            self.patrol_timer = 0 

                    # 2. RÖRELSE - MED TRÖGHET (INGEN SICK-SACK)
                    diff_x = target_x - self.player2_x
                    diff_y = target_y - self.player2_y
                    
                    bias_x = 0
                    bias_y = 0
                    # Om vi redan åker i en riktning, fortsätt hellre än att byta hela tiden
                    if self.direction in ["LEFT", "RIGHT"]: bias_x = 60 
                    if self.direction in ["UP", "DOWN"]: bias_y = 60    
                    
                    moves_to_try = []
                    if abs(diff_x) + bias_x > abs(diff_y) + bias_y:
                        moves_to_try = [("X", diff_x), ("Y", diff_y)]
                    else:
                        moves_to_try = [("Y", diff_y), ("X", diff_x)]

                    moved_successfully = False
                    
                    for axis, value in moves_to_try:
                        if moved_successfully: break 
                        if abs(value) < 5: continue 

                        test_dx = 0
                        test_dy = 0
                        dir_str = ""
                        angle = 0
                        
                        if axis == "X":
                            if value > 0: test_dx = self.speed; dir_str = "RIGHT"; angle = 270
                            else: test_dx = -self.speed; dir_str = "LEFT"; angle = 90
                        else: 
                            if value > 0: test_dy = self.speed; dir_str = "DOWN"; angle = 180
                            else: test_dy = -self.speed; dir_str = "UP"; angle = 0
                        
                        # Flytta och kolla krock
                        self.player2_x += test_dx
                        self.player2_y += test_dy
                        self.collision_rectangle.x = self.player2_x + self.offset_x
                        self.collision_rectangle.y = self.player2_y + self.offset_y
                        
                        hit = False
                        for wall in walls:
                            if self.collision_rectangle.colliderect(wall):
                                hit = True
                                # Backa tillbaka
                                self.player2_x -= test_dx
                                self.player2_y -= test_dy
                                self.collision_rectangle.x = self.player2_x + self.offset_x
                                self.collision_rectangle.y = self.player2_y + self.offset_y
                                break 
                        
                        if not hit:
                            self.direction = dir_str
                            self.sprite_player2 = pygame.transform.rotate(self.original_image, angle)
                            moved_successfully = True

                    # 3. OM FAST I PATRULL -> BYT MÅL
                    if not moved_successfully and self.mode == "PATROL":
                        self.patrol_timer += 50

                def draw(self, screen):
                    if not self.exploded:
                        screen.blit(self.sprite_player2, (self.player2_x, self.player2_y))
                        if ui.get_setting("hitboxes"):
                            pygame.draw.rect(screen, (0, 0, 255), self.collision_rectangle, 2)

                def collide(self, bullet_rect):
                    if not self.exploded:
                        if self.collision_rectangle.colliderect(bullet_rect):
                            if ui.get_setting("particles"):
                                explosions.append([Particle(self.player2_x + 34, self.player2_y + 30) for _ in range(100)])
                            self.health -= damage()
                            return True
                    return False

            player_2 = Player2()

            while game:
                if countdown > 0:
                    for event in pygame.event.get(): 
                        if event.type == pygame.QUIT: game = False
                    screen.blit(background, (0, 0))
                    screen.blit(dim, (0, 0))
                    text_surf = other_font.render(f"{countdown-1}".replace("0", "Fight!"), True, (255, 255, 255))
                    screen.blit(text_surf, text_surf.get_rect(center=(width//2, height//2)))
                    pygame.display.flip()
                    countdown -= 1
                    time.sleep(1.0)
                    continue
                
                player_1.move(walls)
                player_2.move(walls, player_1.player1_x, player_1.player1_y) 

                screen.blit(background, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game = False
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and player_1.exploded == False:
                    if (bullet_counter1 > 20):
                        shot.play()
                        bullet_list1.append(Bullet(player_1.player1_x + 20, player_1.player1_y, player_1.direction))
                        bullet_counter1 = 0

                dist_x = abs(player_1.player1_x - player_2.player2_x)
                dist_y = abs(player_1.player1_y - player_2.player2_y)
                if not player_2.exploded and bullet_counter2 > 40 and (dist_x + dist_y) < 600:
                    shot.play()
                    bx, by = player_2.player2_x, player_2.player2_y
                    if player_2.direction == "UP": bx += 20; by -= 10
                    elif player_2.direction == "DOWN": bx += 20; by += 40
                    elif player_2.direction == "LEFT": bx -= 10; by += 20
                    elif player_2.direction == "RIGHT": bx += 40; by += 20
                    bullet_list2.append(Bullet(bx, by, player_2.direction))
                    bullet_counter2 = 0

                if player_1.health <= 0:
                    player_1.exploded = True
                    dead.play()
                    if ui.get_setting("particles"):
                        explosions.append([Particle(player_1.player1_x, player_1.player1_y) for _ in range(100)])
                    player_1.health = 100
                    player_2.health = 100

                if player_2.health <= 0:
                    player_2.exploded = True
                    dead.play()
                    player_1.health = 100
                    player_2.health = 100

                clock.tick(60)
                bullet_counter1 += 0.5
                bullet_counter2 += 0.3 

                for wall in walls:
                    pygame.draw.rect(screen, (255, 0, 0), wall, 1)

                if player_1.health < last_health1:
                    last_health1 = player_1.health
                    hp_bar_health1 = hp_bar_health1.subsurface(pygame.Rect(0, 0, max(int(225 * (player_1.health / 100)), 1), hp_bar_rect1.height))
                if player_2.health < last_health2:
                    last_health2 = player_2.health
                    hp_bar_health2 = hp_bar_health2.subsurface(pygame.Rect(0, 0, max(int(225 * (player_2.health / 100)), 1), hp_bar_rect2.height))

                screen.blit(hp_bar_back, hp_bar_rect1)
                screen.blit(hp_bar_health1, hp_bar_rect1)
                text_surf = primary_font.render(f"{max(player_1.health, 0)} HP", True, (255, 255, 255))
                screen.blit(text_surf, text_surf.get_rect(center=hp_bar_rect1.center))
                screen.blit(hp_bar_overlay, hp_bar_rect1)
                screen.blit(hp_bar_back, hp_bar_rect2)
                screen.blit(hp_bar_health2, hp_bar_rect2)
                text_surf = primary_font.render(f"{max(player_2.health, 0)} HP", True, (255, 255, 255))
                screen.blit(text_surf, text_surf.get_rect(center=hp_bar_rect2.center))
                screen.blit(hp_bar_overlay, hp_bar_rect2)

                player_1.draw(screen)
                player_2.draw(screen)

                for bullet in reversed(bullet_list1):
                    bullet.move()
                    bullet.draw(screen)
                    hit_wall = False
                    for wall in walls:
                        if bullet.collision_rectangle.colliderect(wall): hit_wall = True
                    if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980 or hit_wall:
                        bullet_list1.remove(bullet)
                        if hit_wall and ui.get_setting("particles"):
                            explosions.append([Particle(bullet.x, bullet.y) for _ in range(100)])
                    elif player_2.collide(bullet.collision_rectangle):
                        bullet_list1.remove(bullet)

                for bullet in reversed(bullet_list2):
                    bullet.move()
                    bullet.draw(screen)
                    hit_wall = False
                    for wall in walls:
                        if bullet.collision_rectangle.colliderect(wall): hit_wall = True
                    if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980 or hit_wall:
                        bullet_list2.remove(bullet)
                        if hit_wall and ui.get_setting("particles"):
                            explosions.append([Particle(bullet.x, bullet.y) for _ in range(100)])
                    elif player_1.collide(bullet.collision_rectangle):
                        bullet_list2.remove(bullet)
                
                for explosion in explosions:
                    for particle in explosion:
                        particle.update()
                        particle.draw(screen)
                explosions = [[p for p in explosion if p.lifetime > 0] for explosion in explosions]
                explosions = [e for e in explosions if len(e) > 0]
                pygame.display.flip()
            pygame.quit()

        # =====================================================================
        # VS MODE - NORMAL HASTIGHET (1) FÖR BÅDA
        # =====================================================================
        elif ui.get_mode() == "vs":
            player_1 = Player1(speed_val=1)
            
            class Player2:
                def __init__(self):
                    self.player2_x = width - 90
                    self.player2_y = (height // 2) - 20
                    self.sprite_player2 = sprite_player2
                    self.health = player_health
                    self.damage = damage()
                    self.speed = 1 # VS HASTIGHET ÄR 1
                    self.direction = "UP"
                    self.exploded = False
                    self.original_image = sprite_player2
                    self.sprite_player2 = self.original_image
                    hitbox_width = self.sprite_player2.get_width() - 25
                    hitbox_height = self.sprite_player2.get_height() - 25
                    self.offset_x = (self.sprite_player2.get_width() - hitbox_width) // 2
                    self.offset_y = (self.sprite_player2.get_height() - hitbox_height) // 2
                    self.collision_rectangle = pygame.Rect(self.player2_x + self.offset_x, self.player2_y + self.offset_y, hitbox_width, hitbox_height)

                def move(self, walls):
                    keys = pygame.key.get_pressed()
                    dx = 0
                    dy = 0
                    if keys[pygame.K_UP] and self.health > 0:
                        dy = -self.speed
                        self.sprite_player2 = pygame.transform.rotate(self.original_image, 0)
                        self.direction = "UP"
                    elif keys[pygame.K_DOWN] and self.health > 0:
                        dy = self.speed
                        self.sprite_player2 = pygame.transform.rotate(self.original_image, 180)
                        self.direction = "DOWN"
                    elif keys[pygame.K_LEFT] and self.health > 0:
                        dx = -self.speed
                        self.sprite_player2 = pygame.transform.rotate(self.original_image, 90)
                        self.direction = "LEFT"
                    elif keys[pygame.K_RIGHT] and self.health > 0:
                        dx = self.speed
                        self.sprite_player2 = pygame.transform.rotate(self.original_image, 270)
                        self.direction = "RIGHT"
                    
                    self.player2_x += dx
                    self.collision_rectangle.x = self.player2_x + self.offset_x
                    for wall in walls:
                        if self.collision_rectangle.colliderect(wall):
                            if dx > 0: self.collision_rectangle.right = wall.left
                            if dx < 0: self.collision_rectangle.left = wall.right
                            self.player2_x = self.collision_rectangle.x - self.offset_x
                    
                    self.player2_y += dy
                    self.collision_rectangle.y = self.player2_y + self.offset_y
                    for wall in walls:
                        if self.collision_rectangle.colliderect(wall):
                            if dy > 0: self.collision_rectangle.bottom = wall.top
                            if dy < 0: self.collision_rectangle.top = wall.bottom
                            self.player2_y = self.collision_rectangle.y - self.offset_y
                    self.collision_rectangle.topleft = (self.player2_x + self.offset_x, self.player2_y + self.offset_y)

                def draw(self, screen):
                    if not self.exploded:
                        screen.blit(self.sprite_player2, (self.player2_x, self.player2_y))
                        if ui.get_setting("hitboxes"):
                            pygame.draw.rect(screen, (0, 0, 255), self.collision_rectangle, 2)
                
                def collide(self, bullet_rect):
                    if not self.exploded:
                        if self.collision_rectangle.colliderect(bullet_rect):
                            if ui.get_setting("particles"):
                                explosions.append([Particle(self.player2_x + 34, self.player2_y + 30) for _ in range(100)])
                            self.health -= damage()
                            return True
                    return False

            player_2 = Player2()

            while game:
                if countdown > 0:
                    for event in pygame.event.get(): ...
                    screen.blit(background, (0, 0))
                    screen.blit(dim, (0, 0))
                    text_surf = other_font.render(f"{countdown-1}".replace("0", "Fight!"), True, (255, 255, 255))
                    screen.blit(text_surf, text_surf.get_rect(center=(width//2, height//2)))
                    pygame.display.flip()
                    countdown -= 1
                    time.sleep(1.0)
                    continue
                
                player_1.move(walls)
                player_2.move(walls)
                screen.blit(background, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and player_1.exploded == False:
                    if (bullet_counter1 > 20):
                        shot.play()
                        bullet_list1.append(Bullet(player_1.player1_x + 20, player_1.player1_y, player_1.direction))
                        bullet_counter1 = 0

                if keys[pygame.K_RETURN] and player_2.exploded == False:
                    if (bullet_counter2 > 20):
                        shot.play()
                        bullet_list2.append(Bullet(player_2.player2_x + 20, player_2.player2_y, player_2.direction))
                        bullet_counter2 = 0
                
                if player_1.health <= 0:
                    player_1.exploded = True
                    dead.play()
                    player_1.health = 100
                    player_2.health = 100
                    
                if player_2.health <= 0:
                    player_2.exploded = True
                    dead.play()
                    player_1.health = 100
                    player_2.health = 100

                clock.tick(60)
                bullet_counter1 += 0.2
                bullet_counter2 += 0.2

                for wall in walls:
                    pygame.draw.rect(screen, (255, 0, 0), wall, 1)

                if player_1.health < last_health1:
                    last_health1 = player_1.health
                    hp_bar_health1 = hp_bar_health1.subsurface(pygame.Rect(0, 0, max(int(225 * (player_1.health / 100)), 1), hp_bar_rect1.height))
                if player_2.health < last_health2:
                    last_health2 = player_2.health
                    hp_bar_health2 = hp_bar_health2.subsurface(pygame.Rect(0, 0, max(int(225 * (player_2.health / 100)), 1), hp_bar_rect2.height))

                screen.blit(hp_bar_back, hp_bar_rect1)
                screen.blit(hp_bar_health1, hp_bar_rect1)
                text_surf = primary_font.render(f"{max(player_1.health, 0)} HP", True, (255, 255, 255))
                screen.blit(text_surf, text_surf.get_rect(center=hp_bar_rect1.center))
                screen.blit(hp_bar_overlay, hp_bar_rect1)
                screen.blit(hp_bar_back, hp_bar_rect2)
                screen.blit(hp_bar_health2, hp_bar_rect2)
                text_surf = primary_font.render(f"{max(player_2.health, 0)} HP", True, (255, 255, 255))
                screen.blit(text_surf, text_surf.get_rect(center=hp_bar_rect2.center))
                screen.blit(hp_bar_overlay, hp_bar_rect2)

                player_1.draw(screen)
                player_2.draw(screen)

                for bullet in reversed(bullet_list1):
                    bullet.move()
                    bullet.draw(screen)
                    hit_wall = False
                    for wall in walls:
                        if bullet.collision_rectangle.colliderect(wall): hit_wall = True
                    if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980 or hit_wall:
                        bullet_list1.remove(bullet)
                        if hit_wall and ui.get_setting("particles"):
                            explosions.append([Particle(bullet.x, bullet.y) for _ in range(100)])
                    elif player_2.collide(bullet.collision_rectangle):
                        bullet_list1.remove(bullet)

                for bullet in reversed(bullet_list2):
                    bullet.move()
                    bullet.draw(screen)
                    hit_wall = False
                    for wall in walls:
                        if bullet.collision_rectangle.colliderect(wall): hit_wall = True
                    if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980 or hit_wall:
                        bullet_list2.remove(bullet)
                        if hit_wall and ui.get_setting("particles"):
                            explosions.append([Particle(bullet.x, bullet.y) for _ in range(100)])
                    elif player_1.collide(bullet.collision_rectangle):
                        bullet_list2.remove(bullet)
                
                for explosion in explosions:
                    for particle in explosion:
                        particle.update()
                        particle.draw(screen)
                explosions = [[p for p in explosion if p.lifetime > 0] for explosion in explosions]
                explosions = [e for e in explosions if len(e) > 0]
                pygame.display.flip()
            pygame.quit()

        # =====================================================================
        # KING OF THE HILL - ORÖRD (FÖRUTOM NÖDVÄNDIGA ANPASSNINGAR)
        # =====================================================================
        elif ui.get_kind() == "king of hill":
            hill_size = 300
            hill_rect = pygame.Rect((width - hill_size) // 2, (height - hill_size) // 2, hill_size, hill_size)
            p1_score = 0
            p2_score = 0
            score_font = pygame.font.Font("assets/fonts/SEEKUW.ttf", 40)

            player_1 = Player1(speed_val=5) # Behåller originalhastighet för KotH (eller vad den nu var)
            
            class Player2_KotH:
                def __init__(self):
                    self.player2_x = width - 90
                    self.player2_y = (height // 2) - 20
                    self.health = player_health
                    self.damage = damage()
                    self.speed = 3
                    self.direction = "UP"
                    self.exploded = False
                    self.original_image = sprite_player2
                    self.sprite_player2 = self.original_image
                    hitbox_width = self.sprite_player2.get_width() - 25
                    hitbox_height = self.sprite_player2.get_height() - 25
                    self.offset_x = (self.sprite_player2.get_width() - hitbox_width) // 2
                    self.offset_y = (self.sprite_player2.get_height() - hitbox_height) // 2
                    self.collision_rectangle = pygame.Rect(self.player2_x + self.offset_x, self.player2_y + self.offset_y, hitbox_width, hitbox_height)

                def move(self, walls, target_player_x, target_player_y):
                    if self.health <= 0: return
                    center_x = 960 
                    center_y = 540
                    dist_to_center = math.sqrt((self.player2_x - center_x)**2 + (self.player2_y - center_y)**2)
                    dist_to_player = math.sqrt((self.player2_x - target_player_x)**2 + (self.player2_y - target_player_y)**2)

                    if dist_to_center > 100:
                        target_x = center_x
                        target_y = center_y
                    elif dist_to_player < 200: 
                        target_x = target_player_x
                        target_y = target_player_y
                    elif dist_to_center < 5:
                        self.player2_x = center_x
                        self.player2_y = center_y
                        self.collision_rectangle.x = self.player2_x + self.offset_x
                        self.collision_rectangle.y = self.player2_y + self.offset_y
                        return 
                    else:
                        target_x = center_x
                        target_y = center_y

                    diff_x = target_x - self.player2_x
                    diff_y = target_y - self.player2_y
                    
                    bias_x = 0
                    bias_y = 0
                    if dist_to_center > 150:
                        if self.direction in ["LEFT", "RIGHT"]: bias_x = 60 
                        if self.direction in ["UP", "DOWN"]: bias_y = 60    
                    
                    moves_to_try = []
                    if abs(diff_x) + bias_x > abs(diff_y) + bias_y:
                        moves_to_try = [("X", diff_x), ("Y", diff_y)]
                    else:
                        moves_to_try = [("Y", diff_y), ("X", diff_x)]

                    moved_successfully = False
                    
                    for axis, value in moves_to_try:
                        if moved_successfully: break 
                        if abs(value) < 2: continue 

                        test_dx = 0
                        test_dy = 0
                        angle = 0
                        dir_str = ""
                        
                        if axis == "X":
                            if value > 0: test_dx = self.speed; dir_str = "RIGHT"; angle = 270
                            else: test_dx = -self.speed; dir_str = "LEFT"; angle = 90
                        else: 
                            if value > 0: test_dy = self.speed; dir_str = "DOWN"; angle = 180
                            else: test_dy = -self.speed; dir_str = "UP"; angle = 0
                        
                        self.player2_x += test_dx
                        self.player2_y += test_dy
                        self.collision_rectangle.x = self.player2_x + self.offset_x
                        self.collision_rectangle.y = self.player2_y + self.offset_y
                        
                        hit = False
                        for wall in walls:
                            if self.collision_rectangle.colliderect(wall):
                                hit = True
                                self.player2_x -= test_dx
                                self.player2_y -= test_dy
                                self.collision_rectangle.x = self.player2_x + self.offset_x
                                self.collision_rectangle.y = self.player2_y + self.offset_y
                                break 
                        
                        if not hit:
                            self.direction = dir_str
                            self.sprite_player2 = pygame.transform.rotate(self.original_image, angle)
                            moved_successfully = True

                def draw(self, screen):
                    if not self.exploded:
                        screen.blit(self.sprite_player2, (self.player2_x, self.player2_y))
                        if ui.get_setting("hitboxes"):
                            pygame.draw.rect(screen, (0, 0, 255), self.collision_rectangle, 2)

                def collide(self, bullet_rect):
                    if not self.exploded:
                        if self.collision_rectangle.colliderect(bullet_rect):
                            if ui.get_setting("particles"):
                                explosions.append([Particle(self.player2_x + 34, self.player2_y + 30) for _ in range(100)])
                            self.health -= damage()
                            return True 
                    return False 

            player_2 = Player2_KotH()

            while game:
                if countdown > 0:
                    for event in pygame.event.get(): 
                        if event.type == pygame.QUIT: game = False
                    screen.blit(background, (0, 0))
                    pygame.draw.rect(screen, (50, 200, 50, 100), hill_rect, 5)
                    screen.blit(dim, (0, 0))
                    text_surf = other_font.render(f"{countdown-1}".replace("0", "Capture!"), True, (255, 255, 255))
                    screen.blit(text_surf, text_surf.get_rect(center=(width//2, height//2)))
                    pygame.display.flip()
                    countdown -= 1
                    time.sleep(1.0)
                    continue
                
                player_1.move(walls)
                player_2.move(walls, player_1.player1_x, player_1.player1_y) 

                screen.blit(background, (0, 0))
                
                hill_color = (100, 100, 100) 
                p1_in_hill = player_1.collision_rectangle.colliderect(hill_rect) and not player_1.exploded
                p2_in_hill = player_2.collision_rectangle.colliderect(hill_rect) and not player_2.exploded

                if p1_in_hill and not p2_in_hill:
                    hill_color = (0, 255, 0)
                    p1_score += 1
                elif p2_in_hill and not p1_in_hill:
                    hill_color = (255, 0, 0)
                    p2_score += 1
                elif p1_in_hill and p2_in_hill:
                    hill_color = (255, 255, 0)
                
                s = pygame.Surface((hill_size, hill_size))  
                s.set_alpha(100)                
                s.fill(hill_color)           
                screen.blit(s, (hill_rect.x, hill_rect.y))
                pygame.draw.rect(screen, hill_color, hill_rect, 5)

                p1_text = score_font.render(f"P1: {p1_score}", True, (0, 255, 0))
                p2_text = score_font.render(f"AI: {p2_score}", True, (255, 50, 50))
                screen.blit(p1_text, (50, 100))
                screen.blit(p2_text, (width - 250, 100))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT: game = False
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and player_1.exploded == False:
                    if (bullet_counter1 > 20):
                        shot.play()
                        bullet_list1.append(Bullet(player_1.player1_x + 20, player_1.player1_y, player_1.direction))
                        bullet_counter1 = 0

                dist_to_p1 = math.sqrt((player_1.player1_x - player_2.player2_x)**2 + (player_1.player1_y - player_2.player2_y)**2)
                if not player_2.exploded and bullet_counter2 > 40 and dist_to_p1 < 600:
                    shot.play()
                    bx, by = player_2.player2_x, player_2.player2_y
                    if player_2.direction == "UP": bx += 20; by -= 10
                    elif player_2.direction == "DOWN": bx += 20; by += 40
                    elif player_2.direction == "LEFT": bx -= 10; by += 20
                    elif player_2.direction == "RIGHT": bx += 40; by += 20
                    bullet_list2.append(Bullet(bx, by, player_2.direction))
                    bullet_counter2 = 0

                if player_1.health <= 0:
                    player_1.exploded = True
                    dead.play()
                    if ui.get_setting("particles"):
                        explosions.append([Particle(player_1.player1_x, player_1.player1_y) for _ in range(100)])
                    player_1.health = 100
                    player_1.player1_x = 30
                    player_1.player1_y = height // 2

                if player_2.health <= 0:
                    player_2.exploded = True
                    dead.play()
                    if ui.get_setting("particles"):
                        explosions.append([Particle(player_2.player2_x, player_2.player2_y) for _ in range(100)])
                    player_2.health = 100
                    player_2.player2_x = width - 90
                    player_2.player2_y = height // 2

                clock.tick(60)
                bullet_counter1 += 0.5
                bullet_counter2 += 0.3 

                for wall in walls:
                    pygame.draw.rect(screen, (255, 0, 0), wall, 1)

                if player_1.health < last_health1:
                    last_health1 = player_1.health
                    hp_bar_health1 = hp_bar_health1.subsurface(pygame.Rect(0, 0, max(int(225 * (player_1.health / 100)), 1), hp_bar_rect1.height))
                if player_2.health < last_health2:
                    last_health2 = player_2.health
                    hp_bar_health2 = hp_bar_health2.subsurface(pygame.Rect(0, 0, max(int(225 * (player_2.health / 100)), 1), hp_bar_rect2.height))

                screen.blit(hp_bar_back, hp_bar_rect1)
                screen.blit(hp_bar_health1, hp_bar_rect1)
                screen.blit(hp_bar_overlay, hp_bar_rect1)
                screen.blit(hp_bar_back, hp_bar_rect2)
                screen.blit(hp_bar_health2, hp_bar_rect2)
                screen.blit(hp_bar_overlay, hp_bar_rect2)

                player_1.draw(screen)
                player_2.draw(screen)

                for bullet in reversed(bullet_list1):
                    bullet.move()
                    bullet.draw(screen)
                    hit_wall = False
                    for wall in walls:
                        if bullet.collision_rectangle.colliderect(wall): hit_wall = True
                    if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980 or hit_wall:
                        bullet_list1.remove(bullet)
                        if hit_wall and ui.get_setting("particles"):
                            explosions.append([Particle(bullet.x, bullet.y) for _ in range(100)])
                    elif player_2.collide(bullet.collision_rectangle):
                        bullet_list1.remove(bullet)

                for bullet in reversed(bullet_list2):
                    bullet.move()
                    bullet.draw(screen)
                    hit_wall = False
                    for wall in walls:
                        if bullet.collision_rectangle.colliderect(wall): hit_wall = True
                    if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980 or hit_wall:
                        bullet_list2.remove(bullet)
                        if hit_wall and ui.get_setting("particles"):
                            explosions.append([Particle(bullet.x, bullet.y) for _ in range(100)])
                    elif player_1.collide(bullet.collision_rectangle):
                        bullet_list2.remove(bullet)

                for explosion in explosions:
                    for particle in explosion:
                        particle.update()
                        particle.draw(screen)
                explosions = [[p for p in explosion if p.lifetime > 0] for explosion in explosions]
                explosions = [e for e in explosions if len(e) > 0]
                
                pygame.display.flip()
                
                if p1_score >= 1000:
                    print("PLAYER 1 WINS!")
                    game = False
                if p2_score >= 1000:
                    print("AI WINS!")
                    game = False

            pygame.quit()
    
    ui.restart()