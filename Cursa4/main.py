import random
import pygame
from pygame.locals import*

pygame.init()

clock = pygame.time.Clock()  #задаю частоту кадров
fps = 60

screen_width = 460
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

font = pygame.font.SysFont('Bauhaus 93', 50) #выбираем шрифт из библиотеки

white = (255, 255, 255) #задаю цвет

ground_scroll = 0
scroll_speed = 2
flying = False
game_over = False
pipe_gap = 100
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False


bg = pygame.image.load('E:/Projects/mypj/Новая папка/img/bg.png')
bg = pygame.transform.scale(bg, (460, 420))
ground_img = pygame.image.load('E:/Projects/mypj/Новая папка/img/ground.png')
ground_img = pygame.transform.scale(ground_img, (480, 80))
button_img = pygame.image.load('E:/Projects/mypj/Новая папка/img/restart.png')
