import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
red_background = (255, 0, 0)
white_background = (255, 255, 255)

# Define screen dimensions
dis_width = 1200
dis_height = 800

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Preservation Python, Adapted from Snake Game by Edureka')

clock = pygame.time.Clock()

snake_block = 40
snake_speed = 10

font_style = pygame.font.SysFont("arial", 25)
score_font = pygame.font.SysFont("timesnewroman", 20)

# Load and scale the images for the food items
def load_and_scale_image(image_name):
    img = pygame.image.load(f'images/{image_name}')
    img = pygame.transform.scale(img, (snake_block, snake_block))
    return img

# Initial set of images for food that increases the score
food_increase_images_1 = [
    load_and_scale_image('accessrights.png'),
    load_and_scale_image('checksum.png'),
    load_and_scale_image('context.png'),
    load_and_scale_image('dataobject.png'),
    load_and_scale_image('metadata.png')
]

# New set of images after score reaches 25
food_increase_images_2 = [
    load_and_scale_image('backup.png'),
    load_and_scale_image('emulation.png'),
    load_and_scale_image('migration.png'),
    load_and_scale_image('refresh.png'),
    load_and_scale_image('techwatch.png')
]

# Images for food that decreases the score
food_decrease_images = [
    load_and_scale_image('brokenhardware.png'),
    load_and_scale_image('delete.png'),
    load_and_scale_image('legal.png'),
    load_and_scale_image('obsolete.png'),
    load_and_scale_image('orgcommitment.png'),
    load_and_scale_image('softwarebug.png'),
    load_and_scale_image('virus.png')
]

# Timer for spawning new food
food_timer = pygame.time.get_ticks()  # Initialize timer
last_food_type = 'increase'  # Track the last food type

# List to store food items
food_items = []

# Function to display score
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

# Function to draw the snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Function to display messages
def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 3, dis_height / 3 + y_displace])

# Function to spawn food
def spawn_food(food_type=None, current_food_increase_images=None):
    global last_food_type
    if food_type is None:
        foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
        if last_food_type == 'increase':
            food_type = 'decrease'
        else:
            food_type = 'increase'
        last_food_type = food_type
    else:
        foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
        last_food_type = food_type

    # Choose a specific image based on the food type
    if food_type == 'increase':
        image = random.choice(current_food_increase_images)
    else:
        image = random.choice(food_decrease_images)

    food_items.append((foodx, foody, food_type, image))

# Main game loop
def gameLoop():
    global food_timer  # Use the global timer variable
    global dis_width, dis_height  # Ensure these are available

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    current_food_increase_images = food_increase_images_1  # Start with the initial set of images
    display_ingest_message = False  # Track whether "Ingest complete" message should be displayed
    ingest_message_start_time = 0  # Store the time when the message is displayed

    spawn_food('increase', current_food_increase_images)  # Spawn initial food item that increases score

    # Instructions screen before the game starts
    game_start = False
    while not game_start:
        dis.fill(blue)
        message("Welcome to Preservation Python!", white, -200)
        message("Collect preservation information.", white, -100)
        message("Avoid data loss and obsolescence.", white)
        message("Maintain accessibility!", white, 100)
        message("Use the arrow keys to move. Press the SPACEBAR to start", green, 200)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_start = True

        clock.tick(15)  # Control the frame rate of the instructions screen

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("Preservation Failure! The digital object is lost.", red)
            message("Press R to Play Again or Q-Quit", red, +50)
            Your_score(Length_of_snake - 1)  # Update the score display
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        gameLoop()
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0 
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                    
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        # Check if score is greater than or equal to 25 to switch images
        if Length_of_snake - 1 >= 5 and current_food_increase_images != food_increase_images_2:
            current_food_increase_images = food_increase_images_2
            display_ingest_message = True  # Trigger the display of the "Ingest complete" message
            ingest_message_start_time = pygame.time.get_ticks()  # Record the time the message is shown

        # Display "Ingest complete" message for 3 seconds
        if display_ingest_message:
            if pygame.time.get_ticks() - ingest_message_start_time < 3000:  # 3000 milliseconds = 3 seconds
                message("Ingest complete. Keep it accessible!", green, -200)
            else:
                display_ingest_message = False  # Stop displaying the message after 3 seconds

        # Check timer to spawn new food every 10 seconds
        if pygame.time.get_ticks() - food_timer > 10000:  # 10,000 milliseconds = 10 seconds
            spawn_food('decrease')  # Spawn a food item that decreases score
            food_timer = pygame.time.get_ticks()  # Reset timer

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)  # Update the score display

        # Draw all food items
        for (foodx, foody, food_type, image) in food_items:
            if food_type == 'increase':
                pygame.draw.rect(dis, white_background, [foodx, foody, snake_block, snake_block])
            else:
                pygame.draw.rect(dis, red_background, [foodx, foody, snake_block, snake_block])
            # Draw the image on top of the background
            dis.blit(image, (foodx, foody))

        # Check collision with each food item
        for i, (foodx, foody, food_type, _) in enumerate(food_items):
            if x1 == foodx and y1 == foody:
                if food_type == 'increase':
                    Length_of_snake += 1
                    spawn_food('increase', current_food_increase_images)  # Spawn new food item
                elif food_type == 'decrease':
                    Length_of_snake = max(1, Length_of_snake // 2)  # Halve the snake's length, ensuring it doesn't go below 1
                    if Length_of_snake <= 1:
                        game_close = True
                del food_items[i]  # Remove the food item after collision
                break

        Your_score(Length_of_snake - 1)  # Ensure the score updates immediately after eating
        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
