import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
BLOCK_SIZE = 20
SPEED = 0


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')


class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # initialize display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        # initialize the game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-2*BLOCK_SIZE, self.head.y)]
        # initialize food
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        if x > self.w - BLOCK_SIZE:
            x = 0
        elif x < 0:
            x = self.w - BLOCK_SIZE
        if y > self.h - BLOCK_SIZE:
           y = 0
        elif y < 0:
            y = self.h - BLOCK_SIZE
        self.head = Point(x, y)

    def play_step(self):
        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        # move
        self._move(self.direction)
        self.snake.insert(0, self.head)
        # check game over
        game_over = False
        if self._is_collision():
            print(self.snake)
            game_over = True
            self.game_over_screen()
            return game_over, self.score
        # place new food or just  move
        if self.head == self.food:
            self._place_food()
            self.score += 1
        else:
            if self.head == self.snake[2]:
                # print('collided')
                self.snake.pop(0)
                # self.head = self.snake[-1]
                if self.direction == Direction.UP:
                    self.direction = Direction.DOWN
                elif self.direction == Direction.DOWN:
                    self.direction = Direction.UP
                elif self.direction == Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif self.direction == Direction.RIGHT:
                    self.direction = Direction.LEFT

            else:
                self.snake = self.snake[:-1]
        # update ui and clock
        self._update_ui()
        # length dependent speed
        SPEED = (len(self.snake) - 3 + 10)
        self.clock.tick(SPEED)
        # return game over and score

        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        # if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
        #     return True
        # self
        if self.head in self.snake[3:]:
            return True
        return False

    def game_over_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            text = font.render('GAME OVER', True, RED)
            text_rect = text.get_rect()
            text_rect.center = (self.h //2, self.w //2)
            self.display.blit(text, text_rect)
            pygame.display.flip()

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, (0, 0))
        # print(self.snake)
        pygame.display.flip()


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()
        if game_over:
            break
        # break if game over
    print('Final Score: ' + str(score))
    pygame.quit()
