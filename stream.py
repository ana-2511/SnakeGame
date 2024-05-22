import pygame
import random
from PIL import Image
import io
import streamlit as st

# Initialize Pygame
pygame.init()

# Define colors for light theme
LIGHT_THEME = {
    "BACKGROUND": (255, 255, 255),
    "TEXT": (0, 0, 0),
    "BUTTON_NORMAL": (0, 128, 0),
    "BUTTON_HOVER": (192, 192, 192),
    "SNAKE_1": (0, 255, 0),
    "SNAKE_2": (0, 0, 255),
    "APPLE": (255, 0, 0)
}

# Set the theme to light
current_theme = LIGHT_THEME

# Set display dimensions
display_width = 800
display_height = 600

# Set up display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# Set snake and food sizes
block_size = 20
snake_speed = 10  # Decreased snake speed

# Define BLACK color
BLACK = (0, 0, 0)

# Set up display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, 30)  # Decreased font size
small_font = pygame.font.SysFont(None, 25)

# Function to display message on screen
def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    gameDisplay.blit(mesg, [display_width / 3, display_height / 3 + y_displace])  # Centered

# Function to display button text
def text_objects(text, font):
    textSurface = font.render(text, True, current_theme["TEXT"])
    return textSurface, textSurface.get_rect()

# Function to draw buttons
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    text_surf, text_rect = text_objects(msg, small_font)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(text_surf, text_rect)

# Function to display scores
def Your_score(score1, score2=None):
    value1 = font_style.render("Player 1 Score: " + str(score1), True, current_theme["TEXT"])
    gameDisplay.blit(value1, [10, 10])
    if score2 is not None:
        value2 = font_style.render("Player 2 Score: " + str(score2), True, current_theme["TEXT"])
        gameDisplay.blit(value2, [display_width - 200, 10])

