from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

SCREEN_CENTER = (
    (SCREEN_WIDTH // 2 // GRID_SIZE) * GRID_SIZE,
    (SCREEN_HEIGHT // 2 // GRID_SIZE) * GRID_SIZE
)

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
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Класс-родитель для элементов игры.

    Атрибуты:
        position (tuple): координаты элемента игры на x и y осях поля
        body_color (tuple): цвет элемента.

    """

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Пустая функция-шаблон для отрисовки элементов игры."""
        pass

    def draw_cell(self, position, clear=False):
        """Отрисовывет клетку"""
        x, y = position
        rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        if clear:
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        else:
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        return rect


class Apple(GameObject):
    """
    Представляет яблоко в игре.

    Атрибуты:
        Наследует атрибуты от родительского класса.

    """

    def __init__(self):
        super().__init__(position=SCREEN_CENTER, body_color=APPLE_COLOR)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Создание рандомных координат для яблока."""
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return (x, y)

    def reposition(self):
        """Создание новых координат для смены положения яблока."""
        self.position = self.randomize_position()

    def draw(self):
        """Отрисовка яблока."""
        return self.draw_cell(self.position)


class Snake(GameObject):
    """
    Представляет змею в игре.

    Атрибуты:
        Наследует атрибуты родительского класса.
        length (int): длина "тела" змеи
        positions (list): список координат для всех составляющих змеи
        direction (tuple): текущее направление движения змеи
        next_direction (tuple): следующее направление движения змеи
        last (tuple): координаты последнего элемента тела змеи
    """

    def __init__(self):
        super().__init__(position=SCREEN_CENTER, body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, перемещая её в новое положение."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = (
            head_x + direction_x * GRID_SIZE,
            head_y + direction_y * GRID_SIZE
        )

        new_head_x, new_head_y = new_head
        new_head_x = new_head_x % SCREEN_WIDTH
        new_head_y = new_head_y % SCREEN_HEIGHT

        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змею на экране."""

        for position in self.positions:
            self.draw_cell(position)

        # Отрисовка головы змейки
        # self.draw_cell(self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, clear=True)

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def body_collide(self, item):
        """Проверяет коллизию переданного в параметр предмета с телом змеи"""
        return item in self.positions[1:]

    def reset(self):
        """Возвращает змею в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для управления змеей.

    Аргументы:
        game_object: объект, для которого обрабатываются нажатия клавиш
    """
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


def needed_reposition(snake, apple):
    """Меняет положение яблока, если яблоко оказывается на теле змеи."""
    while snake.body_collide(apple.position):
        apple.reposition()


def main():
    """Запуск игры"""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        needed_reposition(snake, apple)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.reposition()
            needed_reposition(snake, apple)

        if snake.body_collide(snake.get_head_position()):
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
