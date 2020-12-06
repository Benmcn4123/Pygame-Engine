import json
import pygame

tiles = None

class vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def _move_rect(rect, velocity, colliders):
    collisions = {"right":False, "left":False, "top":False, "bottom":False}

    # update x position
    rect.move_ip(velocity.x, 0)
    for collision in colliders:
        if rect.colliderect(collision):
            if velocity.x > 0:
                rect.right = collision.left
                collisions["right"] = True
            else:
                rect.left = collision.right
                collisions["left"] = True

    # update y position
    rect.move_ip(0, velocity.y)
    for collision in colliders:
        if rect.colliderect(collision):
            if velocity.y < 0:
                rect.top = collision.bottom
                collisions["top"] = True
            else:
                rect.bottom = collision.top
                collisions["bottom"] = True

    return collisions # return a list of all collisions with other tiles

class entity:
    def __init__(self, rect, animations, animation_directory, img_offset, framerate, use_physics, gravity):
        self.rect = rect
        self.animation_directory = animation_directory
        self.frame = 0
        anims = {}
        for anim_name in list(animations.keys()):
            sub_anims = []
            for i in range(0, animations[anim_name]):
                sub_anims.append(pygame.image.load(str(self.animation_directory) + str(anim_name) + str(i+1) + ".png"))
            anims[anim_name] = sub_anims
        self.animations = anims
        self.animation = list(self.animations.keys())[0]
        self.image = self.animations[self.animation][self.frame]
        self.img_offset = img_offset
        self.framerate = framerate
        self.anim_time = 0
        self.use_physics = use_physics
        self.velocity = vector(0, 0)
        self.gravity = gravity

    def _update_anim(self, delta_time):
        self.anim_time += delta_time
        if self.anim_time >= self.framerate:
            self.anim_time = 0
            self.frame += 1
            if self.frame >= len(self.animations[self.animation]):
                self.frame = 0
            self.image = self.animations[self.animation][self.frame]


    def _update_position(self, tiles):
        if self.use_physics:
            self.velocity.y += self.gravity
            collisions = _move_rect(self.rect, self.velocity, tiles)
            if collisions["bottom"] or collisions["top"]:
                self.velocity.y = 0
            return collisions

        _move_rect(self.rect, self.velocity, tiles)

    def _render(self, cam_pos, flipped, display):
        rect = pygame.Rect(self.rect.x - cam_pos.x, self.rect.y - cam_pos.y, self.rect.width, self.rect.height)
        offset_rect = (rect.x + self.img_offset.x, rect.y + self.img_offset.y, rect.width, rect.height)
        if flipped:
            display.blit(pygame.transform.flip(self.image, True, False), offset_rect)
            return
        display.blit(self.image, offset_rect)

def _load_tilemap(file_path):
    with open(file_path) as file:
        chunks = json.load(file)
        return chunks

def _visible_chunks(all_chunks, tile_width, cam):
    for chunk in all_chunks:
        pass