# Function to draw the snake
def our_snake(block_size, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(gameDisplay, color, [x[0], x[1], block_size, block_size])

# Function to draw the food (circle)
def draw_food(x, y, radius, color):
    pygame.draw.circle(gameDisplay, color, (x + radius, y + radius), radius)

# Main game loop
def gameLoop(multiplayer=False):
    game_exit = False
    game_over = False

    lead_x_1 = display_width / 4
    lead_y_1 = display_height / 2
    lead_x_change_1 = 0
    lead_y_change_1 = 0
    last_direction_1 = None  # Track the last direction for player 1

    if multiplayer:
        lead_x_2 = 3 * display_width / 4
        lead_y_2 = display_height / 2
        lead_x_change_2 = 0
        lead_y_change_2 = 0
        last_direction_2 = None  # Track the last direction for player 2

        snake_list_2 = []
        snake_length_2 = 1
    else:
        lead_x_2 = None
        lead_y_2 = None
        lead_x_change_2 = None
        lead_y_change_2 = None
        snake_list_2 = None
        snake_length_2 = None

    snake_list_1 = []
    snake_length_1 = 1

    randAppleX = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
    randAppleY = round(random.randrange(0, display_height - block_size) / 20.0) * 20.0

    while not game_exit:
        while game_over:
            gameDisplay.fill(current_theme["BACKGROUND"])
            message("Game Over!", current_theme["TEXT"], y_displace=-50)
            message("Press C to Play Again or Q to Quit", current_theme["TEXT"], y_displace=0)
            message("Final Scores: Player 1: " + str(snake_length_1 - 1) + ((" Player 2: " + str(snake_length_2 - 1)) if multiplayer else ""), current_theme["TEXT"], y_displace=50)
            button("Play Again", 150, 450, 150, 50, current_theme["BUTTON_NORMAL"], current_theme["BUTTON_HOVER"], start_menu)
            button("Exit", 500, 450, 150, 50, current_theme["BUTTON_NORMAL"], current_theme["BUTTON_HOVER"], pygame.quit)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        start_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if last_direction_1 != "RIGHT":
                        lead_x_change_1 = -block_size
                        lead_y_change_1 = 0
                        last_direction_1 = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    if last_direction_1 != "LEFT":
                        lead_x_change_1 = block_size
                        lead_y_change_1 = 0
                        last_direction_1 = "RIGHT"
                elif event.key == pygame.K_UP:
                    if last_direction_1 != "DOWN":
                        lead_y_change_1 = -block_size
                        lead_x_change_1 = 0
                        last_direction_1 = "UP"
                elif event.key == pygame.K_DOWN:
                    if last_direction_1 != "UP":
                        lead_y_change_1 = block_size
                        lead_x_change_1 = 0
                        last_direction_1 = "DOWN"
                if multiplayer:
                    if event.key == pygame.K_a:
                        if last_direction_2 != "RIGHT":
                            lead_x_change_2 = -block_size
                            lead_y_change_2 = 0
                            last_direction_2 = "LEFT"
                    elif event.key == pygame.K_d:
                        if last_direction_2 != "LEFT":
                            lead_x_change_2 = block_size
                            lead_y_change_2 = 0
                            last_direction_2 = "RIGHT"
                    elif event.key == pygame.K_w:
                        if last_direction_2 != "DOWN":
                            lead_y_change_2 = -block_size
                            lead_x_change_2 = 0
                            last_direction_2 = "UP"
                    elif event.key == pygame.K_s:
                        if last_direction_2 != "UP":
                            lead_y_change_2 = block_size
                            lead_x_change_2 = 0
                            last_direction_2 = "DOWN"
                elif event.key == pygame.K_p:
                    pause()

        if lead_x_1 >= display_width or lead_x_1 < 0 or lead_y_1 >= display_height or lead_y_1 < 0:
            game_over = True

        if multiplayer and (lead_x_2 >= display_width or lead_x_2 < 0 or lead_y_2 >= display_height or lead_y_2 < 0):
            game_over = True

        lead_x_1 += lead_x_change_1
        lead_y_1 += lead_y_change_1
        if multiplayer:
            lead_x_2 += lead_x_change_2
            lead_y_2 += lead_y_change_2

        gameDisplay.fill(current_theme["BACKGROUND"])

        # Draw the food (circle)
        draw_food(randAppleX, randAppleY, block_size // 2, current_theme["APPLE"])

        snake_head_1 = []
        snake_head_1.append(lead_x_1)
        snake_head_1.append(lead_y_1)
        snake_list_1.append(snake_head_1)
        if len(snake_list_1) > snake_length_1:
            del snake_list_1[0]

        if multiplayer:
            snake_head_2 = []
            snake_head_2.append(lead_x_2)
            snake_head_2.append(lead_y_2)
            snake_list_2.append(snake_head_2)
            if len(snake_list_2) > snake_length_2:
                del snake_list_2[0]

            for each_segment in snake_list_2[:-1]:
                if each_segment == snake_head_2:
                    game_over = True
                    break

            our_snake(block_size, snake_list_2, current_theme["SNAKE_2"])

        for each_segment in snake_list_1[:-1]:
            if each_segment == snake_head_1:
                game_over = True
                break

        our_snake(block_size, snake_list_1, current_theme["SNAKE_1"])
        Your_score(snake_length_1 - 1, snake_length_2 - 1 if multiplayer else None)

        pygame.display.update()

        if lead_x_1 == randAppleX and lead_y_1 == randAppleY:
            randAppleX = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
            randAppleY = round(random.randrange(0, display_height - block_size) / 20.0) * 20.0
            snake_length_1 += 1

        if multiplayer and (lead_x_2 == randAppleX and lead_y_2 == randAppleY):
            randAppleX = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
            randAppleY = round(random.randrange(0, display_height - block_size) / 20.0) * 20.0
            snake_length_2 += 1

        clock.tick(snake_speed)
        # Update display
        pygame.display.update()

# Function to capture the game screen
def capture_screen():
    # Capture the game screen as a Pygame Surface
    screen_surface = pygame.display.get_surface()
    
    # Convert the Pygame Surface to a numpy array
    screen_array = pygame.surfarray.array3d(screen_surface)
    
    # Convert the numpy array to a PIL Image
    pil_image = Image.fromarray(screen_array)
    
    # Convert the PIL Image to bytes
    img_bytes = io.BytesIO()
    pil_image.save(img_bytes, format='PNG')
    
    return img_bytes.getvalue()

# Display the captured game screen in Streamlit
st.image(capture_screen(), caption='Snake Game')

# Function to pause the game
def pause():
    paused = True
    message("Paused", current_theme["TEXT"])
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)

# Function to display game instructions
def show_instructions():
    instructions_shown = True
    while instructions_shown:
        gameDisplay.fill(current_theme["BACKGROUND"])
        message("Game Instructions", current_theme["TEXT"], y_displace=-100)
        instructions = [
            "Single Player:",
            "Use arrow keys to move the snake",
            "You can't reverse the direction",
            "Multiplayer:",
            "Player 1: Use arrow keys to move",
            "Player 2: Use WASD keys to move",
            "You can't reverse the direction",
            "Pause Game: Press P",
            "Quit Game: Press Q"
        ]
        y_offset = -50
        for line in instructions:
            text = small_font.render(line, True, current_theme["TEXT"])
            gameDisplay.blit(text, (50, display_height // 2 + y_offset))
            y_offset += 30
        button("Back", 350, 450, 100, 50, current_theme["BUTTON_NORMAL"], current_theme["BUTTON_HOVER"], start_menu)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    instructions_shown = False

# Function to start menu
def start_menu():
    menu = True

    while menu:
        gameDisplay.fill(current_theme["BACKGROUND"])
        message("Welcome to Snake Game", current_theme["TEXT"], y_displace=-100)
        button("Single Player", 150, 200, 150, 50, current_theme["BUTTON_NORMAL"], current_theme["BUTTON_HOVER"], lambda: start_game(multiplayer=False))
        button("Multiplayer", 450, 200, 200, 50, current_theme["BUTTON_NORMAL"], current_theme["BUTTON_HOVER"], lambda: start_game(multiplayer=True))
        button("Instructions", 300, 300, 200, 50, current_theme["BUTTON_NORMAL"], current_theme["BUTTON_HOVER"], show_instructions)
        button("Exit", 350, 400, 100, 50, current_theme["BUTTON_NORMAL"], current_theme["BUTTON_HOVER"], pygame.quit)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Function to start the game loop
def start_game(multiplayer=False):
    gameLoop(multiplayer)

# Function to exit the game
def exit_game():
    pygame.quit()
    quit()

# Update the button function to call exit_game when the "Exit" button is pressed
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    text_surf, text_rect = text_objects(msg, small_font)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(text_surf, text_rect)

# Update the "Exit" button to call the exit_game function
button("Exit", 500, 450, 150, 50, current_theme["BUTTON_NORMAL"], current_theme["BUTTON_HOVER"], exit_game)


# Start the game
start_menu()
