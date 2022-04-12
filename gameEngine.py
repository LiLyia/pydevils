import pygame
from pygame.locals import *
from castle import Castle
from game_map import GameMap
from tower import *
from unit import Unit
from FireTower import *
from imageCreator import *
import menu
import random


# -----------Colors------------------------#

WHITE = (255, 255, 255)

# ------------------game------------------#
screen = pygame.init()
SCREEN_HEIGHT, SCREEN_WIDTH = 650, 850
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Defence Tower")
#  -----------Adjusting the Frame of the Game------------#
clock = pygame.time.Clock()
FPS = 60
# -----------BG Image---------------------#
bg_img = pygame.image.load("Images/Background/bg_1.png")

#--------------SideMenu--------------------
imager = ImageCreator.createImageCreator('Images')
sideMenu = menu.VerticalMenu(750, 120, pygame.transform.scale(pygame.image.load('Images/menu.png').convert_alpha(), (200, 650)))
sideMenu.add_btn(imager.getTowerImage(0, 0, 0), "Basic", 500)
sideMenu.add_btn(imager.getTowerImage(0, 1, 0), "FireTower", 600)
#sideMenu.add_btn(imager.getTowerImage(2, 2, 0), "SlowingTower", 800)

# -------------castle-class-----------------------
# image of castle1 with 100% health
castle1_100_img = pygame.image.load('Images/Castle/castle1_100.png').convert_alpha()
# image of castle1 with 50% health
castle1_50_img = pygame.image.load('Images/Castle/castle1_50.png').convert_alpha()
# image of castle1 with 25% health
castle1_25_img = pygame.image.load('Images/Castle/castle1_25.png')
# image of castle2 with 100% health
castle2_100_img = pygame.image.load('Images/Castle/castle2_100.png').convert_alpha()
# image of castle2 with 50% health
castle2_50_img = pygame.image.load('Images/Castle/castle2_50.png').convert_alpha()
# image of castle2 with 25% health
castle2_25_img = pygame.image.load('Images/Castle/castle2_25.png')
# declearing tower positions
tower_pos = [(150, 150), (200, 200), (300, 300), (400, 400), (200, 500)]
position_tower = random.choice(tower_pos)
position_tower_2 = random.choice(tower_pos)
while position_tower_2 == position_tower:
    position_tower_2 = random.choice(tower_pos)

# creating towers
tower_images = [[pygame.image.load('Images/Towers/tower1.png'),pygame.image.load('Images/Towers/tower2.png'),pygame.image.load('Images/Towers/tower3.png')],[None,None,None],[None,None,None]]
fire_tower_images = [[pygame.image.load('Images/Towers/firetower.png'),pygame.image.load('Images/Towers/firetower.png'),pygame.image.load('Images/Towers/firetower.png')],[None,None,None],[None,None,None]]

tower1 = Tower.createTower(position_tower, tower_images, screen)
tower_2 = Tower.createTower(position_tower_2, tower_images, screen)
tower_2.setHealth(14)
tower_2.declareHealthLevel()

# randomly picking the position of castle 1 position
castle1_pos = [(150, 100), (200, 100), (250, 100), (300, 100), (350, 100), (400, 100), (450, 100)]
position_castle1 = random.choice(castle1_pos)
# randomly picking the position of castle 2 position
castle2_pos = [(150, 450), (200, 450), (250, 450), (300, 450), (350, 450), (400, 450), (450, 450)]
position_castle2 = random.choice(castle2_pos)
castle1 = Castle(castle1_100_img,castle1_50_img,castle1_25_img, position_castle1, 0.09, screen)
castle2 = Castle(castle2_100_img,castle2_50_img,castle2_25_img, position_castle2, 0.09, screen)


#soldier = Unit((100, 400),screen,'Images/soldier.png', 0.07 )
# ------------creating grid for game map --------------#
tile_size = 50
# def create_grid():
#     for line in range(13):
#         pygame.draw.line(screen, WHITE, (0, line*tile_size), (SCREEN_WIDTH, line* tile_size))
#         pygame.draw.line(screen,WHITE, (line*tile_size, 0),(line * tile_size,SCREEN_HEIGHT))

