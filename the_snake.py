import random

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_START = 20

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Это базовый класс, от него наследуются другие объекты."""

    def __init__(self, bg_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = bg_color

    def draw(self):
        """Метод определяет, как будет отрисовываться объект."""
        pass

    def draw_object(self, position):
        """Метод определяет, как будет отрисовываться объект."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для яблока"""

    def __init__(self, snake_pos=None, bg_color=APPLE_COLOR):
        super().__init__(bg_color)
        self.randomize_position(snake_pos)

    def randomize_position(self, occupied_cells):
        """Задает случайную координату"""
        while True:
            x_position = random.randrange(SCREEN_START,
                                          SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)
            y_position = random.randrange(SCREEN_START,
                                          SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
            if (x_position, y_position) not in occupied_cells:
                self.position = (x_position, y_position)
                break

    def draw(self):
        """Метод определяет, как будет отрисовываться объект."""
        self.draw_object(self.position)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, bg_color=SNAKE_COLOR):
        super().__init__(bg_color)
        self.positions = None
        self.length = 0
        self.last = None
        self.direction = None
        self.next_direction = None
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        head_new_pos = ((head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
                        (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, head_new_pos)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод определяет, как будет отрисовываться объект."""
        self.draw_object(self.positions[0])
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice((UP, DOWN, LEFT, RIGHT))


def handle_keys(game_object):
    """Обрабатывает события клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл"""
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw()
        snake.draw()

        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
