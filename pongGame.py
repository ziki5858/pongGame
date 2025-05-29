import sys

from GameTextManager import GameTextManager
from GameBoardManager import GameBoardManager
from BallManager import BallManager
from MovementManager import MovementManager
from constantsGlobal import *
from InputBox import game_settings


def main():
    """
    Initialize Pygame and game settings, then start the game loop.
    """
    pygame.init()
    GlobalData.screen = pygame.display.set_mode((gWidth, gHeight))
    pygame.display.set_caption("Pong")
    BallManager.init_sounds()

    # Show settings panel
    game_settings()
    # Clear any leftover events so first keypress registers in opponent selection
    pygame.event.clear()

    # Choose opponent mode
    GlobalData.against_com = againstWho()
    start_game()


def start_game():
    """
    Prepare the game board and enter continuous play mode.
    """
    GameBoardManager.upload_screen("pong", WHITE, RED)
    GameBoardManager.upload_sprites()
    check_quit("move")


def againstWho():
    """
    Displays an animated menu for selecting opponent type.
    Returns True if Computer is selected, False for Friend.
    """
    top_base = (100, 100, 160)
    bottom_base = (180, 180, 240)
    prompt = 'Choose Game Mode'
    options = [
        ("Computer (C)", RED, gHeight // 2),
        ("Friend (F)", RED, gHeight // 2 + 70)
    ]
    title_font = pygame.font.Font(None, 72)
    option_font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()

    while True:
        # draw pulsating gradient background
        GameTextManager.draw_gradient_background(
            GlobalData.screen,
            gWidth, gHeight,
            top_base, bottom_base
        )

        # draw centered menu title and options
        GameTextManager.draw_menu(
            GlobalData.screen,
            gWidth, gHeight,
            prompt, options,
            title_font, option_font
        )

        pygame.display.flip()

        # poll keyboard for selection
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            return True
        if keys[pygame.K_f]:
            return False

        # handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(REFRESH)


def check_quit(status):
    """
    Core event loop: processes input and updates AI/ball each frame.
    status 'move': gameplay, 'start': opponent selection, 'over': restart.
    """
    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if status == 'move':
                    MovementManager.sprite_movement(event)
                elif status == 'over':
                    start_game()
                elif status == 'start':
                    return againstWho()
        if status == 'move':
            # Always update AI movement
            MovementManager.sprite_movement(None)
            # Move the ball and redraw
            BallManager.ball_move()
        clock.tick(REFRESH)


if __name__ == "__main__":
    main()
