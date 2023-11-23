import os
import random
import string

import numpy
import pygame as pg

pg.init()

# Game Constants
screenWidth = 1280
screenHeight = 700
card_size = 110
playing = True
columns, rows, padding = 3, 4, 10
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
counter = 30
timer_event = pg.USEREVENT + 1
pg.time.set_timer(timer_event, 1000)

# Background Image
bg_image = pg.image.load('Images/background.jpg')
screen.blit(pg.transform.scale(bg_image, (screenWidth, screenHeight)), (0, 0))


# Memory Images
memoryImages = []
for item in os.listdir('./Images/cards'):
    icon = pg.image.load(f'./Images/cards/{item}')
    icon = pg.transform.scale(icon, (card_size-padding, card_size-padding))
    memoryImages.append(icon)
    memoryImages.append(icon)
    random.shuffle(memoryImages)


def menubar():
    pg.draw.rect(screen, dark_blue, [0, screenHeight - 80, screenWidth, 80])
    title = font.render('- Round 1 -', True, white)
    screen.blit(title, (600, screenHeight-55))


def init_cards():
    cv_index = 0
    for i in range(columns):
        for j in range(rows):
            x = i * 200 + lrMargin
            y = j * 130 + tbMargin
            pg.draw.rect(screen, white, [x, y, card_size, card_size])
            pg.draw.rect(screen, dark_blue, [x, y, card_size, card_size], 1)
            screen.blit(memoryImages[cv_index], (x+5, y+5))
            cv_index += 1


def cover_cards():
    cover = list(string.ascii_uppercase)
    cv_index = 0
    for i in range(columns):
        for j in range(rows):
            x = i * 200 + lrMargin
            y = j * 130 + tbMargin
            pg.draw.rect(screen, white, [x, y, card_size, card_size])
            pg.draw.rect(screen, dark_blue, [x, y, card_size, card_size], 1)
            cover_letter = font.render(cover[cv_index], True, black)
            screen.blit(cover_letter, (x + 38, y + 35))
            cv_index += 1


def display_timer():
    global counter
    global timer

    pg.draw.rect(screen, white, [50, 50, 100, 80])
    pg.draw.rect(screen, dark_blue, [50, 50, 100, 80], 1)
    timer = font.render(str(counter), True, dark_blue)
    screen.blit(timer, (75, 75))


while playing:
    pg.display.update()
    menubar()
    display_timer()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
        elif event.type == timer_event:
            if counter != 0:
                init_cards()
                counter -= 1
                pg.draw.rect(screen, white, [50, 50, 100, 80])
                pg.draw.rect(screen, dark_blue, [50, 50, 100, 80], 1)
                timer = font.render(str(counter), True, black)
            else:
                cover_cards()

    pg.display.update()

pg.quit()
