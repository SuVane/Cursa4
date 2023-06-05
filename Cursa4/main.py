import random
import sys
import pygame
from pygame.locals import*


if __name__ == "__main__":
    pygame.init()
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Flappy Bird")
    time_clock = pygame.time.Clock()
    ground_y = screen_height * 0.8
    game_images = {}
    is_running = True
    game_images['numbers'] = (
        pygame.image.load('E:/Projects/mypj/images/0.png').convert_alpha(),
        pygame.image.load('E:/Projects/mypj/images/1.png').convert_alpha(),
        pygame.image.load('E:/Projects/mypj/images/2.png').convert_alpha(),
        pygame.image.load('E:/Projects/mypj/images/3.png').convert_alpha(),
        pygame.image.load('E:/Projects/mypj/images/4.png').convert_alpha(),
        pygame.image.load('E:/Projects/mypj/images/5.png').convert_alpha(),
        pygame.image.load('E:/Projects/mypj/images/6.png').convert_alpha(),
        pygame.image.load('E:/Projects/mypj/images/7.png').convert_alpha(),
        pygame.image.load('E:/Projects/mypj/images/8.png').convert_alpha(),
        pygame.image.load('E:/Projects/mypj/images/9.png').convert_alpha()
    )
    player = 'E:/Projects/mypj/images/bird.png'
    background = 'E:/Projects/mypj/images/background.png'
    pipe = 'E:/Projects/mypj/images/pipe.png'
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        pygame.display.flip()
        time_clock.tick(60)
    game_images['start'] = pygame.image.load('E:/Projects/mypj/images/start.jpg').convert_alpha()
    game_images['base'] = pygame.image.load('E:/Projects/mypj/images/base.png').convert_alpha()
    game_images['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
    )
    game_images['background'] = pygame.image.load(background).convert_alpha()
    game_images['player'] = pygame.image.load(player).convert_alpha()


def start_screen():
    player_x = int(screen_width / 8)
    player_y = int((screen_height - game_images['player'].get_height()) / 2)
    message_x = int((screen_width - game_images['message'].get_width()) / 2)
    message_y = int(screen_height * 0.2)
    base_x = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(game_images['background'], (0, 0))
                screen.blit(game_images['message'], (message_x, message_y))
                screen.blit(game_images['player'], (player_x, player_y))
                screen.blit(game_images['base'], (base_x, ground_y))
                pygame.display.update()
                time_clock.tick()


def gameplay():
    score = 0
    player_x = int(screen_width / 8)
    player_y = int(screen_height / 2)
    base_x = 0
    new_pipe1 = get_random_pipe()
    new_pipe2 = get_pandom_pipe()
    upper_pipes = [
        {'x': screen_width + 200, 'y': new_pipe1[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': new_pipe2[0]['y']}
    ]
    lower_pipes = [
        {'x': screen_width + 200, 'y': new_pipe1[1]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': new_pipe2[1]['y']}
    ]
    pipe_ox = -4
    player_oy = -9
    player_max_oy = 10
    player_min_oy = -8
    player_start_oy = 1
    player_flap = -8
    player_flap = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_oy = player_flap
                    player_flap = True
        crash_test = is_smash(player_x, player_y, upper_pipes, lower_pipes)
        if crash_test:
            return
        player_mid = player_x + game_images['player'].get_width() / 2
        for pipe in upper_pipes:
            pipe_mid = pipe['x'] + game_images['pipe'][0].get_width() / 2
            if pipe_mid <= player_mid < pipe_mid + 4:
                score += 1
                print(f"Your Score is {score}")
        if player_oy < player_max_oy and not player_flap:
            player_oy += player_start_oy
        if player_flap:
            player_flap = False
        player_height = game_images['player'].get_height()
        player_y = player_y + min(player_oy, ground_y - player_y - player_height)
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_ox
            lower_pipe['x'] += pipe_ox
        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])
        if upper_pipes[0]['x'] < -game_images['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)
            screen.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            screen.blit(game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        screen.blit(game_images['base'], (base_x, ground_y))
        screen.blit(game_images['player'], (player_x, player_y))
        my_score = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_score:
            width += game_images['numbers'][digit].get_width()
        x_move = (screen_width - width) / 2

        for digit in my_score:
            screen.blit(game_images['numbers'][digit], (x_move, screen_height * 0.12))
            x_move += game_images['numbers'][digit].get_width()
        pygame.display.update()
        time_clock.tick()
