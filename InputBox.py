import pygame
import GlobalData
from constants import *

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('black')
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 2 and event.unicode.isdigit():
                    self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)
        return None

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self):
        return self.text

def game_settings():
    screen = GlobalData.screen
    font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()

    box_balls = InputBox(300, 100, 50, 40)
    box_lives = InputBox(300, 180, 50, 40)
    box_level = InputBox(300, 260, 50, 40)
    boxes = [box_balls, box_lives, box_level]

    running = True
    while running:
        screen.fill(WHITE)

        screen.blit(font.render('Balls (1–3):', True, BLACK), (100, 110))
        screen.blit(font.render('Lives (1–9):', True, BLACK), (100, 190))
        screen.blit(font.render('AI Level (1–3):', True, BLACK), (100, 270))
        screen.blit(font.render('Press ENTER to confirm', True, RED), (100, 340))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                try:
                    GlobalData.ball_amount = min(max(int(box_balls.get_value()), 1), 3)
                    GlobalData.player_life = min(max(int(box_lives.get_value()), 1), 9)
                    level_map = {'1': 30, '2': 15, '3': 5}
                    GlobalData.com_level = level_map.get(box_level.get_value(), 15)
                    running = False
                except ValueError:
                    pass  # Ignore invalid input
            for box in boxes:
                box.handle_event(event)

        for box in boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)
