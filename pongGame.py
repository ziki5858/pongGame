import random
import pygame
from GameBoardManager import GameBoardManager
from GameTextManager import GameTextManager
from BallManager import BallManager
from MovementManager import MovementManager
from constants import *
import GlobalData

def main():
    pygame.font.init()
    BallManager.init_sounds()
    start_game()

def start_game():
    GameBoardManager.upload_screen("pong", WHITE, RED)
    GameBoardManager.upload_sprites()
    check_quit("move")

def againstWho():
    # Clear screen with white background
    GlobalData.screen.fill(WHITE)

    # Render the title text and center it
    title_font = pygame.font.Font(None, 60)
    title_surf = title_font.render('Choose Game Mode:', True, RED)
    title_x = (gWidth - title_surf.get_width()) // 2
    GlobalData.screen.blit(title_surf, (title_x, 40))

    # Define the options and their vertical positions
    options = [
        ('Press C for Computer', 140),
        ('Press F for Friend', 200)
    ]

    # Render each option and center it
    font = pygame.font.Font(None, 50)
    for text, y in options:
        text_surf = font.render(text, True, BLACK)
        text_x = (gWidth - text_surf.get_width()) // 2
        GlobalData.screen.blit(text_surf, (text_x, y))

    # Update the display and wait for user input
    pygame.display.flip()
    return check_quit('start')

def check_quit(status):
    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if status == 'move':
                    MovementManager.sprite_movement(event)
                if status == 'over':
                    start_game()
                if status == "start":
                    if event.key == pygame.K_c:
                        return True
                    if event.key == pygame.K_f:
                        return False
        if status == 'move':
            if not events and GlobalData.against_com:
                if random.randrange(COM_LEVEL) == 5:
                    MovementManager.sprite_movement(None)
            BallManager.ball_move()
            clock.tick(REFRESH)

if __name__ == "__main__":
    main()
