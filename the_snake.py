from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """это базовый класс, от которого наследуются другие игровые объекты"""

    def __init__(self, body_color=None):
        self.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.body_color = body_color

    def draw(self):
        """заготовку метода для отрисовки объекта"""
        pass


class Snake(GameObject):
    """класс, описывающий змейку"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.positions = [self.position]
        self.next_direction = None

        self.last = None
        self.direction = RIGHT
        self.length = 1

    def get_head_position(self):
        """возвращает позицию головы"""
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку после столкновения с собой"""
        if self.length > 1:
            if self.positions[0] in self.positions[1:]:
                self.direction = RIGHT
                self.last = None
                self.positions = [self.position]
                self.length = 1
                screen.fill(BOARD_BACKGROUND_COLOR)

    def update_direction(self):
        """обновляет направление движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """бновляет позицию змейки"""
        head_x, head_y = self.positions[0]
        direction_x, direction_y = self.direction
        position = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """отрисовывает змейку"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """класс описывающий яблоко"""

    def __init__(self, body_color=APPLE_COLOR, f=[]):
        super().__init__(body_color)
        self.f = f
        self.randomize_position(self.f)

    def randomize_position(self, f):
        """устанавливает случайное положение яблока"""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in f:
                break

    def draw(self, surface):
        """отрисовывает яблоко"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """обрабатывает нажатия клавиш"""
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
    apple = Apple()
    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.get_head_position
        snake.reset()
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        if apple.position in snake.positions:
            apple.randomize_position(snake.positions)
            snake.length += 1


if __name__ == '__main__':
    main()
