#Få tankarna att röra på sig  KLART
#Få dem att skjuta KLART
#Få dom att krocka med hinder KLART
#Gör så att de kan skada varandra med skott KLART
#pickups






#Importerar
import random
import time
import pygame
import ui

shot = pygame.mixer.Sound("C:/War Lightning/assets/audio/Tank shot.mp3")
normal_hit = pygame.mixer.Sound("C:/War Lightning/assets/audio/Metal hit.mp3")
crit_hit = pygame.mixer.Sound("C:/War Lightning/assets/audio/Metal pierce.mp3")
dead = pygame.mixer.Sound("C:/War Lightning/assets/audio/Tank kaboom.mp3")
pygame.mixer.music.load("assets/audio/Match start.mp3")
pygame.mixer.music.play()
volume = ui.get_setting("volume")
pygame.mixer.music.set_volume(volume)

color_list = [(255, 50, 50), (255, 150, 50), (255, 255, 50)]
explosions = []

if ui.get_mode() == "exit":
    pygame.quit()
else:
    pygame.init()
    #Skärm inställningar
    width = 1920
    height = 1080
    #Spelarnas stats
    player_health = 100
    

    #Denna delen laddar in de olika sprites, och bakgrunder vi har i spelet
    original_background = pygame.image.load("C:/War Lightning/assets/tiles/map1.png")
    original_bullet = pygame.image.load("C:/War Lightning/assets/bullets/bullet.png")
    original_player1 = pygame.image.load("C:/War Lightning/assets/tanks/Player1.png")
    original_player2 = pygame.image.load("C:/War Lightning/assets/tanks/Player2.png")
    


    background = pygame.transform.smoothscale(original_background, (width, height))
    sprite_bullet = pygame.transform.smoothscale(original_bullet, (original_bullet.get_width() + 1, original_bullet.get_height() + 1))
    sprite_player1 = pygame.transform.smoothscale(original_player1, (original_player1.get_width(), original_player1.get_height()))
    sprite_player2 = pygame.transform.smoothscale(original_player2, (original_player2.get_width(), original_player2.get_height()))
    #Här defineras fps klockan för att begränsa till samma hastighet
    clock = pygame.time.Clock()
    #Det som håller spelet igång och startar upp fönstret
    game = True
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
            self.player1_y = height // 2
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
            
            
            self.offset_x = (self.sprite_player1.get_width() - hitbox_width) // 2
            self.offset_y = (self.sprite_player1.get_height() - hitbox_height) // 2
            
            
            self.collision_rectangle = pygame.Rect(
                self.player1_x + self.offset_x, 
                self.player1_y + self.offset_y, 
                hitbox_width, 
                hitbox_height
            )

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
            self.collision_rectangle.x = self.player1_x
            
            self.collision_rectangle.x = self.player1_x + self.offset_x
            
            for wall in walls:
                if self.collision_rectangle.colliderect(wall):
                    if dx > 0: 
                        self.collision_rectangle.right = wall.left
                    if dx < 0: 
                        self.collision_rectangle.left = wall.right
                    
                    
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
    if ui.get_mode() == "solo":
        class Player2:
            def __init__(self):
                self.player2_x = width - 30
                self.player2_y = height // 2
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
            
            
                self.offset_x = (self.sprite_player2.get_width() - hitbox_width) // 2
                self.offset_y = (self.sprite_player2.get_height() - hitbox_height) // 2
                
                
                self.collision_rectangle = pygame.Rect(
                    self.player2_x + self.offset_x, 
                    self.player2_y + self.offset_y, 
                    hitbox_width, 
                    hitbox_height
                )

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
                self.collision_rectangle.x = self.player2_x
                
                self.collision_rectangle.x = self.player2_x + self.offset_x
                
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if dx > 0: 
                            self.collision_rectangle.right = wall.left
                        if dx < 0: 
                            self.collision_rectangle.left = wall.right
                        
                        
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
                
    elif ui.get_mode() == "vs":
        class Player2:
            def __init__(self):
                self.player2_x = width - 30
                self.player2_y = height // 2
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
            
            
                self.offset_x = (self.sprite_player2.get_width() - hitbox_width) // 2
                self.offset_y = (self.sprite_player2.get_height() - hitbox_height) // 2
                
                
                self.collision_rectangle = pygame.Rect(
                    self.player2_x + self.offset_x, 
                    self.player2_y + self.offset_y, 
                    hitbox_width, 
                    hitbox_height
                )

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
                self.collision_rectangle.x = self.player2_x
                
                self.collision_rectangle.x = self.player2_x + self.offset_x
                
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if dx > 0: 
                            self.collision_rectangle.right = wall.left
                        if dx < 0: 
                            self.collision_rectangle.left = wall.right
                        
                        
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
    class Bullet:
        def __init__(self, x, y, direction):
            self.x = x
            self.y = y
            self.speed = 20
            self.bild = sprite_bullet
            self.direction = direction
            self.collision_rectangle = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())
            self.collision = False

            if self.direction == "LEFT":
                self.bild = pygame.transform.rotate(sprite_bullet, 90)
            elif self.direction == "DOWN":
                self.bild = pygame.transform.rotate(sprite_bullet, 180)
            elif self.direction == "RIGHT":
                self.bild = pygame.transform.rotate(sprite_bullet, -90)


        def move(self):
            if self.direction == "UP":
                self.y -= self.speed
            elif self.direction == "DOWN":
                self.y += self.speed
            elif self.direction == "LEFT":
                self.x -= self.speed
            elif self.direction == "RIGHT":
                self.x += self.speed

            self.collision_rectangle.topleft = (self.x, self.y)

        def draw(self, screen):
            if self.direction == "UP" or self.direction == "DOWN":
                screen.blit(self.bild, (self.x + 8, self.y))
            else:
                screen.blit(self.bild, (self.x, self.y + 28))

        

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

    primary_font = pygame.font.Font("assets/fonts/SEEKUW.ttf", 20)
    other_font = pygame.font.Font("assets/fonts/SEEKUW.ttf", 100)
    dim = pygame.Surface((width, height), pygame.SRCALPHA)
    dim.fill((50, 50, 50, 150))
    countdown = 4
    # Här defineras de två spelarna utifrån deras klasser
    player_1 = Player1()
    player_2 = Player2()
    #Och här definieras skott räknarna som gör att man inte kan skjuta för snabbt
    bullet_counter1 = 0
    bullet_counter2 = 0
    #Listor som håller koll på de olika objekten som avfyrats från båda spelarna under en runda
    bullet_list1 = []
    bullet_list2 = []
    #Main spel loopen där hela spelet händer och där alla funktioner och all logik uppdateras och genomförs.
    #All kollision

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
        pygame.Rect(1135, 860, 28, 86),
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
        pygame.Rect(60, 479, 172, 28),
    ]
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
            
            
            #Funktionerna för att de två spelarna ska kunna röra sig
            player_1.move(walls)
            player_2.move(walls)
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

            #Här så uppdateras varenda objekt i respektive lista
            

            if player_1.health < 0 or player_1.health == 0:
                player_1.exploded = True
                dead.play()
                if ui.get_setting("particles"):
                        explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                        
                        explosions.append(explosion)
                #######################
                player_1.health = 100##
                player_2.health = 100##
                #######################
            if player_2.health < 0 or player_2.health == 0:
                player_2.exploded = True
                dead.play()
                #######################
                player_1.health = 100##
                player_2.health = 100##
                #######################
            #Här konfigueras fps klockan till sextio frames per sekund
            clock.tick(60)#och här läggs det till till räknarna för att det ska gå långsammare att skjuta
            bullet_counter1 = bullet_counter1 + 0.2
            bullet_counter2 = bullet_counter2 + 0.2


            for wall in walls:
                pygame.draw.rect(screen, (255, 0, 0), wall, 1)
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
            player_1.draw(screen)
            player_2.draw(screen)

            for bullet in reversed(bullet_list1):
                bullet.move()
                bullet.draw(screen)
                
                hit_wall = False
                for wall in walls:
                    if bullet.collision_rectangle.colliderect(wall):
                        hit_wall = True
                # Check if bullet went off screen
                if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                    bullet_list1.remove(bullet)
                
                if hit_wall:
                    bullet_list1.remove(bullet)
                    if ui.get_setting("particles"):
                        explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                        explosions.append(explosion)

                
                
                elif player_2.collide(bullet.collision_rectangle):
                    bullet_list1.remove(bullet)

            
            #Samma som ovan
            for bullet in reversed(bullet_list2):
                bullet.move()
                bullet.draw(screen)

                hit_wall = False
                for wall in walls:
                    if bullet.collision_rectangle.colliderect(wall):
                        hit_wall = True
                if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                    bullet_list2.remove(bullet)

                if hit_wall:
                    bullet_list2.remove(bullet)
                    if ui.get_setting("particles"):
                        explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                        explosions.append(explosion)
                
                
                elif player_1.collide(bullet.collision_rectangle):
                    bullet_list2.remove(bullet)
                
            for explosion in explosions:
                for particle in explosion:
                    particle.update()
                    particle.draw(screen)

            explosions = [[p for p in explosion if p.lifetime > 0] for explosion in explosions]
            explosions = [e for e in explosions if len(e) > 0]
            #Och här så uppdateras hela pygame-skärmen
            pygame.display.flip()

        #här så stängs pygame och stänger fönstret
        pygame.quit()
    elif ui.get_kind() == "king of hill":
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
            
            
            #Funktionerna för att de två spelarna ska kunna röra sig
            player_1.move(walls)
            player_2.move(walls)
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

            #Här så uppdateras varenda objekt i respektive lista
            

            if player_1.health < 0 or player_1.health == 0:
                player_1.exploded = True
                dead.play()
                if ui.get_setting("particles"):
                        explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                        
                        explosions.append(explosion)
                #######################
                player_1.health = 100##
                player_2.health = 100##
                #######################
            if player_2.health < 0 or player_2.health == 0:
                player_2.exploded = True
                dead.play()
                #######################
                player_1.health = 100##
                player_2.health = 100##
                #######################
            #Här konfigueras fps klockan till sextio frames per sekund
            clock.tick(60)#och här läggs det till till räknarna för att det ska gå långsammare att skjuta
            bullet_counter1 = bullet_counter1 + 0.2
            bullet_counter2 = bullet_counter2 + 0.2


            for wall in walls:
                pygame.draw.rect(screen, (255, 0, 0), wall, 1)
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
            player_1.draw(screen)
            player_2.draw(screen)

            for bullet in reversed(bullet_list1):
                bullet.move()
                bullet.draw(screen)
                
                hit_wall = False
                for wall in walls:
                    if bullet.collision_rectangle.colliderect(wall):
                        hit_wall = True
                # Check if bullet went off screen
                if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                    bullet_list1.remove(bullet)
                
                if hit_wall:
                    bullet_list1.remove(bullet)
                    if ui.get_setting("particles"):
                        explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                        explosions.append(explosion)

                
                
                elif player_2.collide(bullet.collision_rectangle):
                    bullet_list1.remove(bullet)

            
            #Samma som ovan
            for bullet in reversed(bullet_list2):
                bullet.move()
                bullet.draw(screen)

                hit_wall = False
                for wall in walls:
                    if bullet.collision_rectangle.colliderect(wall):
                        hit_wall = True
                if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                    bullet_list2.remove(bullet)

                if hit_wall:
                    bullet_list2.remove(bullet)
                    if ui.get_setting("particles"):
                        explosion = [Particle(bullet.x, bullet.y) for _ in range(100)]
                        explosions.append(explosion)
                
                
                elif player_1.collide(bullet.collision_rectangle):
                    bullet_list2.remove(bullet)
                
            for explosion in explosions:
                for particle in explosion:
                    particle.update()
                    particle.draw(screen)

            explosions = [[p for p in explosion if p.lifetime > 0] for explosion in explosions]
            explosions = [e for e in explosions if len(e) > 0]
            #Och här så uppdateras hela pygame-skärmen
            pygame.display.flip()

        #här så stängs pygame och stänger fönstret
        pygame.quit()