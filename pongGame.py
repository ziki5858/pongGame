import random
import pygame
from constants  import BLACK, WHITE, RED, gWidth, gHeight, REFRESH, \
                       BallSpeedPix, AddSpeedBall, LIFE, Xdeviation, \
                       BALL_AMOUNT, COM_LEVEL
from player     import Player
from ball       import Ball

sprite_speed = 25

def main():
    pygame.font.init()
    start_game()


def start_game():
    upload_screen("pong", WHITE, RED)
    upload_sprites()
    check_quit("move")


def upload_screen(title, bColor, sColor):
    """ Get: game title,  background color, and sketch color
    Output screen with those details"""
    global screen
    global against_com
    pygame.init()
    screen = pygame.display.set_mode((gWidth, gHeight))
    screen.fill(bColor)
    pygame.display.set_caption(str(title))
    against_com = againstWho()
    screen.fill(bColor)
    pygame.draw.line(screen, sColor, (gWidth / 2, 0), (gWidth / 2, gHeight), 2)
    pygame.display.flip()


def againstWho():
    """show start options in caption, return if against com or user by custom key press"""
    captions(50, 'press c for against com', 1, BLACK, 20, 50,False)
    captions(50, 'press f for friend com', 1, BLACK, 20, 200,True)
    return check_quit('start')


def upload_sprites():
    """create sprites and balls in position on the board"""
    global sprite_list
    global ball_list
    sprite_list = pygame.sprite.Group()
    ball_list = pygame.sprite.Group()
    nextSpriteD = 0
    for i in range(int(2)):
        sprite_list.add(Player(nextSpriteD, gHeight / 2))
        nextSpriteD = gWidth - sprite_list.sprites()[i].get_width()
    for i in range(int(BALL_AMOUNT)):
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


def captions(font, caption, size, color, x, y,flip):
    font = pygame.font.Font(None, font)
    text1 = font.render(caption, size, color)
    screen.blit(text1, (x, y))
    if flip:
        pygame.display.flip()


# at module scope, define your key/movement maps once
UP_DOWN_LEFT  = [pygame.K_s, pygame.K_w]
UP_DOWN_RIGHT = [pygame.K_DOWN, pygame.K_UP]

def get_paddles():
    """Return left- and right-paddle sprites."""
    sprites = sprite_list.sprites()
    return sprites[0], sprites[1]

def get_positions(lSprite, rSprite):
    """Fetch x/y for both paddles and the first ball."""
    xL, yL = lSprite.get_pos()
    xR, yR = rSprite.get_pos()
    xB, yB = ball_list.sprites()[0].get_pos()
    return xL, yL, xR, yR, xB, yB

def handle_player_move(event, sprite, x, y, key_map, speed):
    """If event matches one of key_map, move that sprite."""
    for dir_idx, key in enumerate(key_map):
        if event.key == key:
            new_y = checkBorderS(y, speed[dir_idx], sprite.get_height())
            sprite.update_loc(x, new_y)
            break

def handle_ai_move(rSprite, xR, yR, yBall, speed):
    """Exactly the same AI logic as before."""
    if yBall > yR:
        new_y = checkBorderS(yR, speed[0], rSprite.get_height())
        if new_y > yBall:
            new_y = yBall
    else:
        new_y = checkBorderS(yR, speed[1], rSprite.get_height())
        if new_y < yBall:
            new_y = yBall
    rSprite.update_loc(xR, new_y)

def sprite_movement(event):
    lSprite, rSprite = get_paddles()
    xL, yL, xR, yR, xB, yB = get_positions(lSprite, rSprite)
    speed = [sprite_speed, -sprite_speed]

    for i in range(2):
        if event is not None:
            # left paddle
            handle_player_move(event, lSprite, xL, yL, UP_DOWN_LEFT, speed)

            # right paddle (human)
            if not against_com:
                handle_player_move(event, rSprite, xR, yR, UP_DOWN_RIGHT, speed)

        # right paddle (AI)
        if against_com:
            handle_ai_move(rSprite, xR, yR, yB, speed)

def checkBorderS(object_y, move_amount, paddle_height):
    if 0 > object_y + move_amount:
        return 0
    elif object_y + move_amount > gHeight - paddle_height:
        return gHeight - paddle_height
    return object_y + move_amount


