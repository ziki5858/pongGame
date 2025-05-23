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
    """Create and position player paddles and balls on the board."""
    global sprite_list, ball_list

    # Initialize sprite groups
    sprite_list = pygame.sprite.Group()
    ball_list = pygame.sprite.Group()

    # Create left paddle and determine its width
    left_paddle = Player(0, gHeight / 2)
    paddle_width = left_paddle.get_width()
    # Create right paddle at the opposite edge
    right_paddle = Player(gWidth - paddle_width, gHeight / 2)
    sprite_list.add(left_paddle, right_paddle)

    # Create balls centered on the screen
    for _ in range(BALL_AMOUNT):
        ball_list.add(Ball(gWidth / 2, gHeight / 2))

    # Draw and update display
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

def handle_ai_move(rSprite, xR, yR, ball_center, max_step):
    """Move paddle toward ball center with capped speed and dead zone."""
    # Compute paddle center
    paddle_center = yR + rSprite.get_height() * 0.5

    # Compute difference
    delta = ball_center - paddle_center

    # Dead zone: no movement if very close
    dead_zone = 10
    if abs(delta) <= dead_zone:
        step = 0
    else:
        # Cap movement per frame
        step = max(-max_step, min(delta, max_step))

    # Clamp within screen
    new_y = checkBorderS(yR, step, rSprite.get_height())
    rSprite.update_loc(xR, new_y)

def sprite_movement(event):
    lSprite, rSprite = get_paddles()
    xL, yL, xR, yR, xB, yB = get_positions(lSprite, rSprite)
    speed = sprite_speed  # single value now

    # Compute ball center once
    ball = ball_list.sprites()[0]
    ball_center = yB + ball.get_height() * 0.5

    if event is not None:
        handle_player_move(event, lSprite, xL, yL, UP_DOWN_LEFT, [speed, -speed])
        if not against_com:
            handle_player_move(event, rSprite, xR, yR, UP_DOWN_RIGHT, [speed, -speed])

    if against_com:
        handle_ai_move(rSprite, xR, yR, ball_center, speed)


def checkBorderS(object_y, move_amount, paddle_height):
    if 0 > object_y + move_amount:
        return 0
    elif object_y + move_amount > gHeight - paddle_height:
        return gHeight - paddle_height
    return object_y + move_amount


import random

def handle_paddle_collision(
    ball,
    left_paddle,
    right_paddle,
    xMove,
    paddle_w,
    paddle_h,
    sound_effect,
    rList
):
    """Return new (xMove, yMove) if ball collides with either paddle, else None."""
    xBall, yBall = ball.get_pos()
    # Iterate over paddles to remove duplication
    for paddle, side in ((right_paddle, 'r'), (left_paddle, 'l')):
        if check_borders_ball(
            xBall, yBall,
            *paddle.get_pos(),
            paddle_w,
            paddle_h,
            side,
            yBall + ball.get_height()
        ):
            sound(sound_effect)
            # Determine bounce direction: -1 for right paddle, +1 for left
            direction = -1 if side == 'r' else 1
            new_x = direction * abs(xMove) + direction * AddSpeedBall
            new_y = random.choice(rList)
            return new_x, new_y
    return None


def handle_wall_collision(yBall, yMove, ball_height):
    """Return new yMove if ball collides with top/bottom walls, else None."""
    # Top wall collision
    if yBall <= 0:
        return abs(yMove)
    # Bottom wall collision
    if yBall >= gHeight - ball_height:
        return -abs(yMove)
    return None


def handle_side_collision(ball, soundList, index):
    """Handle scoring when ball hits left/right edge and return reset velocities."""
    edgePoint(soundList, index)             # play scoring sound and update score
    xBall, _ = ball.get_pos()
    # If ball went out on left, send right; else send left
    if xBall <= 0:
        return BallSpeedPix, -BallSpeedPix
    return -BallSpeedPix, BallSpeedPix


def update_and_draw(ball, xMove, yMove):
    """Apply movement deltas and update ball position on screen."""
    ball.update_Move(xMove, yMove)          # update ball's dx, dy
    x, y = ball.get_pos()
    ball.update_loc(x + xMove, y + yMove)   # move ball to new position


def ball_move():
    """Move balls and handle all collisions without code duplication."""
    # Precompute vertical speed options
    rList = [abs(BallSpeedPix), -abs(BallSpeedPix)]
    soundList = upload_sound()

    # Get paddles and their dimensions
    left_paddle, right_paddle = sprite_list.sprites()
    paddle_w = right_paddle.get_width()
    paddle_h = right_paddle.get_height()

    for i, ball in enumerate(ball_list.sprites()):
        # Check game over condition each frame
        check_game_over(*left_paddle.get_life())

        # Current position and movement
        xBall, yBall = ball.get_pos()
        xMove, yMove = ball.get_move()

        # 1. Paddle collisions
        paddle_result = handle_paddle_collision(
            ball, left_paddle, right_paddle, xMove,
            paddle_w, paddle_h, soundList[0], rList
        )
        if paddle_result:
            xMove, yMove = paddle_result
        else:
            # 2. Wall collisions (top/bottom)
            wall_result = handle_wall_collision(yBall, yMove, ball.get_height())
            if wall_result is not None:
                yMove = wall_result
            else:
                # 3. Side collisions (scoring)
                if xBall <= 0 or xBall >= gWidth - ball.get_width():
                    xMove, yMove = handle_side_collision(ball, soundList, i)

        # Apply movement and redraw ball
        update_and_draw(ball, xMove, yMove)

    # Refresh the screen once after moving all balls
    r_screen(WHITE, RED)

def edgePoint(soundList, i):
    sound(soundList[1])
    ball_to_center(i)
    sprite_list.sprites()[0].update_right_Life()


def check_borders_ball(
    x_ball, y_ball, x_paddle, y_paddle,
    paddle_width, paddle_height, paddle_side,
    y_ball_bottom
) -> bool:
    """ return True if ball overlaps paddle. """

    # vertical overlap check
    if y_ball_bottom < y_paddle or y_ball > y_paddle + paddle_height:
        return False

    # check with tolerance
    if paddle_side == 'r':
        return x_ball >= x_paddle - Xdeviation - paddle_width
    else:
        return x_ball <= x_paddle + Xdeviation

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
