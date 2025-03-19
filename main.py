import sys
import pygame
import random
from random import choice

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

paddle_sound = pygame.mixer.Sound('paddle hit.mp3')
glass_sound = pygame.mixer.Sound('Glass Smash.mp3')
air_horn_sound = pygame.mixer.Sound('air-horn.mp3')

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0:
        glass_sound.play()
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        glass_sound.play()
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) or ball.colliderect(opponent):
        paddle_sound.play()
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_reset():
    global ball_speed_x, ball_speed_y, score_time
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width // 2, screen_height // 2)

    if current_time - score_time < 700:
        number_three = game_font.render('3', True, light_grey)
        screen.blit(number_three, (screen_width // 2 - 10, screen_height // 2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render('2', True, light_grey)
        screen.blit(number_two, (screen_width // 2 - 10, screen_height // 2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render('1', True, light_grey)
        screen.blit(number_one, (screen_width // 2 - 10, screen_height // 2 + 20))
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0,0
    else:
        air_horn_sound.play()
        ball_speed_y = 7 * choice((1, -1))
        ball_speed_x = 7 * choice((1, -1))
        score_time = None

screen_width = 1280
screen_height = 960
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7
player_score = 0
opponent_score = 0
game_font = pygame.font.Font('freesansbold.ttf', 48)
paddle_length = 140
score_time = 1

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pythong')

ball = pygame.Rect(screen_width // 2 - 15, screen_height // 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height // 2 - 70, 15, paddle_length)
opponent = pygame.Rect(10, screen_height // 2 - 70, 15, paddle_length)

bg_colour = pygame.Color('grey12')
light_grey = (200, 200, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponent_animation()

    screen.fill(bg_colour)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width // 2, 0), (screen_width // 2, screen_height))

    if score_time:
        ball_reset()

    player_text = game_font.render(f'{player_score}', False, light_grey)
    opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (600, 470))
    screen.blit(player_text, (660, 470))

    pygame.display.flip()
    clock.tick(60)