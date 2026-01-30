#Få tankarna att röra på sig  KLART
#Få dem att skjuta
#Få dom att krocka med hinder
#Gör så att de kan skada varandra med skott
#Splitscreen med minimap







#Importerar
import random
import time
import pygame

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


background = pygame.image.load("C:/War Lightning/assets/tiles/svart.jpg")
sprite_bullet = pygame.image.load("C:/War Lightning/assets/bullets/bullet.jpg")
original_player1 = pygame.image.load("C:/War Lightning/assets/tanks/Player1.png")
original_player2 = pygame.image.load("C:/War Lightning/assets/tanks/Player2.png")

sprite_player1 = pygame.transform.smoothscale(original_player1, (original_player1.get_width(), original_player1.get_height()))
sprite_player2 = pygame.transform.smoothscale(original_player2, (original_player2.get_width(), original_player2.get_height()))
clock = pygame.time.Clock()

game = True
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("War Lightning")


class Player1:
    def __init__(self):
        self.player1_x = width - 1980
        self.player1_y = height // 2
        self.sprite_player1 = sprite_player1
        self.health = player_health
        self.damage = damage()
        self.speed = 2
        self.original_image = sprite_player1
        self.sprite_player1 = self.original_image
        self.direction = "UP"

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


    
class Player2:
    def __init__(self):
        self.player2_x = width // 2 
        self.player2_y = height // 2
        self.sprite_player2 = sprite_player2
        self.health = player_health
        self.damage = damage()
        self.speed = 2
        self.direction = "UP"
        self.original_image = sprite_player2
        self.sprite_player2 = self.original_image

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
        screen.blit(self.bild, (self.x, self.y))


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

player_1 = Player1()
player_2 = Player2()

bullet_counter1 = 0
bullet_counter2 = 0

bullet_list1 = []
bullet_list2 = []
while game:
    
    player_1.move()
    player_2.move()
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if (bullet_counter1 > 20):
            bullet_list1.append(Bullet(player_1.player1_x + 20, player_1.player1_y, player_1.direction))
            bullet_counter1 = 0

    if keys[pygame.K_RETURN]:
        if (bullet_counter2 > 20):

            bullet_list2.append(Bullet(player_2.player2_x + 20, player_2.player2_y, player_2.direction))
            bullet_counter2 = 0

    for bullet in reversed(bullet_list1):
        bullet.move()
        bullet.draw(screen)

        if bullet.y < -100:
            bullet_list1.remove(bullet)

    for bullet in reversed(bullet_list2):
        bullet.move()
        bullet.draw(screen)

        if bullet.y < 0 or bullet.y > 1140 or bullet.x < 0 or bullet.x > 1980:
            bullet_list2.remove(bullet)
    clock.tick(60)
    bullet_counter1 = bullet_counter1 + 1
    bullet_counter2 = bullet_counter2 + 1
    screen.blit(player_1.sprite_player1, (player_1.player1_x, player_1.player1_y))
    screen.blit(player_2.sprite_player2, (player_2.player2_x, player_2.player2_y))
    pygame.display.flip()
pygame.quit()