import tkinter as tk
from tkinter import messagebox
import random
import os

class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Clone")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Game state
        self.target_word = ""
        self.current_row = 0
        self.current_col = 0
        self.max_attempts = 6
        self.word_length = 5
        self.guesses = []
        
        # Load word list
        self.word_list = self.load_words()
        if not self.word_list:
            messagebox.showerror("Error", "Could not load word list!")
            self.root.destroy()
            return
        
        # Select random word
        self.target_word = random.choice(self.word_list).upper()
        print(f"DEBUG: Target word is {self.target_word}")  # Remove this in production
        
        # Create UI
        self.create_ui()
        
        # Focus on window
        self.root.focus_set()
        
    def load_words(self):
        """Load words from words.txt file"""
        words = []
        word_file = os.path.join(os.path.dirname(__file__), "words.txt")
        
        if os.path.exists(word_file):
            with open(word_file, "r") as f:
                words = [line.strip().upper() for line in f if len(line.strip()) == 5]
        else:
            # Fallback: use a small default word list
            words = [
                "APPLE", "BEACH", "CHAIR", "DANCE", "EARTH", "FLAME", "GLASS", "HEART",
                "IMAGE", "JOKER", "KNIFE", "LEMON", "MUSIC", "NIGHT", "OCEAN", "PIANO",
                "QUART", "RIVER", "SMILE", "TABLE", "UNITY", "VALUE", "WATER", "YOUTH",
                "ZEBRA", "BRAVE", "CLOUD", "DREAM", "EAGLE", "FAITH", "GHOST", "HAPPY",
                "IVORY", "JAZZY", "KNEEL", "LIGHT", "MAGIC", "NOISE", "OPERA", "PEACE",
                "QUICK", "ROBOT", "SPACE", "TRUTH", "ULTRA", "VIVID", "WHEEL", "XENON",
                "YACHT", "ZESTY"
            ]
        
        return words
    
    def create_ui(self):
        """Create the game UI"""
        # Title
        title_label = tk.Label(
            self.root,
            text="WORDLE",
            font=("Arial", 36, "bold"),
            fg="#6AAA64"
        )
        title_label.pack(pady=20)
        
        # Game board frame
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=20)
        
        # Create grid of entry boxes
        self.cells = []
        for row in range(self.max_attempts):
            row_cells = []
            for col in range(self.word_length):
                cell = tk.Label(
                    board_frame,
                    text="",
                    width=3,
                    height=2,
                    font=("Arial", 24, "bold"),
                    bg="#FFFFFF",
                    fg="#000000",
                    relief="solid",
                    borderwidth=2
                )
                cell.grid(row=row, column=col, padx=3, pady=3)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)
        
        # Entry for word input
        self.word_entry = tk.Entry(
            input_frame,
            font=("Arial", 18),
            width=10,
            justify="center",
            state="normal"
        )
        self.word_entry.pack(side=tk.LEFT, padx=10)
        self.word_entry.bind("<Return>", self.submit_guess)
        self.word_entry.bind("<KeyRelease>", self.on_key_release)
        
        # Submit button
        submit_btn = tk.Button(
            input_frame,
            text="Submit",
            font=("Arial", 14),
            command=self.submit_guess,
            bg="#6AAA64",
            fg="white",
            padx=20,
            pady=5
        )
        submit_btn.pack(side=tk.LEFT, padx=10)
        
        # New game button
        new_game_btn = tk.Button(
            self.root,
            text="New Game",
            font=("Arial", 12),
            command=self.new_game,
            bg="#787C7E",
            fg="white",
            padx=15,
            pady=5
        )
        new_game_btn.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Enter a 5-letter word",
            font=("Arial", 12),
            fg="#787C7E"
        )
        self.status_label.pack(pady=10)
        
        # Focus on entry
        self.word_entry.focus_set()
    
    def on_key_release(self, event):
        """Limit input to 5 characters"""
        current_text = self.word_entry.get().upper()
        if len(current_text) > 5:
            self.word_entry.delete(5, tk.END)
        else:
            # Update display
            self.update_current_row_display()
    
    def update_current_row_display(self):
        """Update the visual display of the current row as user types"""
        if self.current_row < self.max_attempts:
            current_text = self.word_entry.get().upper()
            for col in range(self.word_length):
                if col < len(current_text):
                    self.cells[self.current_row][col].config(
                        text=current_text[col],
                        bg="#FFFFFF"
                    )
                else:
                    self.cells[self.current_row][col].config(
                        text="",
                        bg="#FFFFFF"
                    )
    
    def submit_guess(self, event=None):
        """Submit the current guess"""
        guess = self.word_entry.get().strip().upper()
        
        # Validate guess
        if len(guess) != 5:
            self.status_label.config(text="Word must be 5 letters!", fg="#FF0000")
            return
        
        if not guess.isalpha():
            self.status_label.config(text="Word must contain only letters!", fg="#FF0000")
            return
        
        if guess not in self.word_list:
            self.status_label.config(text="Word not in dictionary!", fg="#FF0000")
            return
        
        if guess in self.guesses:
            self.status_label.config(text="You already tried this word!", fg="#FF0000")
            return
        
        # Add to guesses
        self.guesses.append(guess)
        
        # Process the guess
        self.process_guess(guess)
        
        # Clear entry
        self.word_entry.delete(0, tk.END)
        
        # Check win/loss
        if guess == self.target_word:
            self.status_label.config(text="🎉 Congratulations! You won! 🎉", fg="#6AAA64")
            self.word_entry.config(state="disabled")
            return
        
        # Move to next row
        self.current_row += 1
        
        if self.current_row >= self.max_attempts:
            self.status_label.config(
                text=f"Game Over! The word was: {self.target_word}",
                fg="#FF0000"
            )
            self.word_entry.config(state="disabled")
        else:
            self.status_label.config(text="Enter a 5-letter word", fg="#787C7E")
    
    def process_guess(self, guess):
        """Process the guess and color the cells"""
        # Count letters in target word
        target_letters = {}
        for letter in self.target_word:
            target_letters[letter] = target_letters.get(letter, 0) + 1
        
        # First pass: mark correct positions (green)
        result = [None] * self.word_length
        used_positions = set()
        
        for i in range(self.word_length):
            if guess[i] == self.target_word[i]:
                result[i] = "green"
                used_positions.add(i)
                target_letters[guess[i]] -= 1
        
        # Second pass: mark correct letters in wrong positions (yellow)
        for i in range(self.word_length):
            if result[i] is None:
                if guess[i] in target_letters and target_letters[guess[i]] > 0:
                    result[i] = "yellow"
                    target_letters[guess[i]] -= 1
                else:
                    result[i] = "gray"
        
        # Update cell colors
        for col in range(self.word_length):
            cell = self.cells[self.current_row][col]
            cell.config(text=guess[col])
            
            if result[col] == "green":
                cell.config(bg="#6AAA64", fg="#FFFFFF")  # Green
            elif result[col] == "yellow":
                cell.config(bg="#C9B458", fg="#FFFFFF")  # Yellow
            else:
                cell.config(bg="#787C7E", fg="#FFFFFF")  # Gray
    
    def new_game(self):
        """Start a new game"""
        # Reset game state
        self.target_word = random.choice(self.word_list).upper()
        print(f"DEBUG: Target word is {self.target_word}")  # Remove this in production
        self.current_row = 0
        self.current_col = 0
        self.guesses = []
        
        # Clear all cells
        for row in range(self.max_attempts):
            for col in range(self.word_length):
                self.cells[row][col].config(
                    text="",
                    bg="#FFFFFF",
                    fg="#000000"
                )
        
        # Reset UI
        self.word_entry.config(state="normal")
        self.word_entry.delete(0, tk.END)
        self.status_label.config(text="Enter a 5-letter word", fg="#787C7E")
        self.word_entry.focus_set()


def main():
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
