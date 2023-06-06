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

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):  # цикл чтобы птица летала а не была статичной
            img = pygame.image.load(f'E:/Projects/mypj/Новая папка/img/bird{num}.png')
            img = pygame.transform.scale(img, (35, 25))
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]       #центрую изображение
        self.vel = 0  #настройка скорости полёта птицы
        self.clicked = False

    def update(self):

        if flying == True:
            self.vel += 0.2     #полет птицы
            if self.vel > 30:
                self.vel = 0
            if self.rect.bottom < 420:
                self.rect.y += int(self.vel)

        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:    #настройка прыжка
                self.clicked = True
                self.vel = -5
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False