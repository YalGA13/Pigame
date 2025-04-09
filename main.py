import pygame
import random
import sys
import math

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 40
ENEMY_SIZE = 30
PLAYER_SPEED = 5
ENEMY_SPEED = 2
SPAWN_RATE = 25
MAX_ENEMIES = 15

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
        self.y = SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE)

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        self.x = max(0, min(SCREEN_WIDTH - PLAYER_SIZE, new_x))
        self.y = max(0, min(SCREEN_HEIGHT - PLAYER_SIZE, new_y))
        self.rect.update(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE)

    def draw(self, screen):
        points = []
        radius = PLAYER_SIZE // 2
        center_x = self.x + radius
        center_y = self.y + radius
        for i in range(5):
            angle = math.radians(18 + i * 72)
            outer_x = center_x + radius * math.cos(angle)
            outer_y = center_y + radius * math.sin(angle)
            inner_x = center_x + radius / 2 * math.cos(angle + math.radians(36))
            inner_y = center_y + radius / 2 * math.sin(angle + math.radians(36))
            points.extend([(outer_x, outer_y), (inner_x, inner_y)])
        pygame.draw.polygon(screen, YELLOW, points)


class Enemy:
    def __init__(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            self.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
            self.y = -ENEMY_SIZE
        elif side == 'bottom':
            self.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
            self.y = SCREEN_HEIGHT
        elif side == 'left':
            self.x = -ENEMY_SIZE
            self.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        else:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)

        self.speed = ENEMY_SPEED + random.random() * 1.0
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        angle = math.atan2(center_y - self.y, center_x - self.x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.rect = pygame.Rect(self.x, self.y, ENEMY_SIZE, ENEMY_SIZE)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.update(self.x, self.y, ENEMY_SIZE, ENEMY_SIZE)

    def draw(self, screen):
        pygame.draw.line(screen, RED,
                         (self.x + 5, self.y + 5),
                         (self.x + ENEMY_SIZE - 5, self.y + ENEMY_SIZE - 5), 3)
        pygame.draw.line(screen, RED,
                         (self.x + ENEMY_SIZE - 5, self.y + 5),
                         (self.x + 5, self.y + ENEMY_SIZE - 5), 3)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Survival Flight")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.player = Player()
        self.enemies = []
        self.score = 0
        self.high_score = 0
        self.running = True
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def spawn_enemy(self):
        if len(self.enemies) < MAX_ENEMIES:
            self.enemies.append(Enemy())

    def handle_collisions(self):
        for enemy in self.enemies[:]:
            if self.player.rect.colliderect(enemy.rect):
                self.running = False
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                return

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        high_text = self.font.render(f"High: {self.high_score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_text, (10, 50))

    def game_over_screen(self):
        self.screen.fill(BLACK)
        text = self.font.render("Game Over! Press R to restart", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        self.draw_hud()
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def run(self):
        while True:
            self.reset_game()
            while self.running:
                self.screen.fill(BLACK)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                keys = pygame.key.get_pressed()
                dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
                dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
                self.player.move(dx, dy)

                if random.randint(1, SPAWN_RATE) == 1:
                    self.spawn_enemy()

                for enemy in self.enemies[:]:
                    enemy.update()
                    if (enemy.x < -ENEMY_SIZE * 2 or
                            enemy.x > SCREEN_WIDTH + ENEMY_SIZE * 2 or
                            enemy.y < -ENEMY_SIZE * 2 or
                            enemy.y > SCREEN_HEIGHT + ENEMY_SIZE * 2):
                        self.enemies.remove(enemy)

                self.handle_collisions()
                self.score += 1

                self.player.draw(self.screen)
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                self.draw_hud()

                pygame.display.flip()
                self.clock.tick(60)

            self.game_over_screen()


if __name__ == "__main__":
    game = Game()
    game.run()