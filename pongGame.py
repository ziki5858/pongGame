import random
import pygame
import BoardManger
from BoardManger import *
from constants import *
import GlobalData

sprite_speed = 25

def main():
    pygame.font.init()
    start_game()

def start_game():
    upload_screen("pong", WHITE, RED)
    upload_sprites()
    check_quit("move")

def againstWho():
    captions(50, 'press c for against com', 1, BLACK, 20, 50, False)
    captions(50, 'press f for friend com', 1, BLACK, 20, 200, True)
    return check_quit('start')

def r_screen(bColor, sColor):
    GlobalData.screen.fill(bColor)
    pygame.draw.line(GlobalData.screen, sColor, (gWidth / 2, 0), (gWidth / 2, gHeight), 2)
    GlobalData.sprite_list.draw(GlobalData.screen)
    GlobalData.ball_list.draw(GlobalData.screen)
    show_score()
    pygame.display.flip()

def captions(font_size, caption, size, color, x, y, flip):
    font = pygame.font.Font(None, font_size)
    text1 = font.render(caption, size, color)
    GlobalData.screen.blit(text1, (x, y))
    if flip:
        pygame.display.flip()

UP_DOWN_LEFT = [pygame.K_s, pygame.K_w]
UP_DOWN_RIGHT = [pygame.K_DOWN, pygame.K_UP]

def get_paddles():
    sprites = GlobalData.sprite_list.sprites()
    return sprites[0], sprites[1]

def get_positions(lSprite, rSprite):
    xL, yL = lSprite.get_pos()
    xR, yR = rSprite.get_pos()
    xB, yB = GlobalData.ball_list.sprites()[0].get_pos()
    return xL, yL, xR, yR, xB, yB

def handle_player_move(event, sprite, x, y, key_map, speed):
    for dir_idx, key in enumerate(key_map):
        if event.key == key:
            new_y = checkBorderS(y, speed[dir_idx], sprite.get_height())
            sprite.update_loc(x, new_y)
            break

def handle_ai_move(rSprite, xR, yR, ball_center, max_step):
    paddle_center = yR + rSprite.get_height() * 0.5
    delta = ball_center - paddle_center
    dead_zone = 10
    if abs(delta) <= dead_zone:
        step = 0
    else:
        step = max(-max_step, min(delta, max_step))
    new_y = checkBorderS(yR, step, rSprite.get_height())
    rSprite.update_loc(xR, new_y)

def sprite_movement(event):
    lSprite, rSprite = get_paddles()
    xL, yL, xR, yR, xB, yB = get_positions(lSprite, rSprite)
    speed = sprite_speed
    ball = GlobalData.ball_list.sprites()[0]
    ball_center = yB + ball.get_height() * 0.5

    if event is not None:
        handle_player_move(event, lSprite, xL, yL, UP_DOWN_LEFT, [speed, -speed])
        if not GlobalData.against_com:
            handle_player_move(event, rSprite, xR, yR, UP_DOWN_RIGHT, [speed, -speed])

    if GlobalData.against_com:
        handle_ai_move(rSprite, xR, yR, ball_center, speed)

def checkBorderS(object_y, move_amount, paddle_height):
    if 0 > object_y + move_amount:
        return 0
    elif object_y + move_amount > gHeight - paddle_height:
        return gHeight - paddle_height
    return object_y + move_amount

def ball_move():
    rList = [abs(BallSpeedPix), -abs(BallSpeedPix)]
    soundList = upload_sound()
    left_paddle, right_paddle = GlobalData.sprite_list.sprites()
    paddle_w = right_paddle.get_width()
    paddle_h = right_paddle.get_height()

    for i, ball in enumerate(GlobalData.ball_list.sprites()):
        check_game_over(*left_paddle.get_life())
        xBall, yBall = ball.get_pos()
        xMove, yMove = ball.get_move()

        paddle_result = handle_paddle_collision(
            ball, left_paddle, right_paddle, xMove,
            paddle_w, paddle_h, soundList[0], rList
        )
        if paddle_result:
            xMove, yMove = paddle_result
        else:
            wall_result = handle_wall_collision(yBall, yMove, ball.get_height())
            if wall_result is not None:
                yMove = wall_result
            else:
                if xBall <= 0 or xBall >= gWidth - ball.get_width():
                    xMove, yMove = handle_side_collision(ball, soundList, i)

        update_and_draw(ball, xMove, yMove)

    r_screen(WHITE, RED)

