import pygame
import math


class GoldMine:
    def __init__(self, pos, screen, color, gold=50, image_path='Images/Gold.png', scale=0.3,
                 health=300, max_health=300, price=200):
        self.health = health
        self.max_health = max_health
        self.price = price
        self.pos = pos
        self.gold_amount = gold
        self.color = color

        self.img = pygame.image.load(image_path)

        # Scale the image
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.img = pygame.transform.scale(self.img, (int(self.width * scale), int(self.height * scale)))

        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = pos
        self.screen = screen
        self.hitbox = pygame.Rect(self.pos[0]+3, self.pos[1]+8, 40, 40)  # Hitbox area for the units

    def draw(self):
        """
        Draws the unit with the given images
        """
        self.hitbox = pygame.Rect(self.pos[0]+3, self.pos[1]+8, 70, 70) 
        self.screen.blit(self.img, self.rect)

    def draw_health_bar(self):
        """
        draw health bar above unit
        :return: None
        """
        def draw_health_bar(screen, pos, size, borderC, backC, healthC, progress):
            pygame.draw.rect(screen, backC, (*pos, *size))
            pygame.draw.rect(screen, borderC, (*pos, *size), 1)
            innerPos = (pos[0] + 1, pos[1] + 1)
            innerSize = ((size[0] - 2) * progress, size[1] - 2)
            rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
            pygame.draw.rect(screen, healthC, rect)

        health_rect = pygame.Rect(0, 0, self.img.get_width(), 7)
        health_rect.midbottom = self.rect.centerx, self.rect.top
        x, y, z = self.color
        draw_health_bar(self.screen, health_rect.topleft, health_rect.size, x, y, z, self.health/self.max_health)

    def remove(self):
        """
        Make the unit disappear from the game.
        """
        self.screen.fill((255, 255, 255))

    def addGold(self, player):
        player.gold += self.gold_amount

    def move(self, x, y):
        """
        moves tower to given x and y
        :param x: int
        :param y: int
        :return: None
        """
        self.pos = (x, y)
        self.updateRect()

    def updateRect(self):
        self.rect.x, self.rect.y = self.pos

    @staticmethod
    def getType():
        return "GoldMine"

    def reduceHealth(self, damage):
        """
        Reduce health. If the health is not enough, delete.
        :param damage: enemy damage
        :return: None
        """
        if self.health - damage > 0:
            self.health -= damage
        else:
            self.health = 0

    def collide(self, movingObject):
        x2 = movingObject.pos[0]
        y2 = movingObject.pos[1]
        dis = math.sqrt((x2 - self.pos[0]) ** 2 + (y2 - self.pos[1]) ** 2)
        if dis >= 100:
            return False
        else:
            return True

    @property
    def isInappropriate(self) -> bool:
        if self.pos[0] > 600 - 25 or self.pos[1] > 600 - 35 or self.pos[0] < 50 or self.pos[1] < 50:
            return True
        return False
        
