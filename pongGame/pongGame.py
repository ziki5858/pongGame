import random
import pygame

# region Definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
gWidth = 500
gHeight = 500
REFRESH = 60
BallSpeedPix = 1.9
AddSpeedBall = 0.1
LIFE = 10
Xdeviation = 15


# endregion

class GameSprite(pygame.sprite.Sprite):
    def update_loc(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_pos(self):
        return self.rect.x, self.rect.y

    def get_posX(self):
        return self.rect.x

    def get_posY(self):
        return self.rect.y

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height


class Player(GameSprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.image = pygame.image.load('sprite.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.get_height() / 2
        self.leftLife = LIFE
        self.rightLife = LIFE

    def update_left_Life(self):
        self.leftLife -= 1

    def update_right_Life(self):
        self.rightLife -= 1

    def get_life(self):
        return self.leftLife, self.rightLife


class Ball(GameSprite):
    def __init__(self, x, y):
        super(Ball, self).__init__()
        self.image = pygame.image.load('ball.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x - self.get_width() / 2
        self.rect.y = y - self.get_height() / 2
        self.xMOve = BallSpeedPix
        self.yMove = -BallSpeedPix

    def update_Move(self, x, y):
        self.xMOve = x
        self.yMove = y

    def get_move(self):
        return self.xMOve, self.yMove


def main():
    start_game()


def start_game():
    upload_screen("pong", WHITE, RED)
    soundList = upload_sound()
    upload_sprites(3)
    check_quit(soundList)


def upload_screen(title, bColor, sColor):
    """ Get: game title,  background color, and sketch color
    Output screen with those details"""
    global screen
    pygame.init()
    screen = pygame.display.set_mode((gWidth, gHeight))
    screen.fill(bColor)
    pygame.display.set_caption(str(title))
    pygame.draw.line(screen, sColor, (gWidth / 2, 0), (gWidth / 2, gHeight), 2)
    pygame.display.flip()


def upload_sprites(amount):
    """get amount int that use to sprite paddles
    output paddles and ball"""
    global sprite_list
    global ball_list
    sprite_list = pygame.sprite.Group()
    ball_list = pygame.sprite.Group()
    nextSpriteD = 0
    for i in range(int(2)):
        sprite_list.add(Player(nextSpriteD, gHeight / 2))
        nextSpriteD = gWidth - sprite_list.sprites()[i].get_width()
    for i in range(int(amount)):
        ball_list.add(Ball(gWidth / 2, gHeight / 2))
    sprite_list.draw(screen)
    ball_list.draw(screen)
    pygame.display.flip()


def r_screen(bColor, sColor):
    """get background color, sketch color
    Output screen"""
    screen.fill(bColor)
    pygame.draw.line(screen, sColor, (gWidth / 2, 0), (gWidth / 2, gHeight), 2)
    sprite_list.draw(screen)
    ball_list.draw(screen)
    show_score()
    pygame.display.flip()


def sprite_movement(event):
    lSprite = sprite_list.sprites()[0]
    rSprite = sprite_list.sprites()[1]
    xLeft, yLeft = lSprite.get_pos()
    xRight, yRight = rSprite.get_pos()
    upDownLeft = [pygame.K_s, pygame.K_w]
    upDownRight = [pygame.K_DOWN, pygame.K_UP]
    moveAmount = [22, -22]
    for i in range(2):
        # region leftYMove
        if event.key == upDownLeft[i]:
            if 0 < yLeft + moveAmount[i] < gHeight - lSprite.get_height():
                yLeft = yLeft + moveAmount[i]
            elif upDownLeft[i] == pygame.K_w:
                yLeft = 0
            elif upDownLeft[i] == pygame.K_s:
                yLeft = gHeight - lSprite.get_height()
            lSprite.update_loc(xLeft, yLeft)
        # endregion
        # region rightYMove
        if event.key == upDownRight[i]:
            if 0 < yRight + moveAmount[i] < gHeight - rSprite.get_height():
                rSprite.update_loc(xRight, yRight + moveAmount[i])
            elif upDownRight[i] == pygame.K_UP:
                rSprite.update_loc(xRight, 0)
            elif upDownRight[i] == pygame.K_DOWN:
                rSprite.update_loc(xRight, gHeight - rSprite.get_height())
        # endregion


def ball_move(amount, soundList):
    for i in range(amount):
        ball = ball_list.sprites()[i]
        check_game_over(*sprite_list.sprites()[0].get_life())
        xBall, yBall = ball.get_pos()
        xLeft, yLeft = sprite_list.sprites()[0].get_pos()
        xRight, yRight = sprite_list.sprites()[1].get_pos()
        xMovement, yMovement = ball.get_move()
        rList = [abs(yMovement), (-abs(yMovement))]
        paddleWidth = sprite_list.sprites()[1].get_width()
        paddleHeight = sprite_list.sprites()[1].get_height()
        edgeUp = yBall
        edgeDown = yBall + ball.get_height()

        # region paddles toach
        if xBall >= xRight - paddleWidth - Xdeviation and yRight <= edgeUp <= yRight + paddleHeight or \
                xBall >= xRight - paddleWidth - Xdeviation and yRight <= edgeDown <= yRight + paddleHeight:
            sound(soundList[0])
            xMovement = -abs(xMovement) - AddSpeedBall
            yMovement = random.choice(rList)

        elif xBall <= xLeft + Xdeviation and yLeft <= edgeUp <= yLeft + paddleHeight or \
                xBall <= xLeft + Xdeviation and yLeft <= edgeDown <= yLeft + paddleHeight:
            sound(soundList[0])
            xMovement = abs(xMovement) + AddSpeedBall
            yMovement = random.choice(rList)
        # endregion

        # region edges toach
        elif gHeight - ball.get_height() <= yBall:
            yMovement = -abs(yMovement)

        elif 0 >= yBall:
            yMovement = abs(yMovement)
        # endregion

        # region Touching the sides - point
        elif gWidth - ball.get_width() <= xBall:
            sound(soundList[1])
            ball_to_center(i)
            xBall, yBall = ball.get_pos()
            xMovement = -BallSpeedPix
            yMovement = BallSpeedPix
            sprite_list.sprites()[0].update_right_Life()

        elif 0 >= xBall:
            sound(soundList[1])
            ball_to_center(i)
            xBall, yBall = ball.get_pos()
            xMovement = BallSpeedPix
            yMovement = -BallSpeedPix
            sprite_list.sprites()[0].update_left_Life()
        # endregion

        ball.update_Move(xMovement, yMovement)
        xMovement, yMovement = ball.get_move()
        xBall += xMovement
        yBall += yMovement
        ball.update_loc(xBall, yBall)
        r_screen(WHITE, RED)


def ball_to_center(i):
    ball_list.sprites()[i].update_loc((gWidth / 2 - ball_list.sprites()[0].get_width() / 2),
                                      (gHeight / 2 - ball_list.sprites()[0].get_height() / 2))


def check_game_over(leftLife, rightLife):
    if leftLife == 0:
        game_over_m('Right')
    elif rightLife == 0:
        game_over_m("Left")


def check_quit(soundList):
    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                sprite_movement(event)
        ball_move(3, soundList)
        clock.tick(REFRESH)


def show_score():
    pygame.font.init()
    score = [*sprite_list.sprites()[0].get_life()]
    font = pygame.font.Font(None, 50)
    text1 = font.render(('life left:     ' + str(+score[0])), 1, BLACK)
    screen.blit(text1, (20, 30))
    text2 = font.render(str(score[1]), 1, BLACK)
    screen.blit(text2, (310, 30))


def game_over_m(winner):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    text1 = font.render('Game over:  ' + winner + '  win', 1, BLACK)
    screen.blit(text1, (65, 200))
    font = pygame.font.Font(None, 25)
    text2 = font.render('Press Enter to regame', 1, RED)
    screen.blit(text2, (160, 250))
    pygame.display.flip()
    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game()
        clock.tick(REFRESH)


def sound(soundNumber):
    channel = pygame.mixer.find_channel()
    if channel is not None:
        channel.queue(soundNumber)


def upload_sound():
    pygame.mixer.init(frequency=22050, size=-16, channels=4)
    soundList = [pygame.mixer.Sound('Swipe Swoosh Transition Sound Effect.mp3'),
                 pygame.mixer.Sound('Video Game Beep - Sound Effect.mp3')]
    return soundList


if __name__ == "__main__":
    main()