# -----------------Game Map---------------------
game_map_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 5, 4, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
    [1, 0, 2, 2, 0, 0, 0, 0, 0, 3, 2, 0, 1],
    [1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
game_map = GameMap(game_map_data, tile_size, screen)
# make sure screen continue
towers = []
units =[]
position_of_towers = []
position_of_units = []
soldier = Unit((150,200),screen,'Images/Units/soldier.png',0.04)
#towers.append(tower_2)
is_game = True
moving_object = None
#Draw bullets
def displayBullets(building_list):
    for b in building_list:
        if type(b) == FireTower:
            for p in b.bulletList:
                pygame.draw.rect(screen, (255,0,0), (p.x, p.y, 4, 4))
#Clear the bullets from the map.If bullets hits or miss the enemy , they will be deleted.
def clearBullets(towerList):
    for i in towerList:
        if type(i) == FireTower:
            for j in i.bulletList:
                if j.hitEnemy == True:
                    i.bulletList.remove(j)
                if i.current_target == None:
                    i.bulletList.remove(j)

def clearMonsters(unit_list):
    for e in unit_list:
        if e.health <= 0:
            unit_list.remove(e)
# Get the target for each tower in the list of targetable units.

def findTargetforTowers(unit_list, tower_list):
    for b in tower_list:
        if type(b) == FireTower:
            b.targetList = []
            for m in unit_list:
                if b.hitbox.colliderect(m.hitbox) == True:
                    b.targetList.append(m)

# Get the target for each tower in the list of targetable units.
def currentTowerTarget(building_list):
    for b in building_list:
        if type(b) == FireTower:
            for m in b.targetList:
                if b.current_target == None:
                   b.current_target = m
                   if b.current_target.health < 0:
                        print("Yes")
                        b.targetList.remove(m)
                if b.current_target.pos[0] <= m.pos[0]:
                    b.current_target = m

            if len(b.targetList) == 0:
               b.current_target = None

#If tower detects an enemy , this function will be activated and shoot to the enemies.

def shootTowers(towerList):
    for i in towerList:
        if type(i) == FireTower:
            if i.current_target != None:
                i.shoot()
                if i.current_target.health <0:
                    i.current_target = None

def add_tower(name, screen):
    global moving_object
    global obj
    x, y = pygame.mouse.get_pos()
    name_list = ["Basic", "FireTower"]
    object_list = [Tower.createTower((x, y), tower_images, screen), FireTower.createTower((x, y), fire_tower_images, screen)]

    try:
        obj = object_list[name_list.index(name)]
        moving_object = obj
        obj.moving = True
    except Exception as e:
        print(str(e) + "NOT VALID NAME")

while is_game:
    clock.tick(FPS)
    screen.blit(bg_img, (0, 0))
    castle1.draw_castle()
    castle2.draw_castle()
    sideMenu.draw(screen)
    # create_grid()
    game_map.draw_tiles()
    pos = pygame.mouse.get_pos()
    if moving_object:
        moving_object.move(pos[0], pos[1])
        collide = False
        for tower in towers:
            if tower.collide(moving_object):
                collide = True
    for event in pygame.event.get():
        if event.type == QUIT:
            is_game = False
        elif event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
            if moving_object:
                not_allowed = False
                for tower in towers:
                    if tower.collide(moving_object):
                        not_allowed = True

                if not not_allowed:
                    towers.append(moving_object)

                    moving_object.moving = False
                    moving_object = None
            # adds position to list
            if event.button == 1 :
                for tower in towers:
                    if ( -4 > tower.pos[0] - event.pos[0] > -23 ) and (-5 >tower.pos[1] - event.pos[1] > -38):
                        towers.remove(tower)

            elif event.button == 3:
                if (600 > event.pos[0] > 50) and (600 > event.pos[1] > 50):
                    soldier = Unit(event.pos,screen,'Images/soldier.png',0.04)
                    position_of_units.append(soldier.pos)
                    units.append(soldier)


            elif event.button == 2:
                if (600 > event.pos[0] > 50) and (600 > event.pos[1] > 50):
                    fire_towerBuy = FireTower.createTower(event.pos,fire_tower_images,screen)
                    towers.append(fire_towerBuy)
            else :
                if (600>event.pos[0] >50) and (600>event.pos[1] >50) :
                    towerBuy = Tower.createTower(event.pos, tower_images, screen)
                    towers.append(towerBuy)
            print(pygame.mouse.get_pos())

        # draw images at positions
        if event.type == MOUSEBUTTONDOWN:
            side_menu_button = sideMenu.get_clicked(event.pos[0], event.pos[1])
            if side_menu_button:
                add_tower(side_menu_button, screen)


    findTargetforTowers(units,towers)
    currentTowerTarget(towers)

    shootTowers(towers)
    for tower in towers:
        tower.draw_tower()
    for unit in units:
        unit.draw()

    displayBullets(towers)
    clearBullets(towers)
    clearMonsters(units)




    pygame.display.flip()

    pygame.display.update()
pygame.quit()
