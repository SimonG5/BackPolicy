from xml.dom.minidom import Text
import numpy as np
import pygame
import pygame_widgets
from pygame_widgets.textbox import TextBox
import tensorflow as tf
from backgammon import button
from backgammon.checker import Checker
from backgammon.point import Point

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1150, 800))
screen.fill((164, 116, 73))
pygame.display.set_caption('Backgammon')
model = tf.keras.models.load_model('models/network.model')


def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    # 2D array where each row is a list of words.
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def main():
    run = True
    clock = pygame.time.Clock()

    board = pygame.image.load('ui/board.png')

    outputMapping = {}
    count = 0
    with open("labels/labels.txt") as file:
        for line in file:
            outputMapping[count] = line.strip('\n')
            count += 1

    game = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -
            5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0, 0, 0, 0]

    points = pygame.sprite.Group()
    homes = pygame.sprite.Group()
    checkers = pygame.sprite.Group()
    font = pygame.font.SysFont('Arial', 20)

    bestMoves = "None"

    # load button images
    firstDice = TextBox(screen, 930, 250, 100, 40, fontSize=25,
                        borderColour=(255, 0, 0), textColour=(0, 200, 0),
                        radius=10, borderThickness=5)
    secondDice = TextBox(screen, 930, 300, 100, 40, fontSize=25,
                         borderColour=(255, 0, 0), textColour=(0, 200, 0),
                         radius=10, borderThickness=5)

    btnImage = pygame.image.load('ui/btn.png').convert_alpha()

    # create button instances
    btn = button.Button(912.5, 100, btnImage, 0.8)

    for i in range(0, 24):
        points.add(Point(i, 0, "NONE"))

    points.add(Point(24, 0, "BLACK"))
    points.add(Point(25, 0, "WHITE"))
    points.add(Point(26, 0, "BLACK"))
    points.add(Point(27, 0, "WHITE"))

    for i in range(0, 2):
        checkers.add(Checker(0, i, "WHITE"))
        points.sprites()[0].addChecker("WHITE")
    for i in range(0, 5):
        checkers.add(Checker(5, i, "BLACK"))
        points.sprites()[5].addChecker("BLACK")
    for i in range(0, 3):
        checkers.add(Checker(7, i, "BLACK"))
        points.sprites()[7].addChecker("BLACK")
    for i in range(0, 5):
        checkers.add(Checker(11, i, "WHITE"))
        points.sprites()[11].addChecker("WHITE")
    for i in range(0, 5):
        checkers.add(Checker(12, i, "BLACK"))
        points.sprites()[12].addChecker("BLACK")
    for i in range(0, 3):
        checkers.add(Checker(16, i, "WHITE"))
        points.sprites()[16].addChecker("WHITE")
    for i in range(0, 5):
        checkers.add(Checker(18, i, "WHITE"))
        points.sprites()[18].addChecker("WHITE")
    for i in range(0, 2):
        checkers.add(Checker(23, i, "BLACK"))
        points.sprites()[23].addChecker("BLACK")

    while run:
        if btn.draw(screen):
            input = game[:]
            input.append(int(firstDice.getText()))
            input.append(int(secondDice.getText()))
            input.append(1)
            print(input)
            input = tf.keras.utils.normalize(input)
            predictions = model.predict([input])
            topTenVals = np.sort(predictions[0])[-10:]
            topTen = np.argsort(predictions[0])[-10:]
            print("------------------------")
            screen.fill((164, 116, 73))
            bestMoves = ""
            for i in range(9, -1, -1):
                bestMoves += str(abs(i-10)) + ": " + str(outputMapping[topTen[i]]) + \
                    " : " + str(topTenVals[i]) + "\n"
            blit_text(screen, bestMoves, (920, 380), font)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for checker in checkers:
                        if checker.rect.collidepoint(pos):
                            checker.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for checker in checkers:
                    if checker.dragging:
                        collidingWithPoint = False
                        for i, point in enumerate(points):
                            if point.rect.collidepoint(pos) and point.canAddChecker(checker.color):
                                points.sprites()[checker.point].removeChecker()
                                checker.point = i
                                collidingWithPoint = True
                                if point.id < 11:
                                    checker.image = pygame.image.load(
                                        'ui/white_checker.png')
                                    if checker.color == "BLACK":
                                        checker.image = pygame.image.load(
                                            'ui/black_checker.png')
                                    checker.rect = checker.image.get_rect()
                                    checker.snapY = 740 - 56 * point.checkers
                                    checker.snapX = point.rect.centerx
                                elif point.id > 11 and point.id < 24:
                                    checker.image = pygame.image.load(
                                        'ui/white_checker.png')
                                    if checker.color == "BLACK":
                                        checker.image = pygame.image.load(
                                            'ui/black_checker.png')
                                    checker.rect = checker.image.get_rect()
                                    checker.snapY = 70 + 56 * point.checkers
                                    checker.snapX = point.rect.centerx
                                elif point.id == 25:
                                    checker.image = pygame.image.load(
                                        'ui/white_checker.png')
                                    checker.rect = checker.image.get_rect()
                                    checker.snapY = 450 + 56 * point.checkers
                                    checker.snapX = point.rect.centerx
                                elif point.id == 24:
                                    checker.image = pygame.image.load(
                                        'ui/black_checker.png')
                                    checker.rect = checker.image.get_rect()
                                    checker.snapY = 365 - 56 * point.checkers
                                    checker.snapX = point.rect.centerx
                                elif point.id == 27:
                                    checker.image = pygame.image.load(
                                        'ui/white_out.png')
                                    checker.rect = checker.image.get_rect()
                                    checker.snapX = point.rect.centerx
                                    checker.snapY = 60 + 18 * point.checkers
                                elif point.id == 26:
                                    checker.image = pygame.image.load(
                                        'ui/black_out.png')
                                    checker.rect = checker.image.get_rect()
                                    checker.snapX = point.rect.centerx
                                    checker.snapY = 755 - 18 * point.checkers
                                checker.rect.center = [
                                    checker.snapX, checker.snapY]
                                point.addChecker(checker.color)
                                break
                        if not collidingWithPoint:
                            checker.returnToPoint()
                    checker.dragging = False

                for i, point in enumerate(points):
                    game[i] = point.checkers
                    if point.color == "BLACK" and point.id < 24:
                        game[i] = -game[i]

                print(game)

        for checker in checkers:
            if checker.dragging:
                pos = pygame.mouse.get_pos()
                checker.rect.center = [pos[0], pos[1]]

        pygame_widgets.update(events)
        pygame.display.flip()
        screen.blit(board, (0, 0))
        points.draw(screen)
        homes.draw(screen)
        checkers.draw(screen)
        clock.tick(60)

    pygame.quit()


main()
