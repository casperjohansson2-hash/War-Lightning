#Få tankarna att röra på sig  KLART
#Få dem att skjuta
#Få dom att krocka med hinder
#Gör så att de kan skada varandra med skott
#Splitscreen med minimap







#Importerar
import random
import time
import pygame
import math
import ui

shot = pygame.mixer.Sound("C:/War Lightning/assets/audio/Tank shot.mp3")
normal_hit = pygame.mixer.Sound("C:/War Lightning/assets/audio/Metal hit.mp3")
crit_hit = pygame.mixer.Sound("C:/War Lightning/assets/audio/Metal pierce.mp3")
pygame.mixer.music.load("assets/audio/Match start.mp3")
pygame.mixer.music.play()
volume = ui.get_setting("volume")
pygame.mixer.music.set_volume(volume)
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
    sprite_bullet = pygame.image.load("C:/War Lightning/assets/bullets/bullet.png")
    original_player1 = pygame.image.load("C:/War Lightning/assets/tanks/Player1.png")
    original_player2 = pygame.image.load("C:/War Lightning/assets/tanks/Player2.png")
    

    background = pygame.transform.smoothscale(original_background, (width, height))
    sprite_player1 = pygame.transform.smoothscale(original_player1, (original_player1.get_width(), original_player1.get_height()))
    sprite_player2 = pygame.transform.smoothscale(original_player2, (original_player2.get_width(), original_player2.get_height()))
    #Här defineras fps klockan för att begränsa till samma hastighet
    clock = pygame.time.Clock()
    #Det som håller spelet igång och startar upp fönstret
    game = True
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
    


    #Klasserna för spelare 1 och spelare 2 som innehåller deras hälsa, skada, olika lägen, hastighet och alla deras funktioner
    class Player1:
        def __init__(self):
            self.player1_x = width // 2
            self.player1_y = height // 2
            self.sprite_player1 = sprite_player1
            self.health = player_health
            self.damage = damage()
            self.speed = 1
            self.original_image = sprite_player1
            self.sprite_player1 = self.original_image
            self.direction = "UP"
            self.exploded = False
            self.collision_rectangle = pygame.Rect(self.player1_x, self.player1_y, self.sprite_player1.get_width(), self.sprite_player1.get_height())

            self.kingpoints = 0

        def move(self, walls):
            right_collision = False
            left_collision = False
            down_collision = False
            up_collision = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player_1.health > 0 and up_collision != True:
                player_1.player1_y -= player_1.speed
                self.sprite_player1 = pygame.transform.rotate(self.original_image, 0)
                self.direction = "UP"
            elif keys[pygame.K_a] and player_1.health > 0 and left_collision != True:
                player_1.player1_x -= player_1.speed
                self.sprite_player1 = pygame.transform.rotate(self.original_image, 90)
                self.direction = "LEFT"
            elif keys[pygame.K_s] and player_1.health > 0 and down_collision != True:
                player_1.player1_y += player_1.speed
                self.sprite_player1 = pygame.transform.rotate(self.original_image, 180)
                self.direction = "DOWN"
            elif keys[pygame.K_d] and player_1.health > 0 and right_collision != True:
                player_1.player1_x += player_1.speed
                self.sprite_player1 = pygame.transform.rotate(self.original_image, 270)
                self.direction = "RIGHT"

            self.collision_rectangle.x += player_1.speed
            for wall in walls:
                if self.collision_rectangle.colliderect(wall):
                    if self.direction == "RIGHT":  
                        right_collision = True
                        left_collision = False
                        down_collision = False
                        up_collision = False
                    elif self.direction == "LEFT":  
                        right_collision = False
                        left_collision = True
                        down_collision = False
                        up_collision = False

            
            self.collision_rectangle.y += player_1.speed
            for wall in walls:
                if self.collision_rectangle.colliderect(wall):
                    if self.direction == "DOWN":  
                        right_collision = False
                        left_collision = False
                        down_collision = True
                        up_collision = False
                    elif self.direction == "UP":  
                        right_collision = False
                        left_collision = False
                        down_collision = False
                        up_collision = True

            self.collision_rectangle.topleft = (self.player1_x // 2, self.player1_y // 2)

        def draw(self, screen):
            if not self.exploded:
                screen.blit(self.sprite_player1, (self.player1_x, self.player1_y))
                

                if ui.get_setting("hitboxes"):
                    pygame.draw.rect(screen, (0, 0, 255), self.collision_rectangle, 2)
             
        def collide(self, bullet_rect):
            if not player_1.exploded:
                if self.collision_rectangle.colliderect(bullet_rect):
                    player_1.health -= damage()
                    return True 
            return False 
    if ui.get_mode() == "solo":
        class Player2:
            def __init__(self):
                self.player2_x = width // 2 
                self.player2_y = height // 2
                self.sprite_player2 = sprite_player2
                self.health = player_health
                self.damage = damage()
                self.speed = 1
                self.direction = "UP"
                self.exploded = False
                self.original_image = sprite_player2
                self.sprite_player2 = self.original_image
                self.collision_rectangle = pygame.Rect(self.player2_x, self.player2_y, self.sprite_player2.get_width(), self.sprite_player2.get_height())

                self.kingpoints = 0

            def move(self, walls):
                keys = pygame.key.get_pressed()
                right_collision = False
                left_collision = False
                down_collision = False
                up_collision = False
                if keys[pygame.K_UP] and player_2.health > 0 and up_collision != True:
                    player_2.player2_y -= player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 0)
                    self.direction = "UP"
                elif keys[pygame.K_LEFT] and player_2.health > 0 and left_collision != True:
                    player_2.player2_x -= player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 90)
                    self.direction = "LEFT"
                elif keys[pygame.K_DOWN] and player_2.health > 0 and down_collision != True:
                    player_2.player2_y += player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 180)
                    self.direction = "DOWN"
                elif keys[pygame.K_RIGHT] and player_2.health > 0 and right_collision != True:
                    player_2.player2_x += player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 270)
                    self.direction = "RIGHT"

                self.collision_rectangle.x += player_2.speed
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if self.direction == "RIGHT":  
                            right_collision = True
                            left_collision = False
                            down_collision = False
                            up_collision = False
                        elif self.direction == "LEFT":  
                            right_collision = False
                            left_collision = True
                            down_collision = False
                            up_collision = False

                
                self.collision_rectangle.y += player_2.speed
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if self.direction == "DOWN":  
                            right_collision = False
                            left_collision = False
                            down_collision = True
                            up_collision = False
                        elif self.direction == "UP":  
                            right_collision = False
                            left_collision = False
                            down_collision = False
                            up_collision = True

                self.collision_rectangle.topleft = (self.player2_x, self.player2_y)

            def draw(self, screen):
                if not self.exploded:
                    screen.blit(self.sprite_player2, (self.player2_x, self.player2_y))
                    


                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (0, 0, 255), self.collision_rectangle, 2)

            def collide(self, bullet_rect):
                if not player_2.exploded:
                    if self.collision_rectangle.colliderect(bullet_rect):
                        player_2.health -= damage()
                        return True 
                return False 
                
    elif ui.get_mode() == "vs":
        class Player2:
            def __init__(self):
                self.player2_x = width // 2 
                self.player2_y = height // 2
                self.sprite_player2 = sprite_player2
                self.health = player_health
                self.damage = damage()
                self.speed = 1
                self.direction = "UP"
                self.exploded = False
                self.original_image = sprite_player2
                self.sprite_player2 = self.original_image
                self.collision_rectangle = pygame.Rect(self.player2_x, self.player2_y, self.sprite_player2.get_width(), self.sprite_player2.get_height())

                self.kingpoints = 0

            def move(self, walls):
                keys = pygame.key.get_pressed()
                right_collision = False
                left_collision = False
                down_collision = False
                up_collision = False
                if keys[pygame.K_UP] and player_2.health > 0 and up_collision != True:
                    player_2.player2_y -= player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 0)
                    self.direction = "UP"
                elif keys[pygame.K_LEFT] and player_2.health > 0 and left_collision != True:
                    player_2.player2_x -= player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 90)
                    self.direction = "LEFT"
                elif keys[pygame.K_DOWN] and player_2.health > 0 and down_collision != True:
                    player_2.player2_y += player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 180)
                    self.direction = "DOWN"
                elif keys[pygame.K_RIGHT] and player_2.health > 0 and right_collision != True:
                    player_2.player2_x += player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 270)
                    self.direction = "RIGHT"

                self.collision_rectangle.x += player_2.speed
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if self.direction == "RIGHT":  
                            right_collision = True
                            left_collision = False
                            down_collision = False
                            up_collision = False
                        elif self.direction == "LEFT":  
                            right_collision = False
                            left_collision = True
                            down_collision = False
                            up_collision = False

                
                self.collision_rectangle.y += player_2.speed
                for wall in walls:
                    if self.collision_rectangle.colliderect(wall):
                        if self.direction == "DOWN":  
                            right_collision = False
                            left_collision = False
                            down_collision = True
                            up_collision = False
                        elif self.direction == "UP":  
                            right_collision = False
                            left_collision = False
                            down_collision = False
                            up_collision = True

                self.collision_rectangle.topleft = (self.player2_x, self.player2_y)

            def draw(self, screen):
                if not self.exploded:
                    screen.blit(self.sprite_player2, (self.player2_x, self.player2_y))
                    


                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (0, 0, 255), self.collision_rectangle, 2)
                
            def collide(self, bullet_rect):
                if not player_2.exploded:
                    if self.collision_rectangle.colliderect(bullet_rect):
                        player_2.health -= damage()
                        return True 
                return False 

    #Klassen för skotten som båda spelarna kan skjuta, och håller koll på hastighet och direktion
    class Bullet:
        def __init__(self, x, y, direction):
            self.x = x
            self.y = y
            self.speed = 10
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
    
    class Pickup:
        def __init__(self, image, effect, tag):
            self.x = random.randint(0, width)
            self.y = random.randint(0, height)
            self.image = image # pygame.image.load()
            self.effect = effect # 0 -> 1000 ?
            self.tag = tag # "health" el. "strength"
        
        def collides(self, player):
            return player.collisionrectangle.collidesrect(self.image.get_rect(topleft=(self.x, self.y)))
        
        def draw(self, screen):
            screen.blit(self.image, (self.x, self.y))
    
    primary_font = pygame.font.Font("assets/fonts/SEEKUW.ttf", 25)
    other_font = pygame.font.Font("assets/fonts/SEEKUW.ttf", 100)
    dim = pygame.Surface((width, height), pygame.SRCALPHA)
    dim.fill((50, 50, 50, 150))

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

    center_x = width//2
    center_y = height//2

    last_kingpoints1 = 0.0
    last_kingpoints2 = 0.0

    frames = 0

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
    walls = [
        pygame.Rect(10, 0, 50, height),
    ]
    pickups = [

    ]

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
        for bullet in reversed(bullet_list1):
            bullet.move()
            bullet.draw(screen)
            
            # Check if bullet went off screen
            if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                bullet_list1.remove(bullet)
            
            
            elif player_2.collide(bullet.collision_rectangle):
                bullet_list1.remove(bullet)

           
        #Samma som ovan
        for bullet in reversed(bullet_list2):
            bullet.move()
            bullet.draw(screen)

            if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                bullet_list2.remove(bullet)
            
            
            elif player_1.collide(bullet.collision_rectangle):
                bullet_list2.remove(bullet)
        

        for wall in walls:
            pygame.draw.rect(screen, (255, 0, 0), wall, 1)
        
        if frames % 10 == 0:
            if random.random() < 0.25: # (25%)
                pickups.append(Pickup(...))
            

        if player_1.health < 0:
            player_1.exploded = True

        if player_2.health < 0:
            player_2.exploded = True
        #Här konfigueras fps klockan till sextio frames per sekund
        clock.tick(60)#och här läggs det till till räknarna för att det ska gå långsammare att skjuta
        bullet_counter1 = bullet_counter1 + 0.5
        bullet_counter2 = bullet_counter2 + 0.5
        #Här ritas spelarnas stridsvagnar
        player_1.draw(screen)
        player_2.draw(screen)

        now = time.monotonic()
        dx = (player_1.player1_x - center_x)
        dy = (player_1.player1_y - center_y)
        distance1 = math.sqrt(dx ** 2 + dy ** 2) if dx != 0 and dy != 0 else 0
        dx = (player_2.player2_x - center_x)
        dy = (player_2.player2_y - center_y)
        distance2 = math.sqrt(dx ** 2 + dy ** 2) if dx != 0 and dy != 0 else 0

        if distance1 < 100 and not distance2 < 100:
            if now - last_kingpoints1 >= 1.0: # Seconds
                last_kingpoints1 = now
                player_1.kingpoints += 1
        
        if distance2 < 100 and not distance1 < 100:
            if now - last_kingpoints2 >= 1.0: # Seconds
                last_kingpoints2 = now
                player_2.kingpoints += 1

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

        text_surf = primary_font.render(f"{player_1.kingpoints} pts", True, (255, 255, 255))
        screen.blit(text_surf, text_surf.get_rect(center=(center_x - 50, 30)))
        text_surf = primary_font.render(f"{player_2.kingpoints} pts", True, (255, 255, 255))
        screen.blit(text_surf, text_surf.get_rect(center=(center_x + 50, 30)))

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
        #Och här så uppdateras hela pygame-skärmen
        pygame.display.flip()
        frames += 1

    #här så stängs pygame och stänger fönstret
    pygame.quit()