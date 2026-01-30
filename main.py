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
original_player1 = pygame.image.load("C:/War Lightning/assets/tanks/Player1.jpg")
original_player2 = pygame.image.load("C:/War Lightning/assets/tanks/Player2.jpg")

sprite_player1 = pygame.transform.scale(original_player1, (original_player1.get_width() // 2, original_player1.get_height() // 2))
sprite_player2 = pygame.transform.scale(original_player2, (original_player2.get_width() // 2, original_player2.get_height() // 2))
clock = pygame.time.Clock()

game = True
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("War Lightning")


class Player1:
    def __init__(self):
        self.player1_x = width // 2 - 120
        self.player1_y = height - 200
        self.sprite_player1 = sprite_player1
        self.health = player_health
        self.damage = damage()
        self.speed = 5


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_1.health > 0:
            player_1.player1_y -= player_1.speed
        elif keys[pygame.K_a] and player_1.health > 0:
            player_1.player1_x -= player_1.speed
        elif keys[pygame.K_s] and player_1.health > 0:
            player_1.player1_y += player_1.speed
        elif keys[pygame.K_d] and player_1.health > 0:
            player_1.player1_x += player_1.speed


    
class Player2:
    def __init__(self):
        self.player2_x = width // 2 - 120
        self.player2_y = height - 200
        self.sprite_player2 = sprite_player2
        self.health = player_health
        self.damage = damage()
        self.speed = 5


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_2.health > 0:
            player_2.player2_y -= player_2.speed
        elif keys[pygame.K_LEFT] and player_2.health > 0:
            player_2.player2_x -= player_2.speed
        elif keys[pygame.K_DOWN] and player_2.health > 0:
            player_2.player2_y += player_2.speed
        elif keys[pygame.K_RIGHT] and player_2.health > 0:
            player_2.player2_x += player_2.speed


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.bild = sprite_bullet


    def flytta(self):
        self.y = self.y - self.speed

    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))


player_1 = Player1()
player_2 = Player2()



bullet_list = []
while game:
    
    player_1.move()
    player_2.move()
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    screen.fill((0, 0, 0))

    clock.tick(60)
    screen.blit(sprite_player1, (player_1.player1_x, player_1.player1_y))
    screen.blit(sprite_player2, (player_2.player2_x, player_2.player2_y))
    pygame.display.flip()
pygame.QUIT()