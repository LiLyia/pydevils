from __future__ import annotations
import pygame
""" 
    This document is created to implement Tower class it will be called in gameEngine class and it will be
     inherited by other tower classes. 
    @author = Harun Eren MUTLU
"""
DEFAULT_TOWER_PRICE: int = 100
DEFAULT_TOWER_HEALTH: int = 100
DEFAULT_HIT: int = 1
DEFAULT_UPGRADE_PERCENT: float = 0.15
DEFAULT_LEVEL: int = 0
DEFAULT_SCALE = 0.09


class Tower:
    '''
    This class created to implement the Base Tower
    '''
    @classmethod
    def createTower(cls, pos: tuple[int], image_list: list[list[pygame.Surface]], screen: pygame.Surface) -> Tower:
        '''
        This method is written to create a Tower class without reaching it directly
        :param pos: tuple[int]
        :param image_list: list[list[pygame.Surface]]
        :param screen: pygame.Surface
        :return: Tower
        '''
        return cls(pos=pos, image_list=image_list, screen= screen)

    def __init__(self, pos: tuple[int],
                 image_list: list[list[pygame.Surface]],
                 screen: pygame.Surface,
                 scale: float = DEFAULT_SCALE,
                 price: int = DEFAULT_TOWER_PRICE,
                 health: int = DEFAULT_TOWER_HEALTH,
                 max_health: int = DEFAULT_TOWER_HEALTH,
                 level: int = DEFAULT_LEVEL
                 ):
        self.image_list = image_list
        self._screen = screen
        self._price: int = price
        self._health: int = health
        self._max_health: int = max_health
        self._level: int = level
        self._health_level: int = None
        self.declareHealthLevel()
        temp_image: pygame.Surface = image_list[self.getLevel][self.getHealthLevel]
        self._towerImage: pygame.Surface = self.scaleImage(temp_image, scale)

        self._rect = self.getTowerImage.get_rect()
        self._rect.x, self._rect.y = pos

    def setHealth(self, health: int) -> None:
        '''
        Sets the health
        :param health: int
        :return:
        '''
        self._health = health

    def setMaxHealth(self, max_health: int) -> None:
        '''
        Sets the Maximum health of tower
        :param max_health: int
        :return:
        '''
        self._max_health = max_health

    def setPrice(self, price: int) -> None:
        '''
        Sets the price of tower
        :param price: int
        :return:
        '''
        self._price = price

    def setLevel(self, level: int) -> None:
        '''
        Sets the level of tower
        :param level: int
        :return:
        '''
        self._level = level

    def setHealthLevel(self, health_level: int) -> None:
        '''
        Sets the Health level of tower
        :param health_level: int
        :return:
        '''
        self._health_level = health_level

    @property
    def getHealth(self) -> int:
        '''
        Returns the health of tower
        :return: int
        '''
        return self._health

    @property
    def getMaxHealth(self) -> int:
        '''
        Returns the maximum health of tower
        :return: int
        '''
        return self._max_health

    @property
    def getPrice(self) -> int:
        '''
        Returns the price of tower
        :return: int
        '''
        return self._price

    @property
    def getLevel(self) -> int:
        '''
        Returns the level of tower
        :return: int
        '''
        return self._level

    @property
    def getHealthLevel(self) -> int:
        '''
        Returns the health level of tower
        :return: int
        '''
        return self._health_level

    @property
    def getScreen(self) -> pygame.Surface:
        '''
        Returns the screen of the game
        :return:
        '''
        return self._screen

    @property
    def getTowerList(self) -> list[list[pygame.Surface]]:
        '''
        Returns the list of possible Towers
        :return: list[list[pygame.Surface]]
        '''
        return self.image_list

    @property
    def getTowerImage(self) -> pygame.Surface:
        '''
        Returns the image of tower
        :return: pygame.Surface
        '''
        return self.scaleImage(self.getTowerList[self.getLevel][self.getHealthLevel])

    @property
    def getRect(self) -> pygame.Rect:
        '''
        Returns the position of tower
        :return:pygame.Rect
        '''
        return self._rect

    def reduceHealth(self, reduce_amount: int = DEFAULT_HIT) -> None:
        '''
        The function that makes tower take a hit
        :param reduce_amount: int
        :return:
        '''
        self.setHealth(self.getHealth - reduce_amount)
        self.declareHealthLevel()

    def isDead(self) -> bool:
        '''
        The function that checks if the tower is that or not
        :return: bool
        '''
        return not self.getHealth > 0

    def upgrade(self, upgrade_percent: float = DEFAULT_UPGRADE_PERCENT):
        '''
        The function that upgrades the attributes of tower
        :param upgrade_percent: float
        :return:
        '''
        self.setLevel(self.getLevel + 1)
        self.setMaxHealth(self.getMaxHealth * (1 + upgrade_percent))
        self.setHealth(self.getHealth * (1 + upgrade_percent))
        self.declareHealthLevel()

    def remove(self):
        '''
        Function that removes the tower
        :return:
        '''
        pass

    def declareHealthLevel(self) -> int:
        '''
        The function that generates health level to be able to choose correct tower image according to tower health
        :return: int
        '''
        if self.getHealth > self.getMaxHealth/2:
            self.setHealthLevel(0)
        elif self.getHealth > self.getMaxHealth/4:
            self.setHealthLevel(1)
        else:
            self.setHealthLevel(2)

    def scaleImage(self, img: pygame.Surface, scale: float = DEFAULT_SCALE) -> pygame.Surface:
        '''
        The function that scales tower image according to some scale
        :param img: pygame.Surface
        :param scale: float
        :return: pygame.Surface
        '''
        width = img.get_width()
        height = img.get_height()
        return pygame.transform.scale(img, (int(width * scale), int(height * scale)))

    def draw_tower(self) -> None:
        '''
        The function for drawing the tower to the map
        :return:
        '''
        self.getScreen.blit(self.getTowerImage, self.getRect)