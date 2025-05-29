import sys
import math

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
    Display animated opponent-selection menu and return True if Computer chosen.
    Uses polling of key state to capture first keypress immediately.
    """
    w, h = gWidth, gHeight
    top_base = (100, 100, 160)
    bot_base = (180, 180, 240)
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 72)
    font_opt = pygame.font.Font(None, 50)
    prompt = 'Choose Game Mode'
    options = [("Computer (C)", RED, h // 2), ("Friend (F)", RED, h // 2 + 70)]

    while True:
        t = pygame.time.get_ticks()
        pulse = (math.sin(t * 0.005) + 1) / 2
        # Gradient background
        top_color = [int(top_base[i] * (1 - pulse) + bot_base[i] * pulse) for i in range(3)]
        bot_color = [int(bot_base[i] * (1 - pulse) + top_base[i] * pulse) for i in range(3)]
        for y in range(h):
            ratio = y / (h - 1)
            r = int(top_color[0] * (1 - ratio) + bot_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bot_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bot_color[2] * ratio)
            pygame.draw.line(GlobalData.screen, (r, g, b), (0, y), (w, y))
        # Title and options
        shadow = font_title.render(prompt, True, BLACK)
        title = font_title.render(prompt, True, RED)
        tx, ty = title.get_size()
        GlobalData.screen.blit(shadow, ((w - tx) // 2 + 3, h // 4 + 3))
        GlobalData.screen.blit(title, ((w - tx) // 2, h // 4))
        for label, color, yy in options:
            surf = font_opt.render(label, True, color)
            rect = surf.get_rect(center=(w // 2, yy))
            bg = pygame.Surface((rect.width + 20, rect.height + 10), pygame.SRCALPHA)
            bg.fill((255, 255, 255, 100))
            GlobalData.screen.blit(bg, bg.get_rect(center=rect.center))
            GlobalData.screen.blit(surf, rect)
        pygame.display.flip()

        # Poll key state
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            return True
        if keys[pygame.K_f]:
            return False

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
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
