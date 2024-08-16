import tkinter as tk
import random

# Constants
ROWS = 25
COLS = 25
TITLE_SIZE = 25
WINDOW_WIDTH = TITLE_SIZE * COLS
WINDOW_HEIGHT = TITLE_SIZE * ROWS
MOVE_DELAY = 100  # milliseconds

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(master, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
        self.canvas.pack()

        # Center the window
        self.master.update_idletasks()
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

        # Initialize game variables
        self.direction = 'right'
        self.snake_body = [(5 * TITLE_SIZE, 5 * TITLE_SIZE)]
        self.food_x, self.food_y = self.generate_food()
        self.score = 0

        # Bind keyboard events
        self.master.bind("<Up>", lambda e: self.change_direction('up'))
        self.master.bind("<Down>", lambda e: self.change_direction('down'))
        self.master.bind("<Left>", lambda e: self.change_direction('left'))
        self.master.bind("<Right>", lambda e: self.change_direction('right'))

        # Start the game loop
        self.move_snake()

    def draw_tile(self, x, y, color):
        self.canvas.create_rectangle(x, y, x + TITLE_SIZE, y + TITLE_SIZE, fill=color, outline='')

    def clear_tile(self, x, y):
        self.canvas.create_rectangle(x, y, x + TITLE_SIZE, y + TITLE_SIZE, fill="black", outline='')

    def generate_food(self):
        while True:
            fx = random.randint(0, COLS - 1) * TITLE_SIZE
            fy = random.randint(0, ROWS - 1) * TITLE_SIZE
            if (fx, fy) not in self.snake_body:
                return fx, fy

    def move_snake(self):
        head_x, head_y = self.snake_body[0]

        # Update head position based on direction
        if self.direction == 'up':
            head_y -= TITLE_SIZE
        elif self.direction == 'down':
            head_y += TITLE_SIZE
        elif self.direction == 'left':
            head_x -= TITLE_SIZE
        elif self.direction == 'right':
            head_x += TITLE_SIZE

        # Check for collisions with walls or self
        if (head_x < 0 or head_x >= WINDOW_WIDTH or
            head_y < 0 or head_y >= WINDOW_HEIGHT or
            (head_x, head_y) in self.snake_body):
            self.game_over()
            return

        # Move snake body
        new_head = (head_x, head_y)
        self.snake_body = [new_head] + self.snake_body[:-1]

        # Check for food collision
        if (head_x, head_y) == (self.food_x, self.food_y):
            self.snake_body.append(self.snake_body[-1])  # Grow the snake
            self.food_x, self.food_y = self.generate_food()  # Generate new food
            self.score += 1

        # Redraw the snake and food
        self.redraw()

        # Schedule the next move
        self.master.after(MOVE_DELAY, self.move_snake)

    def game_over(self):
        self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="Game Over", fill="red", font=("Arial", 30))
        self.master.after_cancel(self.move_snake)

    def redraw(self):
        self.canvas.delete("snake")
        self.canvas.delete("food")

        # Draw snake
        for x, y in self.snake_body:
            self.draw_tile(x, y, "lime green")

        # Draw food
        self.draw_tile(self.food_x, self.food_y, "red")

    def change_direction(self, new_direction):
        if (new_direction == 'up' and self.direction != 'down') or \
           (new_direction == 'down' and self.direction != 'up') or \
           (new_direction == 'left' and self.direction != 'right') or \
           (new_direction == 'right' and self.direction != 'left'):
            self.direction = new_direction

# Initialize Tkinter window and start the game
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
