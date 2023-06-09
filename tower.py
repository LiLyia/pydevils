from __future__ import annotations
import pygame
import math
""" 
    This document is created to implement Tower class it will be called in gameEngine class and it will be
     inherited by other tower classes. 
    @author = Harun Eren MUTLU
"""
DEFAULT_TOWER_PRICE: int = 100
DEFAULT_TOWER_HEALTH: int = 600
DEFAULT_HIT: int = 1
DEFAULT_UPGRADE_PERCENT: float = 0.5
DEFAULT_LEVEL: int = 0
DEFAULT_SCALE = 0.09
DEFAULT_MAXUPGRADE: int = 3


class Tower:
    """
    This class created to implement the Base Tower
    """
    @classmethod
    def createTower(cls, pos: tuple[int, int], image_list: list[list[pygame.Surface]],
                    screen: pygame.Surface, color: list[tuple[int, int, int]]) -> Tower:
        """
        This method is written to create a Tower class without reaching it directly
        :param pos: tuple[int]
        :param image_list: list[list[pygame.Surface]]
        :param screen: pygame.Surface
        :param color: list[tuple[int, int, int]]
        :return: Tower
        """
        return cls(pos=pos, image_list=image_list, screen=screen, color=color)

    def __init__(self, pos: tuple[int, int],
                 image_list: list[list[pygame.Surface]],
                 screen: pygame.Surface,
                 color: list[tuple[int, int, int]],
                 scale: float = DEFAULT_SCALE,
                 price: int = DEFAULT_TOWER_PRICE,
                 health: int = DEFAULT_TOWER_HEALTH,
                 max_health: int = DEFAULT_TOWER_HEALTH,
                 level: int = DEFAULT_LEVEL,
                 max_up: int = DEFAULT_MAXUPGRADE

                 ):
        self.image_list = image_list
        self._screen = screen
        self._price: int = price
        self._health: int = health
        self._max_health: int = max_health
        self._level: int = level
        self._health_level: int = 0
        temp_image: pygame.Surface = image_list[self.level][self.healthLevel]
        self._towerImage: pygame.Surface = self.scaleImage(temp_image, scale)
        self._max_up = max_up

        self._pos: tuple[int, int] = pos
        self._rect: pygame.Rect = self.towerImage.get_rect()
        self._rect.x, self._rect.y = pos
        self._hitbox = pygame.Rect(self._pos[0]-35, self._pos[1]-15, 100, 100)
        self.color = color

    def setHealth(self, health: int) -> None:
        """
        Sets the health
        :param health: int
        :return:
        """
        self._health = health

    def setMaxHealth(self, max_health: int) -> None:
        """
        Sets the Maximum health of tower
        :param max_health: int
        :return:
        """
        self._max_health = max_health

    def setMaxUp(self, max_up: int) -> None:
        """
        Sets the Maximum health of tower
        :param max_up: int
        :return:
        """
        self._max_up = max_up

    def setPrice(self, price: int) -> None:
        """
        Sets the price of tower
        :param price: int
        :return:
        """
        self._price = price

    def setLevel(self, level: int) -> None:
        """
        Sets the level of tower
        :param level: int
        :return:
        """
        self._level = level

    def setHealthLevel(self, health_level: int) -> None:
        """
        Sets the Health level of tower
        :param health_level: int
        :return:
        """
        self._health_level = health_level

    @property
    def health(self) -> int:
        """
        Returns the health of tower
        :return: int
        """
        return self._health

    @property
    def maxHealth(self) -> int:
        """
        Returns the maximum health of tower
        :return: int
        """
        return self._max_health

    @property
    def maxUp(self) -> int:
        """
        Returns the maximum health of tower
        :return: int
        """
        return self._max_up

    @property
    def price(self) -> int:
        """
        Returns the price of tower
        :return: int
        """
        return self._price

    @property
    def level(self) -> int:
        """
        Returns the level of tower
        :return: int
        """
        return self._level

    @property
    def healthLevel(self) -> int:
        """
        Returns the health level of tower
        :return: int
        """
        return self._health_level

    @property
    def screen(self) -> pygame.Surface:
        """
        Returns the screen of the game
        :return:
        """
        return self._screen

    @property
    def towerList(self) -> list[list[pygame.Surface]]:
        """
        Returns the list of possible Towers
        :return: list[list[pygame.Surface]]
        """
        return self.image_list

    @property
    def towerImage(self) -> pygame.Surface:
        """
        Returns the image of tower
        :return: pygame.Surface
        """
        return self.scaleImage(self.towerList[self.level][self.healthLevel])

    @property
    def rect(self) -> pygame.Rect:
        """
        Returns the Rect of tower
        :return:pygame.Rect
        """
        return self._rect

    @property
    def pos(self) -> tuple[int, int]:
        """
        Returns the position of tower
        :return: tuple[int]
        """
        return self._pos

    @property
    def hitbox(self) -> int:
        """
        Returns the hitbox
        :return: pygame.Rect
        """
        return self._hitbox

    def reduceHealth(self, reduce_amount: int = DEFAULT_HIT) -> None:
        """
        The function that makes tower take a hit
        :param reduce_amount: int
        :return: None
        """
        self.setHealth(self.health - reduce_amount)
        self.declareHealthLevel()

    def isDead(self) -> bool:
        """
        The function that checks if the tower is that or not
        :return: bool
        """
        return not self.health > 0

    def upgrade(self, upgrade_percent: float = DEFAULT_UPGRADE_PERCENT):
        """
        The function that upgrades the attributes of tower
        :param upgrade_percent: float
        :return:
        """
        if self.maxUp == 0:
            return False
        self.setMaxUp(self.maxUp - 1)
        self.setMaxHealth(int(self.maxHealth * (1 + upgrade_percent)))
        self.setHealth(int(self.health * (1 + upgrade_percent)))
        self.draw_health_bar()
        return True

    def remove(self) -> None:
        """
        Function that removes the tower
        :return:
        """
        self._screen.fill((255, 255, 255))  # Temporary deletion

    def declareHealthLevel(self) -> None:
        """
        The function that generates health level to be able to choose correct tower image according to tower health
        :return: int
        """
        if self.health > self.maxHealth/2:
            self.setHealthLevel(0)
        elif self.health > self.maxHealth/4:
            self.setHealthLevel(1)
        else:
            self.setHealthLevel(2)

    @staticmethod
    def scaleImage(img: pygame.Surface, scale: float = DEFAULT_SCALE) -> pygame.Surface:
        """
        The function that scales tower image according to some scale
        :param img: pygame.Surface
        :param scale: float
        :return: pygame.Surface
        """
        
        width = img.get_width()
        height = img.get_height()
        return pygame.transform.scale(img, (int(width * scale), int(height * scale)))

    def draw_tower(self) -> None:
        """
        The function for drawing the tower to the map
        :return: None
        """
        self._hitbox = pygame.Rect(self._pos[0] - 35, self._pos[1] - 25, 100, 100)
        self.screen.blit(self.towerImage, self.rect)

    def move(self, x, y):
        """
        moves tower to given x and y
        :param x: int
        :param y: int
        :return: None
        """
        self._pos = (x, y)
        self.updateRect()
        self.updateHitBox()

    def collide(self, remainObject):
        """
        Checks if the towers collide or not.
        :return: bool
        """
        x2 = remainObject.pos[0]
        y2 = remainObject.pos[1]
        dis = math.sqrt((x2 - self.pos[0]) ** 2 + (y2 - self.pos[1]) ** 2)
        if dis >= 100:
            return False
        else:
            return True

    def updateRect(self):
        """
        Changes the _rect.
        :return: None
        """
        self.rect.x, self.rect.y = self.pos
    
    def updateHitBox(self):
        """
        Changes the _hitbox.
        :return: None
        """
        self._hitbox = pygame.Rect(self._pos[0]-35, self._pos[1]-15, 100, 100)

    @staticmethod
    def getType():
        """
        Returns the class name.
        :return: string
        """
        return "BasicTower"

    def draw_health_bar(self):
        """
        draw health bar above object
        :return: None
        """
        def draw_health_bar(screen, pos, size, borderC, backC, healthC, progress):
            pygame.draw.rect(screen, backC, (*pos, *size))
            pygame.draw.rect(screen, borderC, (*pos, *size), 1)
            innerPos = (pos[0] + 1, pos[1] + 1)
            innerSize = ((size[0] - 2) * progress, size[1] - 2)
            rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
            pygame.draw.rect(screen, healthC, rect)
        
        health_rect = pygame.Rect(0, 0, self.towerImage.get_width() + self.maxHealth/10, 7)
        health_rect.midbottom = self.rect.centerx, self.rect.top
        x, y, z = self.color
        draw_health_bar(self.screen, health_rect.topleft, health_rect.size, x, y, z, self.health/self.maxHealth)

    @property
    def isInappropriate(self) -> bool:
        """
        Checks if the position is correct.
        :return: bool
        """
        if self.pos[0] > 600 - 25 or self.pos[1] > 600 - 35 or self.pos[0] < 50 or self.pos[1] < 50:
            return True
        return False
