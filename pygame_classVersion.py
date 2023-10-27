import pygame
from random import randint, choice

# follow along: https://www.youtube.com/watch?v=AY9MnQ4x3zk

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.player_walks = [player_walk1, player_walk2]
        self.player_index = 0
        self.image = self.player_walks[player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walks): self.player_index = 0
            self.image = self.player_walks[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            self.y_pos = 210
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            self.y_pos = 300
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(bottomright=(randint(900, 1100), self.y_pos))

    def animation_state(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x < -100:
            self.kill()

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = test_font.render(f'score:{current_time}', False, 'Black')
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collisions(player, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True

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

bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(-1)

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

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()



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
                obstacle_group.add(obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                # if randint(0, 2):
                #     obstacle_group.add(obstacle('fly'))
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                # else:
                #     obstacle_group.add(obstacle('snail'))
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

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

        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300: player_rect.bottom = 300
        # screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()


        # collision
        game_active = collision_sprite()
        # game_active = collisions(player_rect, obstacle_rect_list)
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