def ball_move():
    """get: amount of balls  and sound list """
    rList = [abs(BallSpeedPix), (-abs(BallSpeedPix))]
    soundList = upload_sound()

    for i in range(BALL_AMOUNT):
        # region definitions
        ball = ball_list.sprites()[i]
        check_game_over(*sprite_list.sprites()[0].get_life())
        xBall, yBall = ball.get_pos()
        xLeft, yLeft = sprite_list.sprites()[0].get_pos()
        xRight, yRight = sprite_list.sprites()[1].get_pos()
        xMovement, yMovement = ball.get_move()
        paddleWidth = sprite_list.sprites()[1].get_width()
        paddleHeight = sprite_list.sprites()[1].get_height()

        # endregion

        # region paddles touch

        if checkBordersB(xBall, yBall, xRight, yRight, paddleWidth, paddleHeight, 'r', yBall + ball.get_height()):
            sound(soundList[0])
            xMovement = -abs(xMovement) - AddSpeedBall
            yMovement = random.choice(rList)

        elif checkBordersB(xBall, yBall, xLeft, yLeft, paddleWidth, paddleHeight, 'l', yBall + ball.get_height()):
            sound(soundList[0])
            xMovement = abs(xMovement) + AddSpeedBall
            yMovement = random.choice(rList)


        # endregion

        # region edges touch
        elif gHeight - ball.get_height() <= yBall:
            yMovement = -abs(yMovement)

        elif 0 >= yBall:
            yMovement = abs(yMovement)
        # endregion

        # region Touching the sides - point
        elif gWidth - ball.get_width() <= xBall:
            edgePoint(soundList, i)
            xBall, yBall = ball.get_pos()
            xMovement = -BallSpeedPix
            yMovement = BallSpeedPix


        elif 0 >= xBall:
            edgePoint(soundList, i)
            xBall, yBall = ball.get_pos()
            xMovement = BallSpeedPix
            yMovement = -BallSpeedPix
        # endregion

        ball.update_Move(xMovement, yMovement)
        xMovement, yMovement = ball.get_move()
        xBall += xMovement
        yBall += yMovement
        ball.update_loc(xBall, yBall)
        r_screen(WHITE, RED)


def edgePoint(soundList, i):
    sound(soundList[1])
    ball_to_center(i)
    sprite_list.sprites()[0].update_right_Life()


def checkBordersB(x_ball, y_ball, x_paddle, y_paddle, paddle_width, paddle_height, paddle_side, y_ball_dowm_Edge):
    range_paddle = range(y_paddle, y_paddle + paddle_height)
    if y_ball in range_paddle or y_ball_dowm_Edge in range_paddle:
        if paddle_side == "r":
            if x_ball >= x_paddle - Xdeviation - paddle_width:
                return True
        elif x_ball <= x_paddle + Xdeviation:
            return True


def ball_to_center(i):
    """get: ball place in balls list
    outPut: ball in the middle of the screen"""
    ball_list.sprites()[i].update_loc((gWidth / 2 - ball_list.sprites()[0].get_width() / 2),
                                      (gHeight / 2 - ball_list.sprites()[0].get_height() / 2))


def check_game_over(leftLife, rightLife):
    """get: life left to each side
    outPUt: call game_over_m function with winner name"""
    if leftLife == 0:
        game_over_m('Right' if not against_com else 'computer')
    elif rightLife == 0:
        game_over_m("Left")


def check_quit(status):
    """get: parameter=status for know what act do to by called function
    check: if the user clicks the exit button- exit
     user status + user press- output: action"""
    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if status == 'move':
                    sprite_movement(event)
                if status == 'over':
                    start_game()
                if status == "start":
                    if event.key == pygame.K_c:
                        return True
                    if event.key == pygame.K_f:
                        return False
        if status == 'move':
            if not events and against_com:
                fil = random.randrange(COM_LEVEL)
                if fil == 5:
                    sprite_movement(None)
            ball_move()
            clock.tick(REFRESH)


def show_score():
    score = [*sprite_list.sprites()[0].get_life()]
    font = pygame.font.Font(None, 50)
    text1 = font.render(('life left:     ' + str(+score[0])), 1, BLACK)
    screen.blit(text1, (20, 30))
    text2 = font.render(str(score[1]), 1, BLACK)
    screen.blit(text2, (310, 30))


def game_over_m(winner):
    screen.fill(WHITE)
    captions(40, 'Game over:  ' + winner + '  win', 1, BLACK, 65, 200,False)
    captions(25, 'Press keyBord to reGame', 1, RED, 160, 250,True)
    clock = pygame.time.Clock()
    while True:
        check_quit("over")
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
