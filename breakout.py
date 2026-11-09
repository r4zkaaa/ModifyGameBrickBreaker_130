import threading
import tkinter as tk

try:
  import winsound

  def play_sound(freq=800, duration=40):
    threading.Thread(
        target=winsound.Beep, args=(freq, duration), daemon=True
    ).start()

except ImportError:
  def play_sound(freq=800, duration=40):
    pass


class GameObject(object):

  def __init__(self, canvas, item):
    self.canvas = canvas
    self.item = item

  def get_position(self):
    return self.canvas.bbox(self.item)

  def move(self, x, y):
    self.canvas.move(self.item, x, y)

  def delete(self):
    self.canvas.delete(self.item)


class Ball(GameObject):

  def __init__(self, canvas, x, y):
    self.radius = 12
    self.direction = [1, -1]  
    self.speed = 4

    sword_points = [
        x,
        y - 18,  
        x + 4,
        y - 12,  
        x + 3,
        y + 2,  
        x + 10,
        y + 2, 
        x + 10,
        y + 6,  
        x + 3,
        y + 6,  
        x + 4,
        y + 16,  
        x,
        y + 18, 
        x - 4,
        y + 16,  
        x - 3,
        y + 6,  
        x - 10,
        y + 6,  
        x - 10,
        y + 2,  
        x - 3,
        y + 2,  
        x - 4,
        y - 12,  
    ]

    item = canvas.create_polygon(
        sword_points,
        fill="#e0e0e0",  
        outline="#ffd700",  
        width=1,
    )
    super(Ball, self).__init__(canvas, item)

  def update(self):
    coords = self.get_position()
    if not coords:
      return
    width = self.canvas.winfo_width()
    if coords[0] <= 0 or coords[2] >= width:
      self.direction[0] *= -1
      play_sound(400, 30)  
    if coords[1] <= 0:
      self.direction[1] = 1  
      play_sound(400, 30)
    x = self.direction[0] * self.speed
    y = self.direction[1] * self.speed
    self.move(x, y)

  def collide(self, game_objects):
    coords = self.get_position()
    if not coords:
      return
    x = (coords[0] + coords[2]) * 0.5

    for game_object in game_objects:
      if isinstance(game_object, Paddle):
        self.direction[1] = -1  
        self.speed += 0.2
        play_sound(600, 40)
      elif isinstance(game_object, Brick):
        obj_coords = game_object.get_position()
        if obj_coords:
          if x > obj_coords[2]:
            self.direction[0] = 1
          elif x < obj_coords[0]:
            self.direction[0] = -1
          else:
            self.direction[1] *= -1
        game_object.hit()


class Paddle(GameObject):

  def __init__(self, canvas, x, y):
    self.width = 100
    self.height = 16
    self.ball = None

    half_w = self.width / 2
    half_h = self.height / 2

    
    sheath_points = [
        x - half_w,
        y - half_h,  
        x + half_w,
        y - half_h,  
        x + half_w - 6,
        y + half_h,  
        x - half_w + 6,
        y + half_h,  
    ]

    item = canvas.create_polygon(
        sheath_points,
        fill="#4a2511",  
        outline="#ffd700",  
        width=2,
    )
    super(Paddle, self).__init__(canvas, item)

  def set_ball(self, ball):
    self.ball = ball

  def move_to(self, target_x):
   
    coords = self.get_position()
    if not coords:
      return
    current_x = (coords[0] + coords[2]) / 2
    width = self.canvas.winfo_width() or 610
    half_w = self.width / 2

    target_x = max(half_w, min(width - half_w, target_x))
    offset = target_x - current_x

    super(Paddle, self).move(offset, 0)
    if self.ball is not None:
      self.ball.move(offset, 0)


