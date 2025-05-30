from constantsGlobal import gWidth, gHeight, GlobalData
from GameTextManager import GameTextManager
import pygame


class InputBox:
    """
    Single-line numeric input:
      • label and valid-range hint
      • change border colour on focus / error
      • self-validation (digits in given range)
    """

    _FONT = None          # lazy-initialised after pygame.init()

    # ---------- construction ----------
    def __init__(self, x, y, w, h, label,
                 max_length=1, valid_range=(1, 9)):
        self.rect = pygame.Rect(x, y, w, h)

        # colours
        self.base_color   = pygame.Color("lightgray")
        self.active_color = pygame.Color("deepskyblue")
        self.error_color  = pygame.Color("tomato")
        self.color        = self.base_color

        # data
        self.text        = ""
        self.label       = label
        self.max_length  = max_length
        self.valid_range = valid_range
        self.active      = False
        self.error       = False

        # first blank surface
        self.txt_surface = self._font().render("",
                                               True, pygame.Color("dimgray"))

    # ---------- internal helpers ----------
    @classmethod
    def _font(cls):
        """Return a cached Font; create on first call (after pygame.init())."""
        if cls._FONT is None:
            cls._FONT = pygame.font.SysFont("Arial", 28)
        return cls._FONT

    # ---------- event handling ----------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color  = self.active_color if self.active else self.base_color

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif (event.unicode.isdigit()
                  and len(self.text) < self.max_length):
                self.text += event.unicode

            # validate
            self.error = not (
                self.text.isdigit()
                and self.valid_range[0] <= int(self.text) <= self.valid_range[1]
            )
            self.txt_surface = self._font().render(
                self.text, True, pygame.Color("black")
            )

    # ---------- drawing ----------
    def draw(self, screen):
        # label + range
        label = f"{self.label} ({self.valid_range[0]}–{self.valid_range[1]})"
        GameTextManager.draw_text(
            label, 28, True, pygame.Color("white"),
            self.rect.x - 15 - GameTextManager.font_width(label, 28),
            self.rect.y + 8
        )

        # box + text
        pygame.draw.rect(screen, pygame.Color("white"),
                         self.rect, border_radius=5)
        screen.blit(self.txt_surface,
                    (self.rect.x + 8, self.rect.y + 8))

        border = (self.error_color if self.error else
                  self.active_color if self.active
                  else pygame.Color("gray"))
        pygame.draw.rect(screen, border,
                         self.rect, 3, border_radius=5)

    # ---------- public helpers ----------
    def is_valid(self):
        return not self.error and self.text.isdigit()

    def get_value(self):
        return int(self.text) if self.text.isdigit() else None


# ----------------------------------------------------------------------
# Settings panel (unchanged logic, just uses InputBox._font internally)
# ----------------------------------------------------------------------
def game_settings():
    pygame.init()                              # ensures font module ready
    screen = GlobalData.screen
    clock  = pygame.time.Clock()
    font_sz = 36

    boxes = [
        InputBox(250, 150, 80, 50, "Balls", max_length=1, valid_range=(1, 3)),
        InputBox(250, 240, 80, 50, "Lives", max_length=1, valid_range=(1, 9)),
        InputBox(250, 330, 80, 50, "AI Lv", max_length=1, valid_range=(1, 3)),
    ]
    btn_rect = pygame.Rect(gWidth//2 - 100, 420, 200, 60)

    running = True
    while running:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                click = True
            for box in boxes:
                box.handle_event(event)

        # UI
        GameTextManager.draw_settings_background(screen, gWidth, gHeight)
        GameTextManager.draw_text(
            "Ready to Pong!", font_sz, True, pygame.Color("white"),
            (gWidth - GameTextManager.font_width("Ready to Pong!", font_sz))//2,
            50
        )
        for box in boxes:
            box.draw(screen)

        all_valid = all(box.is_valid() for box in boxes)
        GameTextManager.draw_button(btn_rect, "Let's Play!",
                                    font_sz, all_valid)

        # apply
        if all_valid and btn_rect.collidepoint(pygame.mouse.get_pos()) and click:
            GlobalData.ball_amount  = boxes[0].get_value()
            GlobalData.player_life  = boxes[1].get_value()
            level_map = {1: 30, 2: 15, 3: 5}
            GlobalData.com_level    = level_map[boxes[2].get_value()]
            running = False

        pygame.display.flip()
        clock.tick(30)
