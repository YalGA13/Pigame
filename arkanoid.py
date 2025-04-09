import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0),  # Красный
          (255, 165, 0),  # Оранжевый
          (255, 255, 0),  # Желтый
          (0, 255, 0),  # Зеленый
          (0, 0, 255)]  # Синий


class Paddle:
    """Класс для платформы игрока"""

    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        """Движение платформы"""
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        """Отрисовка платформы"""
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    """Класс для мяча"""

    def __init__(self):
        self.radius = BALL_RADIUS
        self.reset()

    def reset(self):
        """Сброс мяча в начальное положение"""
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = 5
        self.speed_y = -5
        self.rect = pygame.Rect(self.x - self.radius,
                                self.y - self.radius,
                                self.radius * 2,
                                self.radius * 2)
        self.active = False

    def move(self):
        """Движение мяча"""
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # Столкновение со стенами
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.speed_x *= -1
            if self.rect.top <= 0:
                self.speed_y *= -1

    def draw(self, screen):
        """Отрисовка мяча"""
        pygame.draw.circle(screen, WHITE, self.rect.center, self.radius)


class Brick:
    """Класс для кирпичей"""

    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.active = True

    def draw(self, screen):
        """Отрисовка кирпича"""
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)


class Game:
    """Основной класс игры"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Arkanoid")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        """Инициализация игровых объектов"""
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.create_bricks()

    def create_bricks(self):
        """Создание сетки кирпичей"""
        for row in range(5):
            for col in range(10):
                brick_x = col * (BRICK_WIDTH + 5) + 3
                brick_y = row * (BRICK_HEIGHT + 5) + 50
                color = COLORS[row]
                self.bricks.append(Brick(brick_x, brick_y, color))

    def handle_collisions(self):
        """Обработка столкновений"""
        # Столкновение с платформой
        if self.ball.rect.colliderect(self.paddle.rect) and self.ball.active:
            self.ball.speed_y = -abs(self.ball.speed_y)
            # Изменение направления по X в зависимости от места удара
            hit_pos = (self.ball.rect.centerx - self.paddle.rect.left) / self.paddle.rect.width
            self.ball.speed_x = (hit_pos - 0.5) * 10

        # Столкновение с кирпичами
        for brick in self.bricks:
            if brick.active and self.ball.rect.colliderect(brick.rect):
                brick.active = False
                self.score += 10
                self.ball.speed_y *= -1
                break

        # Проверка на проигрыш
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives > 0:
                self.ball.reset()
            else:
                self.game_over()

    def game_over(self):
        """Завершение игры"""
        text = self.font.render(f"Game Over! Score: {self.score}", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    def check_victory(self):
        """Проверка победы"""
        if all(not brick.active for brick in self.bricks):
            text = self.font.render(f"You Win! Score: {self.score}", True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

    def draw_ui(self):
        """Отрисовка интерфейса"""
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

    def run(self):
        """Основной игровой цикл"""
        while True:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.ball.active:
                        self.ball.active = True

            # Управление
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move("left")
            if keys[pygame.K_RIGHT]:
                self.paddle.move("right")

            # Движение мяча
            self.ball.move()

            # Обработка столкновений
            self.handle_collisions()

            # Отрисовка объектов
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)

            # Отрисовка интерфейса
            self.draw_ui()

            # Проверка победы
            self.check_victory()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()