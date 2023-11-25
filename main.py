import os
import random
import string
import time

import pygame as pg

pg.init()

# Init Round
columns = 2 # <---------------- 3 / 4
rows = 2 # <------------------- 3
game = 'trial'
game_title = "Trial-Round"

# Game Constants
screenWidth = 1280
screenHeight = 700
card_size = 110
playing = True
padding = 10
lrMargin = round((screenWidth - ((card_size + padding) * columns)) // 1.5)
tbMargin = round((screenHeight - ((card_size + padding) * rows)) // 5)

# Colors
dark_blue = (34, 62, 99)
white = (255, 255, 255)
black = (0, 0, 0)

# Game Screen
screen = pg.display.set_mode((screenWidth, screenHeight), pg.RESIZABLE)
pg.display.set_caption('Labor UE 2')
font = pg.font.SysFont('Work Sans', 60)

# Background Images
bg_image = pg.image.load('Images/background.jpg')
screen.blit(pg.transform.scale(bg_image, (screenWidth, screenHeight)), (0, 0))
screen.fill(white)
correct_img = pg.image.load('Images/accept.png')
correct_img = pg.transform.scale(correct_img, (card_size-padding, card_size-padding))
false_img = pg.image.load('Images/cancel.png')
false_img = pg.transform.scale(false_img, (card_size-padding, card_size-padding))

# Memory Images
memory_images = []
for item in os.listdir(f'./Images/{game}'):
    icon = pg.image.load(f'./Images/{game}/{item}')
    icon = pg.transform.scale(icon, (card_size-padding, card_size-padding))
    memory_images.append(icon)

# Coordinates
coordinates = []
for i in range(columns):
    for j in range(rows):
        x_coord = i * 200 + lrMargin
        y_coord = j * 130 + tbMargin
        coordinates.append((x_coord, y_coord))

# Hide Button
hide_button = pg.Rect(100, 70, 150, 70)
pg.draw.rect(screen, dark_blue, hide_button)
pg.draw.rect(screen, white, hide_button, 1)
button_title = font.render('HIDE', True, white)
screen.blit(button_title, (125, 88))
hide = False
tile_clicked = False

class Card:
    def __init__(self, image, x, y, cv_letter):
        self.image = image
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, card_size, card_size)
        self.cv_letter = cv_letter
        self.show = True

    def draw(self):
        pg.draw.rect(screen, white, self.rect)
        pg.draw.rect(screen, dark_blue, self.rect, 1)
        screen.blit(self.image, (self.x + 5, self.y + 5))

    def hide(self):
        pg.draw.rect(screen, white, self.rect)
        pg.draw.rect(screen, dark_blue, self.rect, 1)
        cover_letter = font.render(self.cv_letter, True, black)
        screen.blit(cover_letter, (self.x + 35, self.y + 35))

    def compare(self, solution):
        if solution.image == self.image:
            self.image = correct_img
            self.show = False
            if len(targets) > 1:
                del targets[0]
        elif self.image == correct_img:
            self.image = correct_img
            self.show = False
        else:
            screen.blit(false_img, (self.x + 5, self.y + 5))


# Build Deck
playing_cards = []
cover = list(string.ascii_uppercase)
for i in range(len(memory_images)):
    card = Card(memory_images[i], coordinates[i][0], coordinates[i][1], cover[i])
    playing_cards.append(card)

targets = random.sample(range(len(playing_cards)), (columns*rows))


def menubar():
    pg.draw.rect(screen, dark_blue, [0, screenHeight - 80, screenWidth, 80])
    title = font.render(game_title, True, white)
    screen.blit(title, (500, screenHeight-55))


def cards(mode):
    for tile in playing_cards:
        if mode == 'cover' and tile.show:
            tile.hide()
        else:
            tile.draw()


def check(mouse_click):
    for tile in playing_cards:
        if tile.rect.collidepoint(mouse_click):
            tile.compare(playing_cards[targets[0]])


while playing:
    pg.display.update()
    menubar()
    cards('init')
    # Input Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
        if event.type == pg.MOUSEBUTTONDOWN:
            position = pg.mouse.get_pos()
            if hide_button.collidepoint(position):
                hide = True
            else:
                tile_clicked = True
    if hide:
        cards('cover')
        pg.draw.rect(screen, white, [300, 50, card_size, card_size])
        pg.draw.rect(screen, dark_blue, [300, 50, card_size, card_size], 1)
        screen.blit(playing_cards[targets[0]].image, (305, 55))
    if tile_clicked:
        check(position)
    pg.display.update()

pg.quit()
