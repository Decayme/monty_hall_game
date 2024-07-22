import pygame
import sys
import random as r

# Initialize Pygame
pygame.init()

# Function to play Monty Hall game
def play_monty_hall_game(door_rects):
    car = r.randint(1, 3)

    user_pick = None
    switch = None

    while user_pick is None or switch is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(door_rects):
                    if rect.collidepoint(mouse_pos):
                        user_pick = i + 1  # Convert index to door number
                        switch = None  # Reset switch choice if new door is clicked

    print(f"Chosen door: {user_pick}")

    # Determine outcomes based on user_pick
    if user_pick == car:
        goat_door = r.choice([door for door in range(1, 4) if door != user_pick])
        result_text = f"Behind door number {goat_door} is a Goat"
        switch = False
    else:
        goat_door = [door for door in range(1, 4) if door != user_pick and door != car][0]
        result_text = f"Behind door number {goat_door} is a Goat"
        switch = True

    print(f"Result text: {result_text}, Switch: {switch}")
    return result_text, switch


# Main game loop
def main():
    # Pygame setup
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Monty Hall Game')

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Load images and scale them
    door_closed_img = pygame.image.load("icons/door_closed.png").convert_alpha()
    door_open_img = pygame.image.load("icons/door_open.png").convert_alpha()

    # Scale both closed and open door images
    door_closed_img = pygame.transform.scale(door_closed_img, (100, 150))
    door_open_img = pygame.transform.scale(door_open_img, (100, 150))

    # Initial positions and rectangles of the doors
    door_positions = [
        (150, 300),  # Position for door 1
        (350, 300),  # Position for door 2
        (550, 300)   # Position for door 3
    ]

    # Create a list of rectangles for the doors
    door_rects = [door_closed_img.get_rect(topleft=pos) for pos in door_positions]

    running = True
    game_running = False
    result_text = ""
    switch = None
    user_pick = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_running:
                        game_running = True
                        result_text, switch = play_monty_hall_game(door_rects)
                        print(f"Game started: result_text={result_text}, switch={switch}")

        # Ensure screen is valid before drawing
        if pygame.display.get_surface() is not None:
            screen.fill(WHITE)  # Fill the screen with white

            if not game_running:
                # Draw initial game start prompt
                text_surface = font.render("Press SPACE to start the game", True, BLACK)
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
                screen.blit(text_surface, text_rect)
            else:
                # Draw doors based on game state
                for i, rect in enumerate(door_rects):
                    if switch or (game_running and user_pick == i + 1):
                        screen.blit(door_open_img, rect)
                    else:
                        screen.blit(door_closed_img, rect)

                # Draw game prompts
                text_surface = font.render("Click on a door to make your choice", True, BLACK)
                screen.blit(text_surface, (screen_width // 2 - 150, 50))

                text_surface = font.render("Press 'y' to switch doors, 'n' to keep your choice", True, BLACK)
                screen.blit(text_surface, (screen_width // 2 - 250, 100))

                if result_text:
                    text_surface = font.render(result_text, True, RED if switch else BLACK)
                    screen.blit(text_surface, (screen_width // 2 - 200, screen_height - 50))

            pygame.display.flip()  # Update the full display Surface to the screen
            clock.tick(60)  # Cap the frame rate to 60 FPS

    # Cleanly exit Pygame
    print("Exiting main loop...")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
