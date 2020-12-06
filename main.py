import pygame, sys, engine
from pygame.locals import *
from engine import *

clock = pygame.time.Clock()
pygame.init()

player_anims = {
"idle":7,
"run":8,
}

dir = 1

pygame.display.set_caption("Snow Berry")
win = pygame.display.set_mode((1000, 600), 0, 32)
display = pygame.Surface((500, 300))
platform = pygame.Rect(30, 250, 240, 30)

key_up, key_down, key_left, key_right = False, False, False, False
player = engine.entity(pygame.Rect(50, 20, 8, 16), player_anims, "./Images/Player/", vector(-4, 0), 83, True, 1)

SPEED = 3
JUMP_HEIGHT = 10

coyote_timer = 0

while True:
    # handle input:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                if coyote_timer < 10:
                    coyote_timer = 10
                    player.velocity.y = -JUMP_HEIGHT
            if event.key == K_DOWN:
                key_down = True
            if event.key == K_LEFT:
                dir = -1
                key_left = True
            if event.key == K_RIGHT:
                dir = 1
                key_right = True
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                key_down = False
            if event.key == K_LEFT:
                key_left = False
            if event.key == K_RIGHT:
                key_right = False
    player.velocity.x = 0
    if key_right:
        player.velocity.x = SPEED
    elif key_left:
        player.velocity.x = -SPEED
    collisions = player._update_position([platform])
    if collisions["bottom"]:
        coyote_timer = 0
    else:
        coyote_timer += 0.75

    player.animation = "idle"
    if player.velocity.x != 0:
        player.animation = "run"

    flipped = False
    if dir < 0:
        flipped = True

    player._update_anim(clock.get_time())
    player._render(vector(0, 0), flipped, display)
    pygame.draw.rect(display, (0, 0, 0), platform)

    win.blit(pygame.transform.scale(display, (1000, 600)), (0,0))
    pygame.display.update()
    display.fill((40, 40, 40)) # cls
    clock.tick(60)
