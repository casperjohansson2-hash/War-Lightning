#Få tankarna att röra på sig  KLART
#Få dem att skjuta
#Få dom att krocka med hinder
#Gör så att de kan skada varandra med skott
#Splitscreen med minimap







#Importerar
import random
import time
import pygame
import ui

if ui.get_mode() == "exit":
    pygame.quit()
else:
    pygame.init()
    #Skärm inställningar
    width = 1920
    height = 1080
    #Spelarnas stats
    player_health = 100
    def damage():
        chans = random.randint(1, 3)
        if chans == 1:
            player_damage = 20
        else:
            player_damage = 10

        return player_damage

    #Denna delen laddar in de olika sprites, och bakgrunder vi har i spelet
    background = pygame.image.load("C:/War Lightning/assets/tiles/svart.jpg")
    sprite_bullet = pygame.image.load("C:/War Lightning/assets/bullets/bullet.png")
    original_player1 = pygame.image.load("C:/War Lightning/assets/tanks/Player1.png")
    original_player2 = pygame.image.load("C:/War Lightning/assets/tanks/Player2.png")

    sprite_player1 = pygame.transform.smoothscale(original_player1, (original_player1.get_width(), original_player1.get_height()))
    sprite_player2 = pygame.transform.smoothscale(original_player2, (original_player2.get_width(), original_player2.get_height()))
    #Här defineras fps klockan för att begränsa till samma hastighet
    clock = pygame.time.Clock()
    #Det som håller spelet igång och startar upp fönstret
    game = True
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("War Lightning")
    
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
            self.kollision_rectangle = pygame.Rect(self.player1_x, self.player1_y, self.sprite_player1.get_width(), self.sprite_player1.get_height())

        def move(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player_1.health > 0:
                player_1.player1_y -= player_1.speed
                self.sprite_player1 = pygame.transform.rotate(self.original_image, 0)
                self.direction = "UP"
            elif keys[pygame.K_a] and player_1.health > 0:
                player_1.player1_x -= player_1.speed
                self.sprite_player1 = pygame.transform.rotate(self.original_image, 90)
                self.direction = "LEFT"
            elif keys[pygame.K_s] and player_1.health > 0:
                player_1.player1_y += player_1.speed
                self.sprite_player1 = pygame.transform.rotate(self.original_image, 180)
                self.direction = "DOWN"
            elif keys[pygame.K_d] and player_1.health > 0:
                player_1.player1_x += player_1.speed
                self.sprite_player1 = pygame.transform.rotate(self.original_image, 270)
                self.direction = "RIGHT"


            self.kollision_rectangle.topleft = (self.player1_x, self.player1_y)

        def draw(self, screen):
            if not self.exploded:
                screen.blit(self.sprite_player1, (self.player1_x, self.player1_y))
                

                if ui.get_setting("hitboxes"):
                    pygame.draw.rect(screen, (0, 0, 255), self.kollision_rectangle, 2)
             
        def kollidera(self, player1_tank):
            if not player_1.exploded:
                if (self.kollision_rectangle.colliderect(player1_tank)):
                    player_1.exploded = True
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
                self.kollision_rectangle = pygame.Rect(self.player2_x, self.player2_y, self.sprite_player2.get_width(), self.sprite_player2.get_height())

            def move(self):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and player_2.health > 0:
                    player_2.player2_y -= player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 0)
                    self.direction = "UP"
                elif keys[pygame.K_LEFT] and player_2.health > 0:
                    player_2.player2_x -= player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 90)
                    self.direction = "LEFT"
                elif keys[pygame.K_DOWN] and player_2.health > 0:
                    player_2.player2_y += player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 180)
                    self.direction = "DOWN"
                elif keys[pygame.K_RIGHT] and player_2.health > 0:
                    player_2.player2_x += player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 270)
                    self.direction = "RIGHT"


                self.kollision_rectangle.topleft = (self.player2_x, self.player2_y)

            def draw(self, screen):
                if not self.exploded:
                    screen.blit(self.sprite_player2, (self.player2_x, self.player2_y))
                    


                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (0, 0, 255), self.kollision_rectangle, 2)

            def kollidera(self, player2_tank):
                if not player_2.exploded:
                    if (self.kollision_rectangle.colliderect(player2_tank)):
                        player_2.exploded = True
                
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
                self.kollision_rectangle = pygame.Rect(self.player2_x, self.player2_y, self.sprite_player2.get_width(), self.sprite_player2.get_height())

            def move(self):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and player_2.health > 0:
                    player_2.player2_y -= player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 0)
                    self.direction = "UP"
                elif keys[pygame.K_LEFT] and player_2.health > 0:
                    player_2.player2_x -= player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 90)
                    self.direction = "LEFT"
                elif keys[pygame.K_DOWN] and player_2.health > 0:
                    player_2.player2_y += player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 180)
                    self.direction = "DOWN"
                elif keys[pygame.K_RIGHT] and player_2.health > 0:
                    player_2.player2_x += player_2.speed
                    self.sprite_player2 = pygame.transform.rotate(self.original_image, 270)
                    self.direction = "RIGHT"

                self.kollision_rectangle.topleft = (self.player2_x, self.player2_y)

            def draw(self, screen):
                if not self.exploded:
                    screen.blit(self.sprite_player2, (self.player2_x, self.player2_y))
                    


                    if ui.get_setting("hitboxes"):
                        pygame.draw.rect(screen, (0, 0, 255), self.kollision_rectangle, 2)
                
            def kollidera(self, player2_tank):
                if not player_2.exploded:
                    if (self.kollision_rectangle.colliderect(player2_tank)):
                        player_2.exploded = True

    #Klassen för skotten som båda spelarna kan skjuta, och håller koll på hastighet och direktion
    class Bullet:
        def __init__(self, x, y, direction):
            self.x = x
            self.y = y
            self.speed = 10
            self.bild = sprite_bullet
            self.direction = direction

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
    while game:
        #Funktionerna för att de två spelarna ska kunna röra sig
        player_1.move()
        player_2.move()
        #Här ritas bakgrunden
        screen.blit(background, (0, 0))
        #Här görs det så att man kan stänga fönstret och döda systemet
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        #Knappbindningarna för att skjuta som spelare 1 och spelare 2, och när de skjuter och lever så läggs det till objekt i de tomma listorna
        if keys[pygame.K_SPACE]:
            if (bullet_counter1 > 20):
                bullet_list1.append(Bullet(player_1.player1_x + 20, player_1.player1_y, player_1.direction))
                bullet_counter1 = 0

        if keys[pygame.K_RETURN]:
            if (bullet_counter2 > 20):

                bullet_list2.append(Bullet(player_2.player2_x + 20, player_2.player2_y, player_2.direction))
                bullet_counter2 = 0

        #Här så uppdateras varenda objekt i respektive lista
        for bullet in reversed(bullet_list1):
            bullet.move()
            bullet.draw(screen)
            #Och här så ses det till så att om ett skott är utanför spelets ramar så tas de bort
            if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                bullet_list1.remove(bullet)
        #Samma som ovan
        for bullet in reversed(bullet_list2):
            bullet.move()
            bullet.draw(screen)
            #Samma som ovan
            if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
                bullet_list2.remove(bullet)
        #Här konfigueras fps klockan till sextio frames per sekund
        clock.tick(60)#och här läggs det till till räknarna för att det ska gå långsammare att skjuta
        bullet_counter1 = bullet_counter1 + 1
        bullet_counter2 = bullet_counter2 + 1
        #Här ritas spelarnas stridsvagnar
        player_1.draw(screen)
        player_2.draw(screen)
        #Och här så uppdateras hela pygame-skärmen
        pygame.display.flip()

    #här så stängs pygame och stänger fönstret
    pygame.quit()