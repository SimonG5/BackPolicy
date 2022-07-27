import pygame


class Point(pygame.sprite.Sprite):
    def __init__(self, id, checkers, color):
        super().__init__()
        self.id = id
        self.checkers = checkers
        self.color = color
        self.image = pygame.image.load('ui/pointD.png')
        if self.id > 11:
            self.image = pygame.image.load('ui/pointU.png')
        self.rect = self.image.get_rect()
        x, y = 0, 0
        if self.id == 26:
            x, y = 865, 620
            self.image = pygame.image.load('ui/home.png')
        elif self.id == 27:
            x, y = 865, 180
            self.image = pygame.image.load('ui/home.png')
        elif self.id == 24:
            x, y = 450, 250
            self.image = pygame.image.load('ui/home.png')
        elif self.id == 25:
            x, y = 450, 550
            self.image = pygame.image.load('ui/home.png')
        elif self.id > 11:
            x = 114 + 56 * (self.id - 12)
            if self.id > 17:
                x += 56
            y = 175
        else:
            x = 786 - 56 * self.id
            if self.id > 5:
                x -= 56
            y = 600
        self.rect.center = [x, y]
        pass

    def canAddChecker(self, color):
        if self.color != color and self.checkers > 1 or self.color != color and self.id > 23:
            return False
        return True

    def addChecker(self, color):
        if self.color == color or self.color == "NONE":
            self.checkers += 1
            self.color = color
        elif self.checkers <= 1:
            self.removeChecker()
            self.color = color
            self.checkers = 1

    def removeChecker(self):
        self.checkers -= 1
        if self.checkers == 0 and self.id < 24:
            self.color = "NONE"
