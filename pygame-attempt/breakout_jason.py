import pygame
import sys
'''
This is a prototype of breakout
'''

screen_dim = 640, 480

#objects
Brickw = 110
Brickh = 30
paddlew = 120
paddleh = 24
ball_diameter = 24
ball_radius = ball_diameter/2

paddle_max= screen_dim[0] - paddlew
ball_maxx, ball_maxy = screen_dim[0] - ball_diameter, screen_dim[1] - ball_diameter

paddle_y = screen_dim[1] - paddleh - 10

#colors
black = (30,144,255)
white = (255,255,255)
blue  = (0,0,255)
green = (0, 200, 15)
brick_col = (255,215,0)

# phases
ball_in_paddle = 0
Game_on = 1
Game_win = 2
Game_over = 3

# Sprites
class paddle_image(pygame.sprite.Sprite):
    '''
    This class will represent the panels
    '''
    def __init__(self, width, height, image):
        #call parent function
        super().__init__()
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        
        
class paddle(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        self.image = pygame.Surface([height, width])
        self.image.fill(white)
        self.image.set_colorkey(white)

        pygame.draw.rect(self.image, color, [0,0, width, height])
        self.rect = self.image.get_rect()
        

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
        #self.paddle = paddle(blue, paddleh, paddlew)
        self.ball = pygame.Rect(300, paddle_y - ball_diameter, ball_diameter, ball_diameter)
        self.ball_vel = [15,-15]
 
        self.create_bricks()
    def create_bricks(self):
        y_ofs = 35
        self.bricks = []
        for i in range(3):
            x_ofs = 25
            for j in range(5):
                self.bricks.append(pygame.Rect(x_ofs,y_ofs,Brickw,Brickh))
                x_ofs += Brickw + 10
            y_ofs += Brickh + 5
    def draw_bricks(self):

        for brick in self.bricks:
            pygame.draw.rect(self.screen, brick_col, brick)
    
    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.left -= 15
            if self.paddle.left < 0:
                self.paddle.left = 0
 
        if keys[pygame.K_RIGHT]:
            self.paddle.left += 15
            if self.paddle.left > paddle_max:
                self.paddle.left = paddle_max
 
        if keys[pygame.K_SPACE] and self.state == ball_in_paddle:
            self.ball_vel = [15,-15]
            self.state = Game_on
        elif keys[pygame.K_RETURN] and (self.state == Game_over or self.state == Game_win):
            self.init_game()
    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top += self.ball_vel[1]
        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= ball_maxx:
            self.ball.left = ball_maxx
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top <= 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
    def handle_collision(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) <= 0:
            self.state = Game_win

        if self.ball.colliderect(self.paddle):
            self.ball.top = paddle_y - ball_diameter
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            print("Hi")
            if self.lives > 0:
                self.state = ball_in_paddle
            else:
                self.state = Game_over
    def show_stats(self):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, white)
            self.screen.blit(font_surface, (205,5))

    def show_message(self, message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, white)
            x = (screen_dim[0] - size[0])/2
            y = (screen_dim[1] - size[1])/2
            self.screen.blit(font_surface, (x,y))

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit

            self.clock.tick(50)
            self.screen.fill(black)
            self.check_input()

            if self.state == Game_on:
                self.move_ball()
                self.handle_collision()
            elif self.state == ball_in_paddle:
                self.ball.left = self.paddle.left + self.paddle.width/2
                self.ball.top = self.paddle.top - self.ball.height
                self.show_message("Launch the ball!")

            elif self.state == Game_over:
                self.show_message("GG buddy")
            elif self.state == Game_win:
                self.show_message("Congrats")
            self.draw_bricks()

            pygame.draw.rect(self.screen, blue, self.paddle)
            self.screen.blit(pygame.image.load("pancake.jpg"), self.paddle)
            pygame.draw.circle(self.screen, white, (int(self.ball.left + ball_radius), int(self.ball.top + ball_radius)), int(ball_radius))

            self.show_stats()

            pygame.display.flip()
    
if __name__ == "__main__":
    Brickgame().run()           
            
            
                
            
    
