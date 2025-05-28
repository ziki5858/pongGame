import pygame
import GlobalData
from constants import *

class InputBox:
    def __init__(self, x, y, w, h, label, max_length=1, valid_range=(1, 9)):
        self.rect = pygame.Rect(x, y, w, h)
        self.base_color = pygame.Color('lightgray')
        self.active_color = pygame.Color('deepskyblue')
        self.error_color = pygame.Color('tomato')
        self.color = self.base_color
        self.text = ''
        self.label = label
        self.font = pygame.font.SysFont('Arial', 28)
        self.txt_surface = self.font.render('', True, pygame.Color('dimgray'))
        self.active = False
        self.max_length = max_length
        self.error = False
        self.valid_range = valid_range

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.active_color if self.active else self.base_color
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() and len(self.text) < self.max_length:
                self.text += event.unicode
            self.error = not (self.text.isdigit() and self.valid_range[0] <= int(self.text) <= self.valid_range[1])
            self.txt_surface = self.font.render(self.text, True, pygame.Color('black'))

    def draw(self, screen):
        # label with range
        label_surf = self.font.render(f"{self.label} ({self.valid_range[0]}–{self.valid_range[1]})", True, pygame.Color('white'))
        screen.blit(label_surf, (self.rect.x - label_surf.get_width() - 15, self.rect.y + 8))
        # box background
        pygame.draw.rect(screen, pygame.Color('white'), self.rect, border_radius=5)
        # text
        screen.blit(self.txt_surface, (self.rect.x + 8, self.rect.y + 8))
        # border
        border_color = self.error_color if self.error else (self.active_color if self.active else pygame.Color('gray'))
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=5)

    def is_valid(self):
        return not self.error and self.text.isdigit()

    def get_value(self):
        return int(self.text) if self.text.isdigit() else None


def game_settings():
    pygame.init()
    screen = GlobalData.screen
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 36, bold=True)

    # gradient background
    def draw_gradient_bg():
        for i in range(gHeight):
            ratio = i / gHeight
            r = int(30 + (220 - 30) * ratio)
            g = int(144 + (255 - 144) * ratio)
            b = 255
            pygame.draw.line(screen, (r, g, b), (0, i), (gWidth, i))

    boxes = [
        InputBox(250, 150, 80, 50, 'Balls', max_length=1, valid_range=(1,3)),
        InputBox(250, 240, 80, 50, 'Lives', max_length=1, valid_range=(1,9)),
        InputBox(250, 330, 80, 50, 'AI Lv', max_length=1, valid_range=(1,3)),
    ]

    btn_rect = pygame.Rect((gWidth//2 - 100, 420, 200, 60))
    confirm_surf = font.render("Let's Play!", True, pygame.Color('white'))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            for box in boxes:
                box.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                clicked = True

        # draw
        draw_gradient_bg()
        title = font.render('Ready to Pong!', True, pygame.Color('white'))
        screen.blit(title, ((gWidth - title.get_width())//2, 50))

        for box in boxes:
            box.draw(screen)

        valid = all(box.is_valid() for box in boxes)
        if btn_rect.collidepoint(mouse_pos):
            btn_color = pygame.Color('limegreen') if valid else pygame.Color('gray50')
        else:
            btn_color = pygame.Color('seagreen') if valid else pygame.Color('darkgray')
        pygame.draw.rect(screen, btn_color, btn_rect, border_radius=10)
        screen.blit(confirm_surf, (btn_rect.x + (btn_rect.width - confirm_surf.get_width())//2,
                                   btn_rect.y + (btn_rect.height - confirm_surf.get_height())//2))
        if valid and btn_rect.collidepoint(mouse_pos) and clicked:
            GlobalData.ball_amount = boxes[0].get_value()
            GlobalData.player_life = boxes[1].get_value()
            level_map = {1:30, 2:15, 3:5}
            GlobalData.com_level = level_map[boxes[2].get_value()]
            running = False

        pygame.display.flip()
        clock.tick(30)