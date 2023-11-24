import os
import random
import string
import pygame as pg

pg.init()

# Game Constants
screenWidth = 1280
screenHeight = 700
card_size = 110
playing = True
columns, rows, padding = 3, 2, 10
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

# Timers
counter = 5
timer_event = pg.USEREVENT + 1
pg.time.set_timer(timer_event, 1000)

# Background Images
bg_image = pg.image.load('Images/background.jpg')
screen.blit(pg.transform.scale(bg_image, (screenWidth, screenHeight)), (0, 0))
correct_img = pg.image.load('Images/accept.png')
correct_img = pg.transform.scale(correct_img, (card_size-padding, card_size-padding))


# Memory Images
memory_images = []
for item in os.listdir('./Images/cards'):
    icon = pg.image.load(f'./Images/cards/{item}')
    icon = pg.transform.scale(icon, (card_size-padding, card_size-padding))
    memory_images.append(icon)

# Coordinates
coordinates = []
for i in range(columns):
    for j in range(rows):
        x_coord = i * 200 + lrMargin
        y_coord = j * 130 + tbMargin
        coordinates.append((x_coord, y_coord))


class Card:
    def __init__(self, image, x, y, cv_letter):
        self.image = image
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, card_size, card_size)
        self.cv_letter = cv_letter
        self.hidden = True

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
            self.hidden = False
            if len(targets) > 1:
                del targets[0]
            else:
                print("Game Over")
        else:
            self.draw()


# Build Deck
playing_cards = []
cover = list(string.ascii_uppercase)
for i in range(len(memory_images)):
    card = Card(memory_images[i], coordinates[i][0], coordinates[i][1], cover[i])
    playing_cards.append(card)

targets = random.sample(range(len(playing_cards)), (columns*rows))
print(targets)


def menubar():
    pg.draw.rect(screen, dark_blue, [0, screenHeight - 80, screenWidth, 80])
    title = font.render('- Round 1 -', True, white)
    screen.blit(title, (600, screenHeight-55))


def cards(mode):
    for tile in playing_cards:
        if mode == 'init':
            tile.draw()
        if mode == 'cover' and tile.hidden:
            tile.hide()


def check(mouse_click):
    for tile in playing_cards:
        if tile.rect.collidepoint(mouse_click):
            tile.draw()
            tile.compare(playing_cards[targets[0]])


button = pg.Rect(300, 70, 100, 80)
pg.draw.rect(screen, white, button)
button_title = font.render('HIDE', True, dark_blue)
screen.blit(button_title, (310, 80))
hide = False
tile_clicked = False

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
            if button.collidepoint(position):
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
