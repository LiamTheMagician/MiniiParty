import pygame
import sys
import MainSettings as ms

pygame.init()
screen = pygame.display.set_mode((ms.LONGUEUR, ms.HAUTEUR))
clock = pygame.time.Clock()

#___Variables jeu tonneau___
victoire_un = False
victoire_deux = False

tonneau_un_collided = False
tonneau_deux_collided = False

end_check = False
distance_list = []
restartable = False
start_game_event = pygame.USEREVENT + 1
pygame.time.set_timer(start_game_event, 1000)
timer = 5
wait = True

#Fonctions
def texte(texte_string, taille, couleur, x, y):
    my_font = pygame.font.Font('font/game_font.ttf', taille)
    text_surface = my_font.render(texte_string, False, couleur)
    text_rect = text_surface.get_rect(center = (x, y))
    screen.blit(text_surface, text_rect)

def distance():
    global distance_list
    distance_joueur_un = 0
    distance_joueur_deux = 0

    distance_joueur_un = JoueurUn.rect.top - TonneauUn.rect.bottom
    distance_joueur_deux = JoueurDeux.rect.top - TonneauDeux.rect.bottom

    distance_list = [distance_joueur_un, distance_joueur_deux]

def condition_victoire():
    global victoire_un, victoire_deux, end_check, distance_list, tonneau_un_collided, tonneau_deux_collided

    if pygame.sprite.spritecollide(JoueurUn, groupe_tonneau, True):
        tonneau_un_collided = True
        TonneauUn.espace = True
        
    if pygame.sprite.spritecollide(JoueurDeux, groupe_tonneau, True):
        tonneau_deux_collided = True
        TonneauDeux.espace = True

    if tonneau_un_collided == True and tonneau_deux_collided == True:
            victoire_un = False
            victoire_deux = False
            end_check = True

    if TonneauUn.espace == True and TonneauDeux.espace == True:
        if distance_list[0]<distance_list[1] and tonneau_un_collided == False and tonneau_deux_collided == False:
            victoire_un = True
            victoire_deux = False
            end_check = True

        elif distance_list[0]>distance_list[1] and tonneau_un_collided == False and tonneau_deux_collided == False:
            victoire_un = False
            victoire_deux = True
            end_check = True

        elif distance_list[0]<distance_list[1] and tonneau_un_collided:
            victoire_un = False
            victoire_deux = True
            end_check = True

        elif distance_list[0]>distance_list[1] and tonneau_deux_collided:
            victoire_un = True
            victoire_deux = False
            end_check = True

        elif distance_list[0]==distance_list[1] and tonneau_un_collided == False and tonneau_deux_collided == False:
            victoire_un = True
            victoire_deux = True
            end_check = True

def restart_tonneau():
    global victoire_un, victoire_deux, end_check, tonneau_un_collided, tonneau_deux_collided, restartable, secondes
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r] and restartable == True:
        tonneau_un_collided = False
        tonneau_deux_collided = False

        if victoire_un == False or victoire_deux == False:
            groupe_tonneau.empty()
            groupe_tonneau.add(TonneauUn)
            groupe_tonneau.add(TonneauDeux)

        victoire_un = False
        victoire_deux = False

        TonneauUn.gravite = 0
        TonneauDeux.gravite = 0

        TonneauUn.rect.center = (220, 40)
        TonneauDeux.rect.center = (860-220, 40)

        TonneauUn.espace = False
        TonneauDeux.espace = False

        restartable = False
        end_check = False

#Classes
class Tonneau(pygame.sprite.Sprite):
    def __init__(self, x, y, stop_key):
        super().__init__()
        
        self.image = pygame.image.load('images/tonneau.png')
        self.rect = self.image.get_rect(center = (x, y))
        self.gravite = 0
        self.espace = False
        self.stop_key = stop_key
        self.distance_list = []

    def application_gravite(self):
        keys = pygame.key.get_pressed()

        if keys[self.stop_key]:
            self.espace = True

        if self.espace == False:
            self.gravite += 0.2
            self.rect.y += self.gravite

        if self.espace == True:
            self.gravite = 0
            self.rect.y += self.gravite

    def update(self):
        #self.distance()
        self.application_gravite()

class JoueurTonneau(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('images/joueur.png')
        self.rect = self.image.get_rect(center = (x, y))

#Groupes
groupe_tonneau = pygame.sprite.Group()
groupe_joueur = pygame.sprite.Group()

#Instances
TonneauUn = Tonneau(220, 40, pygame.K_a)
TonneauDeux = Tonneau(860-220, 40, pygame.K_SPACE)

JoueurUn = JoueurTonneau(220,400)
JoueurDeux = JoueurTonneau(860-220,400)

#Ajouter au groupe
groupe_tonneau.add(TonneauUn, TonneauDeux)
groupe_joueur.add(JoueurUn, JoueurDeux)

tonneau_casse_cou = True
while tonneau_casse_cou:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == start_game_event:
            if timer >= 0:
                timer -= 1
            
    restart_tonneau()

    #Groupes Joueur 1
    groupe_tonneau.draw(screen)
    groupe_joueur.draw(screen)

    groupe_tonneau.update()
    groupe_joueur.update()


    if timer != 0:
        if restartable == False:
            texte(f"{timer}", 30, (255,255,255), 430, 240)
            
        TonneauUn.espace = False
        TonneauUn.gravite = 0

        TonneauDeux.espace = False
        TonneauDeux.gravite = 0

    if end_check == False and restartable == False:
        condition_victoire()
        
    else:
        restartable = True
        timer = 5
        texte("Recommencer? [R]", 15, (150,150,150), 430, 320)
        if victoire_un == True and victoire_deux == True:
            texte("Egalité!", 30, (255,255,255), 430, 240)
        elif victoire_un and victoire_deux == False:
            texte(f"Joueur 1 à gagné! {distance_list[0]/50}m", 30, (255,255,255), 430, 240)
        elif victoire_deux and victoire_un == False:
            texte(f"Joueur 2 à gagné! {distance_list[1]/50}m", 30, (255,255,255), 430, 240)
        elif victoire_un == False and victoire_deux == False:
            texte("Perdu!", 30, (255,255,255), 430, 240)
            
    if TonneauUn.gravite != 0 or TonneauDeux.gravite != 0:
        distance()

    pygame.display.update()
    clock.tick(60)
pygame.exit()

