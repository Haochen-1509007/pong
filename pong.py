from uagame import Window
import pygame, time, random
from pygame.locals import *

# User-defined functions
def main():
   window_wide=500
   window_height=400
   window = Window('Pong', window_wide, window_height)
   window.set_auto_update(False)
   game = Game(window)
   game.play()
   window.close()

class Ball:
   # An object in this class represents a colored circle.

   def __init__(self, center, radius, color, window, velocity,paddle1,paddle2):
      # Initialize a Cirlcle.
      # - self is the Circle to initialize
      # - center is a list containing the x and y int
      # coords of the center of the Circle
      # - radius is the int pixel radius of the Circle
      # - color is the pygame.Color of the Circle
      # - window is the uagame window object

      self.center = center
      self.radius = radius
      self.color = color
      self.window = window
      self.window_height=500
      self.window_wide=500
      self.velocity = velocity
      self.randomize_center()
      self.paddle1=paddle1
      self.paddle2=paddle2
      
   def randomize_center(self):
         # Give the dot a new random center location such that the dot
         # fully appears on the screen
         # - self is the dot object to move
         screen_dimension = self.window.get_surface().get_size()     
         for number in range(len(self.center)):
            self.center[number] = random.randint(self.radius , screen_dimension[number] - self.radius)
            
   def draw(self):
      # Draw the Circle.
      # - self is the Circle to draw
      pygame.draw.circle(self.window.get_surface(), self.color, self.center, self.radius )

   def move(self):
      # Move the circle.
      # - self is the Circle to move
      
      window_size = (self.window.get_width(), self.window.get_height())
      size = self.window.get_surface().get_size()
        
      for index in range(len(size)):
         self.center[index] = self.center[index] + self.velocity[index]         
         if self.center[index] - self.radius <= 0 or self.center[index] + self. radius >= size[index]:
            # bounce the ball
            self.velocity[index] = -1* self.velocity[index]
      if self.velocity[0]<0 and self.paddle1.collidepoint(self.center[0], self.center[1]):
         self.velocity[0]=-1*self.velocity[0]
      if self.velocity[0]>0 and self.paddle2.collidepoint(self.center[0], self.center[1]):
         self.velocity[0]=-1*self.velocity[0]
         
   def get_color(self):
      # Return the color of the Circle.
      # - self is the Circle
      
      return self.color
   
class Game:
   # An object in this class represents a complete game.

   def __init__(self, window):
      # Initialize a Game.
      # - self is the Game to initialize
      # - window is the uagame window object
      
      self.window_height=500
      self.window_wide=500     
      self.window = window
      self.color=pygame.Color('white')
      self.pause_time = 0.04 # smaller is faster game
      self.close_clicked = False
      self.continue_game = True
      self.paddle1=pygame.Rect(100,180,10,50)
      self.paddle2=pygame.Rect(400,180,10,50)            
      self.ball = Ball([int(self.window_wide/2), int(self.window_height/2)], 5, self.color, window,[15,10],self.paddle1,self.paddle2)
      self.score=[0,0]
      pygame.key.set_repeat(20, 20)
           
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
          # play frame
         self.handle_event()
                     
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.draw()
         time.sleep(self.pause_time) # set game velocity by pausing

   def handle_event(self):
      # Handle each user event by changing the game state
      # appropriately.
      # - self is the Game whose events will be handled

      event = pygame.event.poll()    
      list_of_keys = pygame.key.get_pressed()
      
      if event.type == QUIT:
         self.close_clicked = True
      if event.type == KEYDOWN and self.continue_game:
         self.handle_key(event)
            
   def handle_key(self, event):
      event = pygame.event.poll()    
      list_of_keys = pygame.key.get_pressed()      
      if list_of_keys[K_q]:
         self.paddle_up(self.paddle1)
         
      if list_of_keys[K_a]:
         self.paddle_down(self.paddle1)
         
      if list_of_keys[K_i]:
         self.paddle_up(self.paddle2)
            
      if list_of_keys[K_k]:
         self.paddle_down(self.paddle2)

   
   def paddle_up(self,paddle):
      
      if(paddle.top > 0):
         
         paddle.move_ip(0, -10);

      if paddle.top < 0:
         paddle.top = 0
      return paddle
         
   def paddle_down(self,paddle):
      paddle.bottom = paddle.bottom + 10
      if paddle.bottom > 400:
         paddle.bottom = 400
         
   def draw(self):
         # Draw all game objects.
         # - self is the Game to draw
         self.window.clear()
         self.ball.draw()
         self.score_draw()
         #self.color=pygame.Color('white')
         #paddle1=pygame.Rect(self.window_wide/10,self.window_height/2-self.window_height/20,self.window_wide/100,self.window_height/8)
         pygame.draw.rect(self.window.get_surface(), self.color, self.paddle1)
         #paddle2=pygame.Rect(self.window_wide*9/10,self.window_height/2-self.window_height/20,self.window_wide/100,self.window_height/8)
         pygame.draw.rect(self.window.get_surface(), self.color, self.paddle2)      
         if not self.continue_game:
            # Perform appropriate game over actions
            self.fg_color_str='black'
            self.window.set_bg_color(self.fg_color_str)
            #self.window.clear()
         self.window.update()

   def update(self):
      # Update the game objects.
      # - self is the Game to update
      size=self.window.get_surface().get_size()
      self.ball.move()
      if self.ball.center[0] <= self.ball.radius:
         self.score[1] += 1
      if self.ball.center[0]+self.ball.radius>=size[0]:
         self.score[0] += 1
      
   def score_draw(self):
      score_string1 = str(self.score[0])
      score_string2 = str(self.score[1])
      fg_color = 'white'
      font_size = 60
      size=self.window.get_surface().get_size()
      self.window.set_font_color(fg_color)
      self.window.set_font_size(font_size)
      self.window.draw_string(score_string1,0,0)
      self.window.draw_string(score_string2,size[0]-font_size,0)
         
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      if self.score[0] > 10 or self.score[1] > 10:
         self.continue_game = False
         


main()
