from random import choice, randint

import pygame

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
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Класс-родитель для элементов игры.

    Атрибуты:
        position (tuple): координаты элемента игры на x и y осях поля
        body_color (tuple): цвет элемента.

    """

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2 - GRID_SIZE // 2,
                         SCREEN_HEIGHT // 2 - GRID_SIZE // 2)
        self.body_color = None

    def draw(self):
        """Пустая функция-шаблон для отрисовки элементов игры."""
        pass


class Apple(GameObject):
    """
    Представляет яблоко в игре.

    Атрибуты:
        Наследует атрибуты от родительского класса.

    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
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
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_rect(self):
        """
        Возвращает прямоугольник, символизирующий яблоко.
        Необходимо для проверки коллизии.
        """
        return pygame.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE)


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
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки"""
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

        # Wrap around the screen edges
        new_head_x, new_head_y = new_head
        new_head_x = new_head_x % SCREEN_WIDTH
        new_head_y = new_head_y % SCREEN_HEIGHT

        new_head = (new_head_x, new_head_y)
        self.last = self.positions[-1] if len(self.positions) > 1 else None
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змею на экране."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # Возвращает позицию головы змейки
    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def get_head_rect(self):
        """Возвращет прямоугольник головы змеи для проверки коллизии."""
        head_x, head_y = self.positions[0]
        return pygame.Rect(head_x, head_y, GRID_SIZE, GRID_SIZE)

    def body_collide(self):
        """Проверяет коллизию головы змеи с телом"""
        head_rect = self.get_head_rect()
        for pos in self.positions[1:]:
            pos_rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            if head_rect.colliderect(pos_rect):
                return True
        return False

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


def main():
    """Запуск игры"""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_rect().colliderect(apple.get_rect()):
            snake.length += 1
            apple.reposition()

        if snake.body_collide():
            snake.reset()

        screen.fill((0, 0, 0))
        apple.draw()
        snake.draw()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