def update_and_draw(ball, xMove, yMove):
    ball.update_Move(xMove, yMove)
    x, y = ball.get_pos()
    ball.update_loc(x + xMove, y + yMove)

def handle_paddle_collision(ball, left_paddle, right_paddle, xMove, paddle_w, paddle_h, sound_effect, rList):
    xBall, yBall = ball.get_pos()
    for paddle, side in ((right_paddle, 'r'), (left_paddle, 'l')):
        if check_borders_ball(
            xBall, yBall, *paddle.get_pos(), paddle_w,
            paddle_h, side, yBall + ball.get_height()
        ):
            sound(sound_effect)
            direction = -1 if side == 'r' else 1
            new_x = direction * abs(xMove) + direction * AddSpeedBall
            new_y = random.choice(rList)
            return new_x, new_y
    return None

def handle_wall_collision(yBall, yMove, ball_height):
    if yBall <= 0:
        return abs(yMove)
    if yBall >= gHeight - ball_height:
        return -abs(yMove)
    return None

def handle_side_collision(ball, soundList, index):
    edgePoint(soundList, index)
    xBall, _ = ball.get_pos()
    if xBall <= 0:
        return BallSpeedPix, -BallSpeedPix
    return -BallSpeedPix, BallSpeedPix

def edgePoint(soundList, i):
    sound(soundList[1])
    ball_to_center(i)
    GlobalData.sprite_list.sprites()[0].update_right_Life()

def ball_to_center(i):
    GlobalData.ball_list.sprites()[i].update_loc(
        (gWidth / 2 - GlobalData.ball_list.sprites()[0].get_width() / 2),
        (gHeight / 2 - GlobalData.ball_list.sprites()[0].get_height() / 2)
    )

def check_borders_ball(x_ball, y_ball, x_paddle, y_paddle, paddle_width, paddle_height, paddle_side, y_ball_bottom):
    if y_ball_bottom < y_paddle or y_ball > y_paddle + paddle_height:
        return False
    if paddle_side == 'r':
        return x_ball >= x_paddle - Xdeviation - paddle_width
    else:
        return x_ball <= x_paddle + Xdeviation

def check_game_over(leftLife, rightLife):
    if leftLife == 0:
        game_over_m('Right' if not GlobalData.against_com else 'computer')
    elif rightLife == 0:
        game_over_m("Left")

def show_score():
    score = [*GlobalData.sprite_list.sprites()[0].get_life()]
    font = pygame.font.Font(None, 50)
    text1 = font.render(('life left:     ' + str(+score[0])), 1, BLACK)
    GlobalData.screen.blit(text1, (20, 30))
    text2 = font.render(str(score[1]), 1, BLACK)
    GlobalData.screen.blit(text2, (310, 30))

def game_over_m(winner):
    GlobalData.screen.fill(WHITE)
    captions(40, 'Game over:  ' + winner + '  win', 1, BLACK, 65, 200, False)
    captions(25, 'Press keyBord to reGame', 1, RED, 160, 250, True)
    clock = pygame.time.Clock()
    while True:
        check_quit("over")
        clock.tick(REFRESH)

def check_quit(status):
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
            if not events and GlobalData.against_com:
                if random.randrange(COM_LEVEL) == 5:
                    sprite_movement(None)
            ball_move()
            clock.tick(REFRESH)

def sound(soundNumber):
    channel = pygame.mixer.find_channel()
    if channel is not None:
        channel.queue(soundNumber)

def upload_sound():
    pygame.mixer.init(frequency=22050, size=-16, channels=4)
    return [
        pygame.mixer.Sound('Swipe Swoosh Transition Sound Effect.mp3'),
        pygame.mixer.Sound('Video Game Beep - Sound Effect.mp3')
    ]

if __name__ == "__main__":
    main()
