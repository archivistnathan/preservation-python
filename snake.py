import pygame


class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    STILL = (0, 0)


class Snake:
    BLOCK = 40
    SPEED = 4  # The lower the slower (1 is slowest, 10 is fastest)

    def __init__(self, x0, y0, color_snake=(0, 0, 0), size=BLOCK):
        self.length = 1
        self.head = [x0, y0]
        self.direction = Direction.STILL
        self.positions = []
        self.color_snake = color_snake
        self.size = size

    @property
    def score(self):
        return max(0, self.length - 1)

    def draw(self, dis):
        for x in self.positions:
            pygame.draw.rect(dis, self.color_snake, [x[0], x[1], self.size, self.size])

    def show_score(self, dis, font, prefix="", color=(255, 255, 102)):
        """Display the current score on the screen."""
        value = font.render(prefix + str(self.score), True, color)
        dis.blit(value, [0, 0])

    def update(self):
        self.positions.append(self.head.copy())
        if len(self.positions) > self.length:
            del self.positions[0]

    def handle(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            return Direction.LEFT
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            return Direction.RIGHT
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            return Direction.UP
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            return Direction.DOWN
        return Direction.STILL

    def out_of_bounds(self, dis_width, dis_height):
        return (
            self.head[0] >= dis_width
            or self.head[0] < 0
            or self.head[1] >= dis_height
            or self.head[1] < 0
        )

    def self_collision(self):
        """
        Check if the snake has collided with itself.
        Returns True if a collision is detected, otherwise False.
        """
        for pos in self.positions[:-1]:
            if pos == self.head:
                return True
        return False

    def grow(self):
        self.length += 1

    def shrink(self):
        """
        Halve the snake's length, ensuring it doesn't go below 1.
        Returns True if the snake's length is now 1 or less, indicating game over.
        """
        self.length = max(1, self.length // 2)
        # Reduce the positions list to match the new length
        self.positions = self.positions[-self.length:]
        return self.length <= 1

    def move(self, direction):
        self.direction = direction
        x_change, y_change = Snake.delta(direction)
        self.head[0] += x_change
        self.head[1] += y_change

    def collide(self, x, y):
        return self.head[0] == x and self.head[1] == y

    @staticmethod
    def delta(direction):
        if direction == Direction.UP:
            return [0, -Snake.BLOCK]
        elif direction == Direction.DOWN:
            return [0, Snake.BLOCK]
        elif direction == Direction.LEFT:
            return [-Snake.BLOCK, 0]
        elif direction == Direction.RIGHT:
            return [Snake.BLOCK, 0]
        return [0, 0]
