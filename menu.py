import pygame
pygame.font.init()


class Button:
    """
    Button class for menu objects
    """
    def __init__(self, menu, img, name):
        self.name = name
        self.img = img
        self.x = menu.x - 50
        self.y = menu.y - 110
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def click(self, X, Y):
        """
        returns if the positon has collided with the menu
        :param X: int
        :param Y: int
        :return: bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def draw(self, win):
        """
        draws the button image
        :param win: surface
        :return: None
        """
        win.blit(self.img, (self.x, self.y))

    def update(self):
        """
        updates button position
        :return: None
        """
        self.x = self.menu.x - 50
        self.y = self.menu.y - 110


class PlayPauseButton(Button):
    def __init__(self, play_img, pause_img, x, y):
        self.img = play_img
        self.play = play_img
        self.pause = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.paused = True

    def draw(self, win):
        if self.paused:
            win.blit(self.play, (self.x, self.y))
        else:
            win.blit(self.pause, (self.x, self.y))


class VerticalButton(Button):
    """
    Button class for menu objects
    """
    def __init__(self, x, y, img, name, cost):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cost = cost


class Menu:
    """
    menu for holding items
    """
    def __init__(self, tower, x, y, img, item_cost):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.item_cost = item_cost
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("comicsans", 25)
        self.tower = tower

    def add_btn(self, img, name):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """
        self.items += 1
        self.buttons.append(Button(self, img, name))

    def get_item_cost(self):
        """
        gets cost of upgrade to next level
        :return: int
        """
        return self.item_cost[self.tower.level - 1]

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """
        win.blit(self.bg, (self.x - self.bg.get_width()/2, self.y-120))
        for item in self.buttons:
            item.draw(win)
            text = self.font.render(str(self.item_cost[self.tower.level - 1]), 1, (255,255,255))
            win.blit(text, (item.x + item.width + 30 - text.get_width()/2, item.y -8))

    def get_clicked(self, X, Y):
        """
        return the clicked item from the menu
        :param X: int
        :param Y: int
        :return: str
        """
        for btn in self.buttons:
            if btn.click(X,Y):
                return btn.name

        return None

    def get_button(self, name):
        for btn in self.buttons:
            if btn.name == name:
                return btn
        return None

    def update(self):
        """
        update menu and button location
        :return: None
        """
        for btn in self.buttons:
            btn.update()


class VerticalMenu(Menu):
    """
    Vertical Menu for side bar of game
    """
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("comicsans", 20)

    def add_btn(self, img, name, cost):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """
        if name == "BackT" or name == "BackU" or name == "BackG" or name == "BackC":
            btn_x = self.x - 30
            btn_y = self.y + 400
        elif name == "Turn":
            btn_x = self.x - 60
            btn_y = self.y + 350
        elif name == "Menu" or name == "Save":
            btn_x = self.x - 60
            btn_y = self.y + 420
        elif name == "BasicTower" or name == "FireTower" or name == "SlowingTower" or name == "UpgradeTower" or name == "Towers":
            self.items += 1
            btn_x = self.x - 20
            btn_y = self.y - 75 + (self.items-1)*120
        else:
            self.items += 1
            btn_x = self.x - 50
            btn_y = self.y-75 + (self.items-1)*120
        self.buttons.append(VerticalButton(btn_x, btn_y, img, name, cost))

    def clear_btn(self, name):
        if name != "BackT" and name != "BackU" and name != "Turn" and name != "BackG" \
                and name != "Menu" and name != "BackC" and name != "Save":
            self.items -=1
        self.buttons.remove(VerticalMenu.get_button(self,name))

    def get_item_cost(self, name):
        """
        gets cost of item
        :param name: str
        :return: int
        """
        for btn in self.buttons:
            if btn.name == name:
                return btn.cost
        return -1

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """
        win.blit(self.bg, (self.x - self.bg.get_width()/2, self.y-120))

        for item in self.buttons:
            if item.name == "BackU" or item.name == "BackT" or item.name == "BackG" or item.name == "BackC":
                text = "Back"
            elif item.name == "Turn" or item.name == "Menu" or item.name == "Save":
                text = ""
            else:
                text = item.name
                if self.get_item_cost(item.name) > 0:
                    text += f' ({self.get_item_cost(item.name)})'
            item.draw(win)
            text = self.font.render(text, 1, (255,255,255))
            win.blit(text, (item.x + item.width/2 - text.get_width()/2 + 7, item.y + item.height + 5))
