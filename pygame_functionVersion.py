import pygame
from random import randint

# follow along: https://www.youtube.com/watch?v=AY9MnQ4x3zk

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = test_font.render(f'score:{current_time}', False, 'Black')
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)


def collisions(player, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player.colliderect(obstacle_rect): return False
    return True


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walks): player_index = 0
        player_surf = player_walks[int(player_index)]

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
# test_surface = pygame.Surface((100,200))
# test_surface.fill('Red')
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()

# score_surf = test_font.render('My game', False, 'Black')
# score_rect = score_surf.get_rect(center=(400, 50))

# obstacle
snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_index = 0
snail_surf = snail_frames[snail_index]

fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_index = 0
fly_surf = fly_frames[fly_index]

obstacle_rect_list = []

player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_walks = [player_walk1, player_walk2]
player_index = 0
player_surf = player_walks[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2.0)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('PixelRunner', False, 'Teal')
game_name_rect = game_name.get_rect(midtop=(400, 50))

#obstacle timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)
fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

            if event.type == snail_timer:
                if snail_index == 1: snail_index = 0
                else: snail_index = 1
                snail_surf = snail_frames[snail_index]
            if event.type == fly_timer:
                if fly_index == 1: fly_index = 0
                else: fly_index = 1
                fly_surf = fly_frames[fly_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()


    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, 'Pink', score_rect)
        # pygame.draw.rect(screen, 'Pink', score_rect, 10)
        # pygame.draw.aaline(screen, 'Gold', (0,0), pygame.mouse.get_pos(), 10)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collisions(player_rect, obstacle_rect_list)
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        if score == 0:
            score_message = test_font.render('Press SPACE to start.', False, 'Red')
            score_message_rect = score_message.get_rect(midbottom=(400, 340))
        else:
            score_message = test_font.render(f'Your score:{score}', False, 'Red')
            score_message_rect = score_message.get_rect(midbottom=(400, 340))
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
