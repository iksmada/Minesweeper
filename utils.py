import pygame

from constants import *

def get_recommended_font_size(screen_object,screen_percentage,text):
    width = int(screen_object.get_width()*screen_percentage/100)
    font = pygame.font.Font('fonts/UbuntuMono.ttf', HUGE_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return HUGE_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', EXTRA_LARGE_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return EXTRA_LARGE_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', LARGE_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return LARGE_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', NORMAL_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return NORMAL_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', SMALL_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return SMALL_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', EXTRA_SMALL_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return EXTRA_SMALL_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', TINY_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return TINY_FONT_SIZE

    return TINY_FONT_SIZE