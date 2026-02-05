
whole_game = True

import random
import time
import pygame
import ui
import math
while whole_game:
    pygame.init()
    shot = pygame.mixer.Sound("C:/War Lightning/assets/audio/Tank shot.mp3")
    normal_hit = pygame.mixer.Sound("C:/War Lightning/assets/audio/Metal hit.mp3")
    crit_hit = pygame.mixer.Sound("C:/War Lightning/assets/audio/Metal pierce.mp3")
    dead = pygame.mixer.Sound("C:/War Lightning/assets/audio/Tank kaboom.mp3")
    start = pygame.mixer.Sound("assets/audio/Match start.mp3")
    pygame.mixer.music.load("assets/music/Ambi med paus.mp3")
    start.play()
    pygame.mixer.music.play(-1) 
    volume = ui.get_setting("volume")
    pygame.mixer.music.set_volume(volume)

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
        #Spelarnas stats
        player_health = 100
        center_y = height // 2
        center_x = width // 2
        

        #Denna delen laddar in de olika sprites, och bakgrunder vi har i spelet
        original_background1 = pygame.image.load("C:/War Lightning/assets/tiles/map1.png")
        original_background2 = pygame.image.load("C:/War Lightning/assets/tiles/map2.png")
        original_bullet = pygame.image.load("C:/War Lightning/assets/bullets/bullet.png")
        original_player1 = pygame.image.load("C:/War Lightning/assets/tanks/Player1.png")
        original_player2 = pygame.image.load("C:/War Lightning/assets/tanks/Player2.png")
        
        

        background1 = pygame.transform.smoothscale(original_background1, (width, height))
        background2 = pygame.transform.smoothscale(original_background2, (width, height))
        sprite_bullet = pygame.transform.smoothscale(original_bullet, (original_bullet.get_width() + 1, original_bullet.get_height() + 1))
        sprite_player1 = pygame.transform.smoothscale(original_player1, (original_player1.get_width(), original_player1.get_height()))
        sprite_player2 = pygame.transform.smoothscale(original_player2, (original_player2.get_width(), original_player2.get_height()))
        #Här defineras fps klockan för att begränsa till samma hastighet
        clock = pygame.time.Clock()
        #Det som håller spelet igång och startar upp fönstret
        game = True
        maps = [background1, background2]
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("War Lightning")
        pygame.display.set_icon(pygame.image.load("assets/ui/war_lightning.png"))
        


        def damage():
            chans = random.randint(1, 3)
            if chans == 1:
                player_damage = 20
                crit_hit.play()
            else:
                player_damage = 10
                normal_hit.play()

            return player_damage
        


        #Klasserna för spelare 1 och spelare 2 som innehåller deras hälsa, skada, olika lägen, hastighet och alla deras funktioner
        class Player1:
            def __init__(self):
                self.player1_x = 30
                self.player1_y = (height // 2) - 20
                self.sprite_player1 = sprite_player1
                self.health = player_health
                self.damage = damage()
                self.speed = 1
                self.original_image = sprite_player1
                self.sprite_player1 = self.original_image
                self.direction = "UP"
                self.exploded = False
                hitbox_width = self.sprite_player1.get_width() - 25
                hitbox_height = self.sprite_player1.get_height() - 25
                self.kingpoints = 0
                self.sprite_player1 = pygame.transform.rotate(self.original_image, 270)
                
                self.offset_x = (self.sprite_player1.get_width() - hitbox_width) // 2
                self.offset_y = (self.sprite_player1.get_height() - hitbox_height) // 2
                
                
                self.collision_rectangle = pygame.Rect(
                    self.player1_x + self.offset_x, 
                    self.player1_y + self.offset_y, 
                    hitbox_width, 
                    hitbox_height
                )

            def move(self, walls, broken_walls):
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
                self.collision_rectangle.x = self.player1_x
                
                self.collision_rectangle.x = self.player1_x + self.offset_x
                
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if dx > 0: 
                            self.collision_rectangle.right = wall.left
                        if dx < 0: 
                            self.collision_rectangle.left = wall.right
                        
                        
                        self.player1_x = self.collision_rectangle.x - self.offset_x

                for broken_wall in broken_walls:
                    if self.collision_rectangle.colliderect(broken_wall):
                        if dx > 0: 
                            self.collision_rectangle.right = broken_wall.left
                        if dx < 0: 
                            self.collision_rectangle.left = broken_wall.right
                        
                        
                        self.player1_x = self.collision_rectangle.x - self.offset_x


                
                self.player1_y += dy
                
                
                self.collision_rectangle.y = self.player1_y + self.offset_y
                
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if dy > 0: 
                            self.collision_rectangle.bottom = wall.top
                        if dy < 0: 
                            self.collision_rectangle.top = wall.bottom
                        
                        
                        self.player1_y = self.collision_rectangle.y - self.offset_y

                for broken_wall in broken_walls:
                    if self.collision_rectangle.colliderect(broken_wall):
                        if dy > 0: 
                            self.collision_rectangle.bottom = broken_wall.top
                        if dy < 0: 
                            self.collision_rectangle.top = broken_wall.bottom
                        
                        
                        self.player1_y = self.collision_rectangle.y - self.offset_y

                self.collision_rectangle.topleft = (self.player1_x + self.offset_x, self.player1_y + self.offset_y)

            def draw(self, screen):
                if not self.exploded:
                    screen.blit(self.sprite_player1, (self.player1_x, self.player1_y))
                    

                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (0, 0, 255), self.collision_rectangle, 2)
                
            def collide(self, bullet_rect):
                if not player_1.exploded:
                    if self.collision_rectangle.colliderect(bullet_rect):
                        if ui.get_setting("particles"):
                            explosion = [Particle(player_1.player1_x + 34, player_1.player1_y + 30) for _ in range(100)]
                            explosions.append(explosion)
                        player_1.health -= damage()
                        return True 
                return False 
        
        class Ai:
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
                    self.kingpoints = 0
                    
                    self.patrol_target_x = random.randint(50, width - 50)
                    self.patrol_target_y = random.randint(50, height - 50)
                    self.mode = "PATROL" 
                    self.patrol_timer = 0 

                def move(self, walls, broken_walls, target_player_x, target_player_y):
                    if self.health <= 0: return

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

                    # Rörelse (Ingen sicksack)
                    diff_x = target_x - self.player2_x
                    diff_y = target_y - self.player2_y
                    
                    bias_x = 0
                    bias_y = 0
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

                        dx = 0
                        dy = 0
                        dir_str = ""
                        angle = 0
                        
                        if axis == "X":
                            if value > 0: dx = self.speed; dir_str = "RIGHT"; angle = 270
                            else: dx = -self.speed; dir_str = "LEFT"; angle = 90
                        else: 
                            if value > 0: dy = self.speed; dir_str = "DOWN"; angle = 180
                            else: dy = -self.speed; dir_str = "UP"; angle = 0
                        
                        self.player2_x += dx
                        self.player2_y += dy
                        self.collision_rectangle.x = self.player2_x + self.offset_x
                        self.collision_rectangle.y = self.player2_y + self.offset_y
                        
                        hit = False
                        for wall in walls:
                            if self.collision_rectangle.colliderect(wall):
                                hit = True
                                self.player2_x -= dx
                                self.player2_y -= dy
                                self.collision_rectangle.x = self.player2_x + self.offset_x
                                self.collision_rectangle.y = self.player2_y + self.offset_y
                                break 
                        for broken_wall in broken_walls:
                            if self.collision_rectangle.colliderect(broken_wall):
                                if dx > 0: 
                                    self.collision_rectangle.right = broken_wall.left
                                if dx < 0: 
                                    self.collision_rectangle.left = broken_wall.right
                                
                                
                                self.player2_x = self.collision_rectangle.x - self.offset_x
                        self.player2_y += dy
                        
                        if not hit:
                            self.direction = dir_str
                            self.sprite_player2 = pygame.transform.rotate(self.original_image, angle)
                            moved_successfully = True

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
                    
        
        class Player2:
            def __init__(self):
                self.player2_x = width - 90
                self.player2_y = (height // 2) - 20
                self.sprite_player2 = sprite_player2
                self.health = player_health
                self.damage = damage()
                self.speed = 1
                self.direction = "UP"
                self.exploded = False
                self.original_image = sprite_player2
                self.sprite_player2 = self.original_image
                hitbox_width = self.sprite_player2.get_width() - 25
                hitbox_height = self.sprite_player2.get_height() - 25
                self.kingpoints = 0
                self.sprite_player2 = pygame.transform.rotate(self.original_image, 90)
            
            
                self.offset_x = (self.sprite_player2.get_width() - hitbox_width) // 2
                self.offset_y = (self.sprite_player2.get_height() - hitbox_height) // 2
                
                
                self.collision_rectangle = pygame.Rect(
                    self.player2_x + self.offset_x, 
                    self.player2_y + self.offset_y, 
                    hitbox_width, 
                    hitbox_height
                )

            def move(self, walls, broken_walls):
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
                self.collision_rectangle.x = self.player2_x
                
                self.collision_rectangle.x = self.player2_x + self.offset_x
                
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if dx > 0: 
                            self.collision_rectangle.right = wall.left
                        if dx < 0: 
                            self.collision_rectangle.left = wall.right
                        
                        
                        self.player2_x = self.collision_rectangle.x - self.offset_x

                for broken_wall in broken_walls:
                    if self.collision_rectangle.colliderect(broken_wall):
                        if dx > 0: 
                            self.collision_rectangle.right = broken_wall.left
                        if dx < 0: 
                            self.collision_rectangle.left = broken_wall.right
                        
                        
                        self.player2_x = self.collision_rectangle.x - self.offset_x
                self.player2_y += dy
                
                
                self.collision_rectangle.y = self.player2_y + self.offset_y
                
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if dy > 0: 
                            self.collision_rectangle.bottom = wall.top
                        if dy < 0: 
                            self.collision_rectangle.top = wall.bottom
                        
                        
                        self.player2_y = self.collision_rectangle.y - self.offset_y

                for broken_wall in broken_walls:
                    if self.collision_rectangle.colliderect(broken_wall):
                        if dy > 0: 
                            self.collision_rectangle.bottom = broken_wall.top
                        if dy < 0: 
                            self.collision_rectangle.top = broken_wall.bottom
                        
                        
                        self.player2_y = self.collision_rectangle.y - self.offset_y

            
                self.collision_rectangle.topleft = (self.player2_x + self.offset_x, self.player2_y + self.offset_y)

            def draw(self, screen):
                if not self.exploded:
                    screen.blit(self.sprite_player2, (self.player2_x, self.player2_y))
                    


                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (0, 0, 255), self.collision_rectangle, 2)
                
            def collide(self, bullet_rect):
                if not player_2.exploded:
                    if self.collision_rectangle.colliderect(bullet_rect):
                        if ui.get_setting("particles"):
                            explosion = [Particle(player_2.player2_x + 34, player_2.player2_y + 30) for _ in range(100)]
                            explosions.append(explosion)
                        player_2.health -= damage()
                        return True 
                return False 

        #Klassen för skotten som båda spelarna kan skjuta, och håller koll på hastighet och direktion
        # Klassen för skotten som båda spelarna kan skjuta
        class Bullet:
            def __init__(self, x, y, direction):
                self.speed = 20
                self.direction = direction
                
                # 1. Rotera bilden FÖRST så vi vet hur stor den är
                if self.direction == "UP":
                    self.bild = sprite_bullet
                    # Justera startposition för att matcha hur du ritade förut (+8 i X-led)
                    self.x = x + 8
                    self.y = y
                elif self.direction == "DOWN":
                    self.bild = pygame.transform.rotate(sprite_bullet, 180)
                    self.x = x + 8
                    self.y = y
                elif self.direction == "LEFT":
                    self.bild = pygame.transform.rotate(sprite_bullet, 90)
                    # Justera startposition (+28 i Y-led för liggande skott)
                    self.x = x
                    self.y = y + 28
                elif self.direction == "RIGHT":
                    self.bild = pygame.transform.rotate(sprite_bullet, -90)
                    self.x = x
                    self.y = y + 28
                else:
                    # Fallback om något går fel
                    self.bild = sprite_bullet
                    self.x = x
                    self.y = y

                # 2. Skapa hitboxen utifrån den ROTERADE bilden
                # Nu får hitboxen rätt bredd och höjd automatiskt (smal för upp/ner, bred för höger/vänster)
                self.collision_rectangle = self.bild.get_rect()
                self.collision_rectangle.topleft = (self.x, self.y)
                self.collision = False

            def move(self):
                if self.direction == "UP":
                    self.y -= self.speed
                elif self.direction == "DOWN":
                    self.y += self.speed
                elif self.direction == "LEFT":
                    self.x -= self.speed
                elif self.direction == "RIGHT":
                    self.x += self.speed

                # Uppdatera hitboxens position till de nya koordinaterna
                self.collision_rectangle.topleft = (self.x, self.y)

            def draw(self, screen):
                # Rita bilden exakt där hitboxen är
                # Vi tog bort de manuella offset-värdena (+8, +28) härifrån
                # och la in dem i __init__ istället.
                screen.blit(self.bild, self.collision_rectangle.topleft)
                
                # (Valfritt) Avkommentera raden nedan för att se hitboxen tydligt när du testar:
                # pygame.draw.rect(screen, (0, 255, 0), self.collision_rectangle, 1)

            

        #Klassen som gör det möjligt för sprites att kunna rotera på sig så att det blir snyggare
        class RotatingSprite(pygame.sprite.Sprite):
            def __init__(self, x, y, image_path):
                super().__init__()
                
                
                self.original_image = pygame.image.load(image_path).convert_alpha()
                
                
                self.image = self.original_image
                
                
                self.rect = self.image.get_rect()
                self.rect.center = (x, y)
                
                
                self.angle = 0
                self.rotation_speed = 2 

            def update(self):
            
                self.angle += self.rotation_speed
                
                
                self.angle = self.angle % 360 

                self.image = pygame.transform.rotate(self.original_image, self.angle)
                
                
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center




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

        class Pickup:
            def __init__(self, image, effect, tag):
                self.x = random.randint(50, (width - 50))
                self.y = random.randint(50, (height - 50))
                self.image = image # pygame.image.load()
                self.effect = effect # 0 -> 1000 ?
                self.tag = tag # "health" el. "strength"
            
            def collides(self, player):
                print(self.image.get_rect(topleft=(self.x, self.y)))
                return player.collision_rectangle.colliderect(self.image.get_rect(topleft=(self.x, self.y)))
            
            def draw(self, screen):
                screen.blit(self.image, (self.x, self.y))

        primary_font = pygame.font.Font("assets/fonts/SEEKUW.ttf", 20)
        other_font = pygame.font.Font("assets/fonts/SEEKUW.ttf", 100)
        dim = pygame.Surface((width, height), pygame.SRCALPHA)
        dim.fill((50, 50, 50, 150))
        countdown = 4


        if ui.get_map() == "Idrilyn":
            background = background1
        elif ui.get_map() == "Nebrodu":
            background = background2
        elif ui.get_map() == "Random":
            background = random.choice(maps)

        if background == background1:
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
                pygame.Rect(0, 0, width, 28),
                pygame.Rect(width - 27, 0, 28, height),
                pygame.Rect(0, height - 27, width, 28),
                pygame.Rect(-1, 0, 28, height),
                ]
            broken_walls = [ 
                pygame.Rect(255, 590, 86, 28), 
                pygame.Rect(794, 255, 28, 80), 
                pygame.Rect(1108, 255, 28, 80),
                pygame.Rect(1582, 425, 28, 80),
                pygame.Rect(822, 946, 86, 28),
                pygame.Rect(1022, 936, 86, 28),
                pygame.Rect(822, 474, 86, 28),
                pygame.Rect(936, 968, 84, 28), 
            ]
        elif background == background2:
            walls = [
                pygame.Rect(0, 0, width, 28),
                pygame.Rect(width - 27, 0, 28, height),
                pygame.Rect(0, height - 27, width, 28),
                pygame.Rect(-1, 0, 28, height),
                pygame.Rect(-1, 479, 172, 28),
                pygame.Rect(-2, 590, 172, 28),
                pygame.Rect(1768, 485, 172, 28),
                pygame.Rect(1768, 590, 172, 28),
                pygame.Rect(251, 507, 28, 86),
                pygame.Rect(760, 507, 28, 86),
                pygame.Rect(1248, 507, 28, 86),
                pygame.Rect(1640, 506, 28, 86),
                pygame.Rect(255, 312, 86, 28),
                pygame.Rect(590, 310, 86, 28),
                pygame.Rect(1354, 311, 86, 28),
                pygame.Rect(1690, 311, 86, 28),
                pygame.Rect(254, 812, 86, 28),
                pygame.Rect(591, 812, 86, 28),
                pygame.Rect(1354, 911, 86, 28),
                pygame.Rect(1690, 900, 86, 28),
                pygame.Rect(847, 980, 86, 28),
                pygame.Rect(1104, 980, 86, 28),
                pygame.Rect(846, 169, 86, 28),
                pygame.Rect(1102, 169, 86, 28),
                
                ]  
            broken_walls = [
                pygame.Rect(932, 485, 86, 26),
                pygame.Rect(932, 649, 86, 26),
                pygame.Rect(1020, 485, 86, 26),
                pygame.Rect(1020, 649, 86, 26),
            ] 
        # Här defineras de två spelarna utifrån deras klasser
        player_1 = Player1()
        if ui.get_kind() == "king of hill":
            last_kingpoints1 = 0

        # ÄNDRING: Här bestämmer vi vem Player 2 är
        if ui.get_mode() == "solo":
            player_2 = Ai()  # Player 2 blir en AI
        else:
            player_2 = Player2() # Player 2 blir en människa (VS mode)

        if ui.get_kind() == "king of hill":
            last_kingpoints2 = 0

        # Ta bort raden: ai = Ai() helt och hållet, den behövs inte nu.
        #Och här definieras skott räknarna som gör att man inte kan skjuta för snabbt
        bullet_counter1 = 0
        bullet_counter2 = 0
        #Listor som håller koll på de olika objekten som avfyrats från båda spelarna under en runda
        bullet_list1 = []
        bullet_list2 = []
        #Main spel loopen där hela spelet händer och där alla funktioner och all logik uppdateras och genomförs.
        #All kollision
        pickups = [
        Pickup(pygame.image.load("assets/tanks/Player1.png"), 25, "health")
        ]
        last_spawn = 0
        dim2 = pygame.Surface((200, 200), pygame.SRCALPHA)
        original_flag_p0 = pygame.image.load("assets/ui/flag_p0.png")
        original_flag_p1 = pygame.image.load("assets/ui/flag_p1.png")
        original_flag_p2 = pygame.image.load("assets/ui/flag_p2.png")
        flag_p0 = pygame.transform.smoothscale(original_flag_p0, (100, 100))
        flag_p1 = pygame.transform.smoothscale(original_flag_p1, (100, 100))
        flag_p2 = pygame.transform.smoothscale(original_flag_p2, (100, 100))

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
        last_death1 = 0.0
        last_death2 = 0.0

        frames = 0
        original_breakable_wall = pygame.image.load("assets/tiles/breakdawallwall.png")
        breakable_wall1 = pygame.transform.smoothscale(original_breakable_wall, (86, 28))
        breakable_wall2 = pygame.transform.smoothscale(pygame.transform.rotate(original_breakable_wall, 90), (28, 80))
        breakable_wall3 = pygame.transform.smoothscale(original_breakable_wall, (84, 28))

        
            
        
        winner = None
        original_winscreen1 = pygame.image.load("assets/ui/p1_win.png")
        original_winscreen2 = pygame.image.load("assets/ui/p2_win.png")
        win_screen1 = pygame.transform.smoothscale(original_winscreen1, (width // 1.4, height // 1.4))
        win_screen2 = pygame.transform.smoothscale(original_winscreen2, (width // 1.4, height // 1.4))
        if ui.get_kind() == "deathmatch":
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
                
                if not winner is None:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game = False

                    if winner == "player1":
                        screen.blit(win_screen1, ((width - width // 1.4) // 2, (height - height // 1.4) // 2))
                    elif winner == "player2":
                        screen.blit(win_screen2, ((width - width // 1.4) // 2, (height - height // 1.4) // 2))

                    now = time.monotonic()
                    if now - win_time >= 3:
                        game = False
                    pygame.display.flip()
                    continue
                    
                
                # Funktionerna för att de två spelarna ska kunna röra sig
                player_1.move(walls, broken_walls)
                
                if ui.get_mode() == "solo":
                    # Om det är solo, skicka med målets koordinater (player_1) till AI:n
                    player_2.move(walls, broken_walls, player_1.player1_x, player_1.player1_y)
                else:
                    # Om det är VS, kör vanlig move utan mål
                    player_2.move(walls, broken_walls)
                #Här ritas bakgrunden
                screen.blit(background, (0, 0))
                #Här görs det så att man kan stänga fönstret och döda systemet
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game = False

                
                keys = pygame.key.get_pressed()
                #Knappbindningarna för att skjuta som spelare 1 och spelare 2, och när de skjuter och lever så läggs det till objekt i de tomma listorna
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

            
                
                if ui.get_mode() == "solo" and not player_2.exploded:
                    
                    if bullet_counter2 > 20:
                        # Chans att skjuta (gör den lägre för svårare motstånd, högre för lättare)
                        should_shoot = False
                        
                        # Om vi jagar (är nära), skjut oftare
                        dist_x = abs(player_1.player1_x - player_2.player2_x)
                        dist_y = abs(player_1.player1_y - player_2.player2_y)
                        
                        # Om vi tittar åt rätt håll ungefär
                        if player_2.direction == "LEFT" and player_1.player1_x < player_2.player2_x and dist_y < 50: should_shoot = True
                        elif player_2.direction == "RIGHT" and player_1.player1_x > player_2.player2_x and dist_y < 50: should_shoot = True
                        elif player_2.direction == "UP" and player_1.player1_y < player_2.player2_y and dist_x < 50: should_shoot = True
                        elif player_2.direction == "DOWN" and player_1.player1_y > player_2.player2_y and dist_x < 50: should_shoot = True
                        
                        if should_shoot:
                            shot.play()
                            bullet_list2.append(Bullet(player_2.player2_x + 20, player_2.player2_y, player_2.direction))
                            bullet_counter2 = 0

                #Här så uppdateras varenda objekt i respektive lista
                

                if player_1.health < 0 or player_1.health == 0:
                    player_1.exploded = True
                    dead.play()
                    if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            
                            explosions.append(explosion)
                    
                    winner = "player2"
                    win_time = time.monotonic()
                if player_2.health < 0 or player_2.health == 0:
                    player_2.exploded = True
                    dead.play()
                    if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            
                            explosions.append(explosion)
                    
                    winner = "player1"
                    win_time = time.monotonic()
                #Här konfigueras fps klockan till sextio frames per sekund
                clock.tick(60)#och här läggs det till till räknarna för att det ska gå långsammare att skjuta
                bullet_counter1 = bullet_counter1 + 0.2
                bullet_counter2 = bullet_counter2 + 0.2


                for wall in walls:
                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (255, 0, 0), wall, 1)

                for broken_wall in broken_walls:
                    size = broken_wall.size
                    if size == (86, 28):
                        screen.blit(breakable_wall1, broken_wall)
                    elif size == (28, 80):
                        screen.blit(breakable_wall2, broken_wall)
                    elif size == (84, 28):
                        screen.blit(breakable_wall3, broken_wall)
                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (0, 0, 255), broken_wall, 1)

                now = time.monotonic()
                if now - last_spawn >= 50 and frames % 10 and len(pickups) < 3:
                    if random.random() < 0.05:
                        last_spawn = now
                        tag = "health"
                        added_pickup = Pickup(
                            image = pygame.image.load("assets/tanks/Player1.png"),
                            effect = 25,
                            tag = tag

                        )
                        pickups.append(added_pickup)
                
                for pickup in pickups.copy():
                    pickup.draw(screen)
                    if pickup.collides(player_1):
                        player_1.health += pickup.effect
                        pickups.remove(pickup)
                    elif pickup.collides(player_2):
                        player_2.health += pickup.effect
                        pickups.remove(pickup)

                    
                if player_1.health < last_health1:
                    last_health1 = player_1.health
                    hp_bar_health1 = hp_bar_health1.subsurface(
                        pygame.Rect(0, 0, max(int(225 * (player_1.health / 100)), 1), hp_bar_rect1.height)
                    )

                if player_2.health < last_health2:
                    last_health2 = player_2.health
                    hp_bar_health2 = hp_bar_health2.subsurface(
                        pygame.Rect(0, 0, max(int(225 * (player_2.health / 100)), 1), hp_bar_rect2.height)
                    )

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

                    hit_broken_wall = False
                    hit_wall = False
                    for wall in walls:
                        if bullet.collision_rectangle.colliderect(wall):
                            hit_wall = True

                    for _i,broken_wall in enumerate(broken_walls):
                        if bullet.collision_rectangle.colliderect(broken_wall):
                            hit_broken_wall = True
                            i = _i
                        # Check if bullet went off screen
                    if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                        bullet_list1.remove(bullet)
                    
                    if hit_wall:
                        bullet_list1.remove(bullet)
                        if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            explosions.append(explosion)
                        
                    if hit_broken_wall:
                        bullet_list1.remove(bullet)
                        if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            explosions.append(explosion)

                        broken_walls.pop(i)
                    
                    if player_2.collide(bullet.collision_rectangle):
                        bullet_list1.remove(bullet)

                
                #Samma som ovan
                for bullet in reversed(bullet_list2):
                    bullet.move()
                    bullet.draw(screen)

                    hit_broken_wall = False
                    hit_wall = False
                    for wall in walls:
                        if bullet.collision_rectangle.colliderect(wall):
                            hit_wall = True

                    for _i,broken_wall in enumerate(broken_walls):
                        if bullet.collision_rectangle.colliderect(broken_wall):
                            hit_broken_wall = True
                            i = _i
                    if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                        bullet_list2.remove(bullet)

                    if hit_wall:
                        bullet_list2.remove(bullet)
                        if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            explosions.append(explosion)
                    
                    if hit_broken_wall:
                        bullet_list2.remove(bullet)
                        if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            explosions.append(explosion)

                        broken_walls.pop(i)

                    if player_1.collide(bullet.collision_rectangle):
                        bullet_list2.remove(bullet)
                    
                for explosion in explosions:
                    for particle in explosion:
                        particle.update()
                        particle.draw(screen)

                explosions = [[p for p in explosion if p.lifetime > 0] for explosion in explosions]
                explosions = [e for e in explosions if len(e) > 0]
                #Och här så uppdateras hela pygame-skärmen
                frames += 1
                pygame.display.flip()

            #här så stängs pygame och stänger fönstret
            pygame.quit()








        elif ui.get_kind() == "king of hill":
            while game:
                if countdown > 0:
                    for event in pygame.event.get(): ...
                    screen.blit(background, (0, 0))
                    screen.blit(dim, (0, 0))

                    text_surf = other_font.render(f"{countdown-1}".replace("0", "Capture!"), True, (255, 255, 255))
                    screen.blit(text_surf, text_surf.get_rect(center=(width//2, height//2)))

                    pygame.display.flip()
                    countdown -= 1
                    time.sleep(1.0)
                    continue
                
                if not winner is None:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game = False

                    if winner == "player1":
                        screen.blit(win_screen1, ((width - width // 1.4) // 2, (height - height // 1.4) // 2))
                    elif winner == "player2":
                        screen.blit(win_screen2, ((width - width // 1.4) // 2, (height - height // 1.4) // 2))


                    now = time.monotonic()
                    if now - win_time >= 3:
                        game = False
                    pygame.display.flip()
                    continue


                # Funktionerna för att de två spelarna ska kunna röra sig
                player_1.move(walls, broken_walls)
                
                if ui.get_mode() == "solo":
                    # Om det är solo, skicka med målets koordinater (player_1) till AI:n
                    player_2.move(walls, broken_walls, player_1.player1_x, player_1.player1_y)
                else:
                    # Om det är VS, kör vanlig move utan mål
                    player_2.move(walls, broken_walls)
                #Här ritas bakgrunden
                screen.blit(background, (0, 0))
                #Här görs det så att man kan stänga fönstret och döda systemet
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game = False

                if player_1.kingpoints >= 100:
                    winner = "player1"
                    win_time = time.monotonic()
                
                if player_2.kingpoints >= 100:
                    winner = "player2"
                    win_time = time.monotonic()
                keys = pygame.key.get_pressed()
                #Knappbindningarna för att skjuta som spelare 1 och spelare 2, och när de skjuter och lever så läggs det till objekt i de tomma listorna
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

                if ui.get_mode() == "solo" and not player_2.exploded:
                    
                    if bullet_counter2 > 20:
                        # Chans att skjuta (gör den lägre för svårare motstånd, högre för lättare)
                        should_shoot = False
                        
                        # Om vi jagar (är nära), skjut oftare
                        dist_x = abs(player_1.player1_x - player_2.player2_x)
                        dist_y = abs(player_1.player1_y - player_2.player2_y)
                        
                        # Om vi tittar åt rätt håll ungefär
                        if player_2.direction == "LEFT" and player_1.player1_x < player_2.player2_x and dist_y < 50: should_shoot = True
                        elif player_2.direction == "RIGHT" and player_1.player1_x > player_2.player2_x and dist_y < 50: should_shoot = True
                        elif player_2.direction == "UP" and player_1.player1_y < player_2.player2_y and dist_x < 50: should_shoot = True
                        elif player_2.direction == "DOWN" and player_1.player1_y > player_2.player2_y and dist_x < 50: should_shoot = True
                        
                        if should_shoot:
                            shot.play()
                            bullet_list2.append(Bullet(player_2.player2_x + 20, player_2.player2_y, player_2.direction))
                            bullet_counter2 = 0

                #Här så uppdateras varenda objekt i respektive lista
                

                if (player_1.health <= 0) and (not player_1.exploded):
                    player_1.exploded = True
                    dead.play()
                    if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            explosions.append(explosion)
                    

                    hp_bar_health1 = pygame.transform.smoothscale(original_hp_bar_health, (215, 50))
                    last_health1 = 100
                    
                    player_1.health = 0
                    player_1.player1_x = 30
                    player_1.player1_y = (height // 2) - 20
                    last_death1 = time.monotonic()
                    
                if (player_2.health <= 0) and (not player_2.exploded):
                    player_2.exploded = True
                    dead.play()
                    if ui.get_setting("particles"):
                        explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                        explosions.append(explosion)
                    
                    hp_bar_health2 = pygame.transform.smoothscale(original_hp_bar_health, (215, 50))
                    last_health2 = 100

                    player_2.health = 0
                    player_2.player2_x = width - 90
                    player_2.player2_y = (height // 2) - 20
                    last_death2 = time.monotonic()
                #Här konfigueras fps klockan till sextio frames per sekund
                clock.tick(60)#och här läggs det till till räknarna för att det ska gå långsammare att skjuta
                bullet_counter1 = bullet_counter1 + 0.2
                bullet_counter2 = bullet_counter2 + 0.2


                for wall in walls:
                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (255, 0, 0), wall, 1)

                for broken_wall in broken_walls:
                    size = broken_wall.size
                    if size == (86, 28):
                        screen.blit(breakable_wall1, broken_wall)
                    elif size == (28, 80):
                        screen.blit(breakable_wall2, broken_wall)
                    elif size == (84, 28):
                        screen.blit(breakable_wall3, broken_wall)
                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (0, 0, 255), broken_wall, 1)

                now = time.monotonic()
                if now - last_spawn >= 50 and frames % 10 and len(pickups) < 3:
                    if random.random() < 0.05:
                        last_spawn = now
                        tag = "health"
                        added_pickup = Pickup(
                            image = pygame.image.load("assets/tanks/Player1.png"),
                            effect = 25,
                            tag = tag

                        )
                        pickups.append(added_pickup)
                
                for pickup in pickups.copy():
                    pickup.draw(screen)
                    if pickup.collides(player_1):
                        player_1.health += pickup.effect
                        pickups.remove(pickup)
                    elif pickup.collides(player_2):
                        player_2.health += pickup.effect
                        pickups.remove(pickup)

                #Här ritas spelarnas stridsvagnar
                if player_1.health < last_health1:
                    last_health1 = player_1.health
                    hp_bar_health1 = hp_bar_health1.subsurface(
                        pygame.Rect(0, 0, max(int(225 * (player_1.health / 100)), 1), hp_bar_rect1.height)
                    )

                if player_2.health < last_health2:
                    last_health2 = player_2.health
                    hp_bar_health2 = hp_bar_health2.subsurface(
                        pygame.Rect(0, 0, max(int(225 * (player_2.health / 100)), 1), hp_bar_rect2.height)
                    )

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

                now = time.monotonic()
                dx = (player_1.player1_x - center_x)
                dy = (player_1.player1_y - center_y)
                distance1 = math.hypot(dx, dy)
                dx = (player_2.player2_x - center_x)
                dy = (player_2.player2_y - center_y)
                distance2 = math.hypot(dx, dy)
                if distance1 < 100 and not distance2 < 100:
                    pygame.draw.circle(dim2, (200, 200, 255), (100, 100), 100)
                    pygame.draw.circle(dim2, (240, 240, 255), (100, 100), 100, 2)
                    dim2.set_alpha(100)
                    screen.blit(dim2, (center_x - 100, center_y - 100))
                    player_1.draw(screen)
                    player_2.draw(screen)
                    screen.blit(flag_p1, (center_x - 50, center_y - 75))
                    if now - last_kingpoints1 >= 1.0: # Seconds
                        last_kingpoints1 = now
                        player_1.kingpoints += 1
                elif distance2 < 100 and not distance1 < 100:
                    pygame.draw.circle(dim2, (255, 200, 200), (100, 100), 100)
                    pygame.draw.circle(dim2, (255, 240, 240), (100, 100), 100, 2)
                    dim2.set_alpha(100)
                    screen.blit(dim2, (center_x - 100, center_y - 100))
                    player_1.draw(screen)
                    player_2.draw(screen)
                    screen.blit(flag_p2, (center_x - 50, center_y - 75))
                    if now - last_kingpoints2 >= 1.0: # Seconds
                        last_kingpoints2 = now
                        player_2.kingpoints += 1
                else:
                    pygame.draw.circle(dim2, (200, 200, 200), (100, 100), 100)
                    pygame.draw.circle(dim2, (240, 240, 240), (100, 100), 100, 1)
                    dim2.set_alpha(100)
                    screen.blit(dim2, (center_x - 100, center_y - 100))
                    player_1.draw(screen)
                    player_2.draw(screen)
                    screen.blit(flag_p0, (center_x - 50, center_y - 75))

                if player_1.exploded:
                    if now - last_death1 >= 3:
                        player_1.exploded = False
                        player_1.health = 100

                if player_2.exploded:
                    if now - last_death2 >= 3:
                        player_2.exploded = False
                        player_2.health = 100

                
                
                text_surf = primary_font.render(f"{player_1.kingpoints} %", True, (0, 0, 255))
                screen.blit(text_surf, text_surf.get_rect(center=(center_x - 50, 30)))
                text_surf = primary_font.render(f"{player_2.kingpoints} %", True, (255, 0, 0))
                screen.blit(text_surf, text_surf.get_rect(center=(center_x + 50, 30)))

                for bullet in reversed(bullet_list1):
                    bullet.move()
                    bullet.draw(screen)

                    hit_broken_wall = False
                    hit_wall = False
                    for wall in walls:
                        if bullet.collision_rectangle.colliderect(wall):
                            hit_wall = True

                    for _i,broken_wall in enumerate(broken_walls):
                        if bullet.collision_rectangle.colliderect(broken_wall):
                            hit_broken_wall = True
                            i = _i
                    # Check if bullet went off screen
                    if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                        bullet_list1.remove(bullet)
                    
                    if hit_wall:
                        bullet_list1.remove(bullet)
                        if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            explosions.append(explosion)
                        
                    if hit_broken_wall:
                        bullet_list1.remove(bullet)
                        if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            explosions.append(explosion)

                        broken_walls.pop(i)
                    
                    if player_2.collide(bullet.collision_rectangle):
                        bullet_list1.remove(bullet)

                
                #Samma som ovan
                for bullet in reversed(bullet_list2):
                    bullet.move()
                    bullet.draw(screen)

                    hit_broken_wall = False
                    hit_wall = False
                    for wall in walls:
                        if bullet.collision_rectangle.colliderect(wall):
                            hit_wall = True

                    for _i,broken_wall in enumerate(broken_walls):
                        if bullet.collision_rectangle.colliderect(broken_wall):
                            hit_broken_wall = True
                            i = _i
                    if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                        bullet_list2.remove(bullet)

                    if hit_wall:
                        bullet_list2.remove(bullet)
                        if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            explosions.append(explosion)
                    
                    if hit_broken_wall:
                        bullet_list2.remove(bullet)
                        if ui.get_setting("particles"):
                            explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                            explosions.append(explosion)

                        broken_walls.pop(i)

                    if player_1.collide(bullet.collision_rectangle):
                        bullet_list2.remove(bullet)
                    
                for explosion in explosions:
                    for particle in explosion:
                        particle.update()
                        particle.draw(screen)
                    
                for explosion in explosions:
                    for particle in explosion:
                        particle.update()
                        particle.draw(screen)

                explosions = [[p for p in explosion if p.lifetime > 0] for explosion in explosions]
                explosions = [e for e in explosions if len(e) > 0]
                #Och här så uppdateras hela pygame-skärmen
                frames += 1
                pygame.display.flip()

            #här så stängs pygame och stänger fönstret
        
            pygame.quit()


    ui.restart()