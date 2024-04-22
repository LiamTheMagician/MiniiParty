import pygame
import sys
from random import choice, randint, randrange
import pygame.math as math
import MainSettings as ms

pygame.init()

screen = pygame.display.set_mode((ms.LONGUEUR, ms.HAUTEUR))
clock = pygame.time.Clock()

#Classes
class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y, left_key, right_key, up_key, down_key, scale_factor):
        super().__init__()
        self.image = pygame.image.load ('images/joueur.png')
        self.image = pygame.transform.scale_by(self.image, scale_factor)
        self.rect = self.image.get_rect(center = (x, y))

        self.velocity = math.Vector2(0, 0)
        self.acceleration = 0.1
        self.max_speed = 4
        self.vertical_speed = 1.1

        self.left_key = left_key
        self.right_key = right_key
        self.up_key = up_key
        self.down_key = down_key

    def input(self):
        keys = pygame.key.get_pressed()
        self.move_direction = math.Vector2(0, 0)

        if keys[self.left_key]:
            self.move_direction.x -= 1
        if keys[self.right_key]:
            self.move_direction.x += 1
        if keys[self.up_key]:
            self.move_direction.y -= 1
        if keys[self.down_key]:
            self.move_direction.y += 1
        
        if self.move_direction.length() >= 1:
            self.move_direction.normalize_ip()

        return self.move_direction

    def move(self):
        self.velocity += self.move_direction * self.acceleration

        #Don't go over max speed
        if self.velocity.length() >= self.max_speed:
            self.velocity.scale_to_length(self.max_speed)


        if pygame.sprite.spritecollideany(self, groupe_asteroid):
            self.move_direction.reflect_ip(self.move_direction)
        
        #Apply velocity
        self.rect.move_ip(self.velocity.x, self.velocity.y)


    def update(self):
        self.input()
        self.move()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_factor, velocity):
        super().__init__()
        self.image = pygame.image.load('images/asteroid.png')
        self.image = pygame.transform.scale_by(self.image, scale_factor)
        self.rect = self.image.get_rect(center = (x, y))

        self.velocity = velocity

    def movement(self):
        self.rect.x += self.velocity

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.movement()
        self.destroy()
        

#Instance Joueurs
JoueurUn = Joueur(ms.LONGUEUR/4, 50, pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s, 0.35)
JoueurDeux = Joueur(ms.LONGUEUR - ms.LONGUEUR/4, 50, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, 0.35)

#Instance Asteroid
AsteroidTest = Asteroid(200,240, 1,  0)

#Groupe
groupe_joueur = pygame.sprite.Group()
groupe_joueur.add(JoueurUn, JoueurDeux)
#--------------------------------------
groupe_asteroid = pygame.sprite.Group()
groupe_asteroid.add(AsteroidTest)

#Evenement spawn asteroid
asteroid_spawn = pygame.USEREVENT + 2
asteroid_timer = pygame.time.set_timer(asteroid_spawn, 500)
asteroid_x = [ms.LONGUEUR+60, ms.LONGUEUR+250, ms.LONGUEUR+400, ms.LONGUEUR+550, ms.LONGUEUR+700]

space_evaders = True
while space_evaders:

    screen.fill((0,0,0))


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

    groupe_joueur.draw(screen)
    groupe_joueur.update()

    groupe_asteroid.draw(screen)
    groupe_asteroid.update()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
