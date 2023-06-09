import pygame
import random

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


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


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

                self.counter += 1   #анимация
                flap_cooldown = 5

                if self.counter > flap_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0

                self.image = self.images[self.index]

                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
            else:
                self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('E:/Projects/mypj/Новая папка/img/pipe.png')
        self.image = pygame.transform.scale(self.image, (35, 250))
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)

button = Button(screen_width // 2 - 50, screen_height // 2 - 50, button_img)

run = True
while run:

    clock.tick(fps)

    screen.blit(bg, (0, 0))

    pipe_group.draw(screen)

    screen.blit(ground_img, (ground_scroll, 420))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.left < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    bird_group.draw(screen)
    bird_group.update()

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom >= 420:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-50, 50)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        pipe_group.update()

        ground_scroll -= scroll_speed + .3
        if abs(ground_scroll) > 20:
            ground_scroll = 0

    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()
