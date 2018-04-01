import pygame
'''
This is a prototype of breakout
'''

screen_dim = 640, 480

#objects
Brickw = 60
Brickh = 15
paddlew = 60
paddleh = 12
ball_diameter = 18
ball_radius = ball_diameter/2

paddle_max= screen_dim[0] - paddlew
ball_maxx, ball_maxy = screen_dim[0] - ball_diameter, screen_dim[1] - ball_diameter

paddle_y = screen_dim[1] - paddleh - 10

#colors
black = (0,0,0)
white = (255,255,255)
blue  = (0,0,255)
green = (0, 200, 15)
brick_col = (200,200,0)

# phases
ball_in_paddle = 0
Game_on = 1
Game_win = 2
Game_over = 3

#Game (main program)
class Brickgame:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(screen_dim)
        pygame.display.set_caption("Breakout game")
        self.clock = pygame.time.Clock()
        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

        self.init_game()

    #support functions

    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = ball_in_paddle

        self.paddle = pygame.Rect(300, paddle_y, paddlew, paddleh)
        self.ball = pygame.Rect(300, paddle_y - ball_diameter, ball_diameter, ball_diameter)
        self.ball_vel = [5,-5]
 
        self.create_bricks()
    def create_bricks(self):
        y_ofs = 35
        self.bricks = []
        for i in range(7):
            x_ofs = 35
            for j in range(8):
                self.bricks.append(pygame.Rect(x_ofs,y_ofs,Brickw,Brickh))
            x_ofs += Brickw + 10
        y_ofs += Brickh + 5

    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.left -= 5
            if self.paddle.left < 0:
                self.paddle.left = 0
 
        if keys[pygame.K_RIGHT]:
            self.paddle.left += 5
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X
 
        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = [5,-5]
            self.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            self.init_game()
    
