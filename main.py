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

# Background Image
bg_image = pg.image.load('Images/background.jpg')
screen.blit(pg.transform.scale(bg_image, (screenWidth, screenHeight)), (0, 0))


# Memory Images
memory_images = []
for item in os.listdir('./Images/cards'):
    icon = pg.image.load(f'./Images/cards/{item}')
    icon = pg.transform.scale(icon, (card_size-padding, card_size-padding))
    memory_images.append(icon)


class Card:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, card_size, card_size)

    def draw(self):
        pg.draw.rect(screen, white, self.rect)
        pg.draw.rect(screen, dark_blue, self.rect, 1)
        screen.blit(self.image, (self.x + 5, self.y + 5))

    def hide(self):
        pg.draw.rect(screen, white, self.rect)
        pg.draw.rect(screen, dark_blue, self.rect, 1)


coordinates = []
for i in range(columns):
    for j in range(rows):
        x_coord = i * 200 + lrMargin
        y_coord = j * 130 + tbMargin
        coordinates.append((x_coord, y_coord))

playing_cards = []
for i in range(len(memory_images)):
    card = Card(memory_images[i], coordinates[i][0], coordinates[i][1])
    playing_cards.append(card)


def menubar():
    pg.draw.rect(screen, dark_blue, [0, screenHeight - 80, screenWidth, 80])
    title = font.render('- Round 1 -', True, white)
    screen.blit(title, (600, screenHeight-55))


def cards(mode):
    cv_index = 0
    cover = list(string.ascii_uppercase)
    for tile in playing_cards:
        if mode == 'init' or 'reveal':
            tile.draw()
        if mode == 'cover':
            tile.hide()
            cover_letter = font.render(cover[cv_index], True, black)
            screen.blit(cover_letter, (tile.x + 35, tile.y + 35))
        cv_index += 1


def display_timer():
    global counter
    global timer

    pg.draw.rect(screen, white, [50, 50, 100, 80])
    pg.draw.rect(screen, dark_blue, [50, 50, 100, 80], 1)
    timer = font.render(str(counter), True, dark_blue)
    screen.blit(timer, (75, 75))


answer = random.randint(0, len(memory_images) - 1)

while playing:
    pg.display.update()
    menubar()
    display_timer()

    # Input Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
        if event.type == timer_event:
            if counter > 0:
                cards('init')
                pg.draw.rect(screen, white, [50, 50, 100, 80])
                pg.draw.rect(screen, dark_blue, [50, 50, 100, 80], 1)
                timer = font.render(str(counter), True, black)
                counter -= 1
            else:
                cards('cover')
                pg.draw.rect(screen, white, [300, 50, card_size, card_size])
                pg.draw.rect(screen, dark_blue, [300, 50, card_size, card_size], 1)
                screen.blit(memory_images[answer], (305, 55))
        if event.type == pg.MOUSEBUTTONDOWN:
            print(pg.mouse.get_pos())

    pg.display.update()

pg.quit()
