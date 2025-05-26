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
    start_game()

def start_game():
    GameBoardManager.upload_screen("pong", WHITE, RED)
    GameBoardManager.upload_sprites()
    check_quit("move")

def againstWho():
    GameTextManager.captions(50, 'press c for against com', 1, BLACK, 20, 50, False)
    GameTextManager.captions(50, 'press f for friend com', 1, BLACK, 20, 200, True)
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