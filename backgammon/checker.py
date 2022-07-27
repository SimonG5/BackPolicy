import pygame


class Checker(pygame.sprite.Sprite):
    def __init__(self, point, pointPos, color):
        super().__init__()
        self.color = color
        if self.color == "WHITE":
            self.image = pygame.image.load('ui/white_checker.png')
        else:
            self.image = pygame.image.load('ui/black_checker.png')
        self.rect = self.image.get_rect()
        self.point = point
        self.pointPos = pointPos
        self.dragging = False
        x, y = 0, 0
        if self.point > 11:
            x = 115 + (self.point - 12) * 56
            if self.point > 17:
                x += 56
            y = 70 + self.pointPos * 56
        else:
            x = 785 - self.point * 56
            if self.point > 5:
                x -= 56
            y = 740 - self.pointPos * 56
        self.rect.center = [x, y]
        self.snapX = x
        self.snapY = y

    def returnToPoint(self):
        self.rect.center = [self.snapX, self.snapY]
