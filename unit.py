from __future__ import annotations
import pygame
from projectile import Projectile

"""
Unit class, functions as a 'Basic Unit' and is the base class of all the units.
Only the position and the screen is required to create it.
"""


class Unit:
    def __init__(self, pos, screen, image_path='Images/basic.png', scale=0.07, health=800, max_health=800, price=100):
        self.health = health
        self.max_health = max_health
        self.price = price
        self.pos = pos
        self.img = pygame.image.load(image_path)

        # Scale the image
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.img = pygame.transform.scale(self.img, (int(self.width * scale), int(self.height * scale)))

        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = pos
        self.screen = screen
        self.hitbox = pygame.Rect(self.pos[0]+3, self.pos[1]+8, 40, 40) #Hitbox area for the units
    def move(self):
        """
        Make the unit move only 1 block according to the path it has.
        """
        goal_pos = self.findPath(self.pos)
        if goal_pos != self.pos:
            self.pos = goal_pos
            self.rect = self.img.get_rect()
            self.rect.x, self.rect.y = self.pos

    def heal(self):
        """
        Extra feature that can be added afterwards
        """
        if (self.health + 100) <= self.max_health:
            self.health += 100
        else:
            self.health = self.max_health

    def get_pos(self):
        """
        :return pos: Current position of the unit
        """
        return self.pos

    def reduceHealth(self, enemy):
        """
        Reduce health. If the health is not enough, delete.
        :param enemy: type of Unit
        :return: None
        """
        if self.health - enemy.damage > 0:
            self.health -= enemy.damage
        else:
            self.delete()

    def draw(self):
        """
        Draws the unit with the given images
        """
        self.screen.blit(self.img, self.rect)

    def draw_health_bar(self, win):
        """
        draw health bar above unit
        :param win: surface...unit_position?
        :return: None
        """
        length = 50
        move_by = round(length / self.max_health)
        health_bar = move_by * self.health

        pygame.draw.rect(win, (255, 0, 0), (self.rect.x - 30, self.rect.y - 75, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.rect.x - 30, self.rect.y - 75, health_bar, 10), 0)

    def remove(self):
        """
        Make the unit disappear from the game.
        """
        self.screen.fill((255, 255, 255))

    def findPath(self, castle_pos):
        """
        Take the current position, calculate the shortest path possible to the enemy castle from the game map.
        :param castle_pos: the position of the enemy castle
        :return next available step's coordinates
        """
        pass

    """"
    def train(self, img, scale):
        self.max_health += 200
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
    """


"""
AttackingUnit Class is a superclass for UvsU, UvsB and UvsO and also subclass of Unit. 
Includes attacking function.
"""


class AttackingUnit(Unit):
    def __init__(self, pos, screen, image_path, scale,
                 health=800,
                 max_health=800,
                 price=100,
                 damage=50,
                 attack_range=50):

        self.damage = damage
        self.attack_range = attack_range
        Unit.__init__(self, pos, screen, image_path, scale, health, max_health, price)

    def attack(self, type):
        """
        Attack and reduceHealth of the enemy if is in attack_range.
        :param enemy: is of type Unit.
        :return: None
        """
        if self.current_cd <= 0 and self.current_target != None:
            self.attackList.append(Projectile(self.pos[0],self.pos[1],self.current_target,self.damage))
            self.current_cd = self.cd
        else:
            self.current_cd -= 1
        for e in self.attackList:
            if type == UvsB:
                if self.current_target != None:
                    e.hitTower()
            else:
                if self.current_target != None:
                    e.hitEnemy()


"""
 UvsU is subclass of AttackingUnit. Meaning UnitvsUnit, it can attack and destroy the enemy units.
"""


class UvsU(AttackingUnit):
    def __init__(self, pos, screen, image_path='Images/uvsu.png', scale=0.07):
        super().__init__(pos, screen, image_path, scale, 500, 500, 100, 50, 50)


"""
 UvsB is subclass of AttackingUnit. Meaning UnitvsBuilding, it can attack and destroy enemy towers.
"""


class UvsB(AttackingUnit):

    def __init__(self, pos, screen, image_path='Images/uvsb.png', scale=0.07):
        super().__init__(pos, screen, image_path, scale, 800, 800, 150, 50, 50)


"""
 UvsO is subclass of AttackingUnit. Meaning UnitvsObstacle, it can attack and destroy the obstacles
"""


class UvsO(AttackingUnit):
    def __init__(self, pos, screen, image_path='Images/uvso', scale=0.07):
        super().__init__(pos, screen, image_path, scale, 800, 400, 100, 50, 50)