class Brick(GameObject):
  COLORS = {1: "#ff5555", 2: "#ffb86c", 3: "#8be9fd"}

  def __init__(self, canvas, x, y, hits):
    self.width = 75
    self.height = 18
    self.hits = hits
    color = Brick.COLORS[hits]
    item = canvas.create_rectangle(
        x - self.width / 2,
        y - self.height / 2,
        x + self.width / 2,
        y + self.height / 2,
        fill=color,
        outline="black",
        width=2,
        tags="brick",
    )
    super(Brick, self).__init__(canvas, item)

  def hit(self):
    play_sound(900 + (3 - self.hits) * 200, 40)
    self.hits -= 1
    if self.hits == 0:
      self.delete()
    else:
      self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])


class Game(tk.Frame):

  def __init__(self, master):
    super(Game, self).__init__(master)
    self.lives = 3
    self.width = 610
    self.height = 400

    self.canvas = tk.Canvas(
        self, bg="black", width=self.width, height=self.height
    )
    self.canvas.pack()
    self.pack()

    self.items = {}
    self.ball = None
    self.paddle = Paddle(self.canvas, self.width / 2, 350)
    self.items[self.paddle.item] = self.paddle

    self.create_bricks()

    self.hud = None
    self.setup_game()
    self.canvas.focus_set()

    self.canvas.bind("<Motion>", lambda e: self.paddle.move_to(e.x))

  def create_bricks(self):
    for x in range(5, self.width - 5, 75):
      self.add_brick(x + 37.5, 40, 3)
      self.add_brick(x + 37.5, 60, 2)
      self.add_brick(x + 37.5, 80, 1)
      self.add_brick(x + 37.5, 100, 1)

  def setup_game(self):
    self.add_ball()
    self.update_lives_text()
    self.text = self.draw_text(300, 200, "Press Space to start")
    self.canvas.bind("<space>", lambda _: self.start_game())
    self.canvas.bind("<r>", lambda _: self.restart_game())

  def restart_game(self):
    self.lives = 3
    self.canvas.delete("all")
    self.items = {}
    self.hud = None
    self.ball = None

    self.paddle = Paddle(self.canvas, self.width / 2, 350)
    self.items[self.paddle.item] = self.paddle
    self.create_bricks()
    self.setup_game()

  def add_ball(self):
    if self.ball is not None:
      self.ball.delete()
    paddle_coords = self.paddle.get_position()
    x = (paddle_coords[0] + paddle_coords[2]) * 0.5
    
    self.ball = Ball(self.canvas, x, 315)
    self.paddle.set_ball(self.ball)

  def add_brick(self, x, y, hits):
    brick = Brick(self.canvas, x, y, hits)
    self.items[brick.item] = brick

  def draw_text(self, x, y, text, size="40"):
    font = ("Forte", size)
    return self.canvas.create_text(x, y, text=text, font=font, fill="#f8f8f2")

  def update_lives_text(self):
    text = "Lives: %s" % self.lives
    if self.hud is None:
      self.hud = self.draw_text(60, 20, text, 15)
    else:
      self.canvas.itemconfig(self.hud, text=text)

  def start_game(self):
    self.canvas.unbind("<space>")
    self.canvas.delete(self.text)
    self.paddle.ball = None
    self.game_loop()

  def game_loop(self):
    self.check_collisions()
    num_bricks = len(self.canvas.find_withtag("brick"))
    if num_bricks == 0:
      self.ball.speed = None
      self.draw_text(300, 200, "You win!")
      play_sound(1200, 200)
    elif self.ball.get_position()[3] >= self.height:
      self.ball.speed = None
      self.lives -= 1
      play_sound(250, 150)
      if self.lives < 0:
        self.draw_text(300, 200, "Game Over! Press R to Restart", 24)
      else:
        self.after(1000, self.setup_game)
    else:
      self.ball.update()
      self.after(16, self.game_loop)

  def check_collisions(self):
    ball_coords = self.ball.get_position()
    if not ball_coords:
      return
    items = self.canvas.find_overlapping(*ball_coords)
    objects = [self.items[x] for x in items if x in self.items]
    self.ball.collide(objects)


if __name__ == "__main__":
  root = tk.Tk()
  root.title("Breakout Sword Edition")
  game = Game(root)
  game.mainloop()