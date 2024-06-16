
import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60

SCORE = 0
SCORE_INCREMENT = 10

SLIDER_VEL = 7
SLIDER_LENGTH = 90
SLIDER_WIDTH = 5

BLOCK_WIDTH = 50
BLOCK_HEIGHT = 65

BALL_X_VEL = 5
BALL_Y_VEL = 5
BALL_WIDTH = 10
BALL_HEIGHT = 10


BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background.png')), (WIDTH, HEIGHT))

SLIDER_IMAGE = pygame.image.load(os.path.join('Assets', 'slider.png'))
SLIDER = pygame.transform.rotate(pygame.transform.scale(SLIDER_IMAGE, (SLIDER_WIDTH, SLIDER_LENGTH)), 90)


BLOCK_IMAGE = pygame.image.load(os.path.join('Assets', 'block.png'))
BLOCK = pygame.transform.rotate(pygame.transform.scale(BLOCK_IMAGE, (BLOCK_WIDTH, BLOCK_HEIGHT)), 90)

BALL_IMAGE = pygame.image.load(os.path.join('Assets', 'ball.png'))
BALL = pygame.transform.rotate(pygame.transform.scale(BALL_IMAGE, (BALL_WIDTH, BALL_HEIGHT)), 90)


font = pygame.font.Font('freesansbold.ttf', 64)
text_welcome = font.render('Press Space Bar to Begin', True, WHITE, BLACK)
text_welcome_rect = text_welcome.get_rect()
text_welcome_rect.center = (WIDTH // 2, HEIGHT // 2)

text_game_over = font.render('Game Over', True, WHITE, BLACK)
text_game_over_rect = text_game_over.get_rect()
text_game_over_rect.center = (WIDTH // 2, HEIGHT // 2)

text_winner = font.render('You Win!', True, WHITE, BLACK)
text_winner_rect = text_winner.get_rect()
text_winner_rect.center = (WIDTH // 2, HEIGHT // 2)

font_score = pygame.font.Font('freesansbold.ttf', 15)
text_score = font_score.render(f'Score: {SCORE}', True, WHITE, BLACK)
text_score_rect = text_score.get_rect()
text_score_rect.center = (WIDTH - 45, 20)




class block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.isDestroyed = False
        self.hitbox = (self.x, self.y, BLOCK_HEIGHT, BLOCK_WIDTH)
        self.blocks = []


    def draw(self, WINDOW):
        if not self.isDestroyed: #only print when object has not been hit
            WINDOW.blit(BLOCK, (self.x, self.y))
            pygame.draw.rect(WINDOW, (255, 0, 0), self.hitbox, 2)

    def append(self, elem):
        self.blocks.append(elem)


    def create(self):
        y = self.y
        for i in range(3):
            x = self.x
            for j in range(7):
                self.blocks.append(block(x, y))
                x = x + BLOCK_WIDTH + BLOCK_HEIGHT
            y = y + BLOCK_WIDTH + BLOCK_HEIGHT

    
    def update(self, ball): #Working vertically
         if ball.y < self.y + BLOCK_HEIGHT and ball.y > self.y:
            if ball.x > self.x and ball.x < self.x + BLOCK_WIDTH:
                 self.isDestroyed = True
                 ball.y_vel *= -1



class slider:
    def __init__(self):
        self.x = (WIDTH // 2) - SLIDER_LENGTH // 2
        self.y = 480
        self.vel = SLIDER_VEL
        self.length = SLIDER_LENGTH
        self.width = SLIDER_WIDTH
        self.left_side = self.x - (self.length // 2)
        self.right_side = self.x + self.length // 2
        self.top_side = self.y + self.width
        self.bottom_side = self.y - self.width
        self.hitbox = (self.x, self.y, SLIDER_LENGTH, SLIDER_WIDTH)
        self.waiting = True

    def draw(self, WINDOW):
        WINDOW.blit(SLIDER, (self.x, self.y))
        pygame.draw.rect(WINDOW, (255, 0, 0), self.hitbox, 2)

    def move(self, keys_pressed):
        if self.waiting == False:
            if keys_pressed[pygame.K_LEFT] and self.x - self.vel > 0: # Moves Left
                self.x -= self.vel
            if keys_pressed[pygame.K_RIGHT] and self.x + SLIDER_LENGTH + self.vel < WIDTH: # Moves Right
                self.x += self.vel

        self.hitbox = (self.x, self.y, SLIDER_LENGTH, SLIDER_WIDTH)

    def get_left(self):
        return self.x - (self.length // 2) + 40 
    
    def get_right(self):
        return self.x + (self.length // 2) + 40

        


class ball:
    def __init__(self):
        self.x = WIDTH // 2 - 5 # - 5 only for appearance
        self.y = 475
        self.width = BALL_WIDTH
        self.height = BALL_HEIGHT
        self.x_vel = BALL_X_VEL
        self.y_vel = BALL_Y_VEL
        self.outOfBounds = False
        self.waiting = True
        self.top = self.y
        self.bottom = self.top + BALL_HEIGHT
        self.left = self.x
        self.right = self.x + BALL_WIDTH
        self.hitbox = (self.x, self.y, BALL_HEIGHT, BALL_WIDTH)
        self.lost = False

    def draw(self, WINDOW):
        WINDOW.blit(BALL, (self.x, self.y))
        pygame.draw.rect(WINDOW, (255, 0, 0), self.hitbox, 2)
            

    def move(self):
        if not self.waiting:

            self.x = self.x - self.x_vel
            self.y = self.y - self.y_vel

            if self.x + self.x_vel + self.width < 0 or self.x + self.x_vel + self.width > WIDTH: # Ball bounces off both left and right sides of screen
                self.x_vel *= -1
                if self.x + self.width + self.x_vel > WIDTH: # Move away from wall to avoid being stuck
                    self.x -= 10
                if self.x + self.width + self.x_vel < 0:
                    self.x += 10
                
            if self.y + self.y_vel < 0: # Ball bounces off top of screen
                self.y_vel *= -1
                self.y += 10

            if self.y + self.y_vel > HEIGHT: 
                self.lost = True


            self.hitbox = (self.x, self.y, BALL_HEIGHT, BALL_WIDTH)



    def stopWaiting(self, keys_pressed):
        if keys_pressed[pygame.K_SPACE]:
            self.waiting = False


def ball_bounced(ball, slider):
    if ball.y == slider.top_side:
        if ball.x > slider.get_left() and ball.x < slider.get_right():
            ball.y_vel *= -1

  

def draw_window(player, ball_oop, blocks, welcome_message, winner_message):
    WINDOW.blit(BACKGROUND, (0, 0))

    player.draw(WINDOW)
    ball_oop.draw(WINDOW)

    for i in blocks.blocks:
        i.draw(WINDOW)


    if welcome_message == True:
        WINDOW.blit(text_welcome, text_welcome_rect)

    if ball_oop.lost == True:
        WINDOW.blit(text_game_over, text_game_over_rect)

    if winner_message == True:
        WINDOW.blit(text_winner, text_winner_rect)

    text_score = font_score.render(f'Score: {SCORE}', True, WHITE, BLACK) # Updates values
    WINDOW.blit(text_score, text_score_rect)

    pygame.display.update()


 

def main():
    player = slider()
    ball_oop = ball()
    blocks = block(70, 20)
    blocks.create()

    clock = pygame.time.Clock()
    run = True
    welcome_message = True
    winner_message = False

    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed() 
        if keys_pressed[pygame.K_SPACE]:
            ball_oop.waiting = False
            player.waiting = False
            welcome_message = False

        ball_oop.move()
        player.move(keys_pressed)
        ball_bounced(ball_oop, player)
        draw_window(player, ball_oop, blocks, welcome_message, winner_message)
        
        for i in blocks.blocks:
            i.update(ball_oop)
            if i.isDestroyed == True:
                global SCORE
                blocks.blocks.remove(i)
                SCORE += SCORE_INCREMENT
                if len(blocks.blocks) == 0:
                    winner_message = True

        

if __name__ == "__main__":
    main()
