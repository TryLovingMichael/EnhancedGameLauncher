import os
import tkinter as tk
from tkinter import ttk, messagebox

class GameLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")  # Light background for the root window
        self.games = {}  # Store games by company
        self.buttons = {}  # Store buttons for each company
        self.filtered_words = []  # Initialize filtered words here

        self.load_games()

    def load_games(self):
        # Directories to search for games
        directories = {
            'Steam': r'C:\Program Files (x86)\Steam\steamapps\common',
            'Epic Games': r'C:\Program Files\Epic Games',
            'GOG': r'C:\Program Files (x86)\GOG Galaxy\Games',
            'Ubisoft': r'C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games',
        }

        # Loop over each directory and look for game executables
        for company, directory in directories.items():
            games_list = self.find_games(directory)
            if games_list:
                self.games[company] = games_list
                self.create_company_button(company)

    def find_games(self, directory):
        """Search for .exe files in the specified directory and return game names without .exe"""
        games = []
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".exe"):  # Find all .exe files
                        game_name = file[:-4]  # Remove the .exe extension
                        if not self.is_filtered(game_name):  # Check if the game is filtered
                            games.append(game_name)  # Add the game name
        return games

    def create_company_button(self, company):
        """Create a button for each company with styling"""
        button = ttk.Button(self.root, text=company, style="Company.TButton", command=lambda c=company: self.show_games(c))
        button.pack(pady=10, fill="x", padx=50)
        self.buttons[company] = button

    def show_games(self, company):
        """Display the games of the selected company in a new window with scroll functionality"""
        if company not in self.games:
            messagebox.showerror("Error", f"No games found for {company}")
            return

        games_window = tk.Toplevel(self.root)
        games_window.title(f"{company} Games")
        games_window.geometry("600x400")

        # Create a canvas to make the games window scrollable
        canvas = tk.Canvas(games_window)
        scrollbar = ttk.Scrollbar(games_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame to hold the game buttons
        buttons_frame = ttk.Frame(canvas)

        # Add the buttons for each game in the company
        games_list = self.games[company]
        for game in games_list:
            game_button = ttk.Button(buttons_frame, text=game, style="Game.TButton", command=lambda g=game: self.launch_game(g))
            game_button.pack(pady=5, fill="x", padx=20)

        # Add the scrollbar to the canvas and display the frame inside the canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=buttons_frame, anchor="nw")

        # Update the scrollable region
        buttons_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Bind the mouse wheel to the canvas for scrolling
        games_window.bind("<MouseWheel>", lambda event, canvas=canvas: self.on_mouse_wheel(event, canvas))

    def on_mouse_wheel(self, event, canvas):
        """Handle mouse wheel scrolling"""
        if event.delta > 0:
            canvas.yview_scroll(-1, "units")  # Scroll up
        else:
            canvas.yview_scroll(1, "units")  # Scroll down

    def launch_game(self, game_name):
        """Launch the game based on its name (filtered name without path)"""
        # Find the full path of the game from the name
        for company, games_list in self.games.items():
            for game in games_list:
                if game == game_name:  # Match the game name
                    game_path = os.path.join(self.get_directory_by_company(company), game_name + ".exe")
                    try:
                        os.startfile(game_path)  # Launch the game
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to launch game: {e}")
                    return

    def get_directory_by_company(self, company):
        """Return the directory path for the given company"""
        directories = {
            'Steam': r'C:\Program Files (x86)\Steam\steamapps\common',
            'Epic Games': r'C:\Program Files\Epic Games',
            'GOG': r'C:\Program Files (x86)\GOG Galaxy\Games',
            'Ubisoft': r'C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games',
        }
        return directories.get(company, "")

    def is_filtered(self, game_name):
        """Check if the game name contains any of the filtered words"""
        for word in self.filtered_words:
            if word.lower() in game_name.lower():  # Case-insensitive matching
                return True
        return False

    def add_filter(self, filter_word):
        """Add a word to the filter list"""
        self.filtered_words.append(filter_word.lower())  # Store the filter word in lowercase

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncherApp(root)

    # Add filters to exclude certain games (e.g., games containing "ndp")
    app.add_filter("ndp")

    # Configure the style for buttons
    style = ttk.Style()
    style.configure("Company.TButton", font=("Arial", 14), padding=10, relief="flat", background="#4CAF50", foreground="white")
    style.configure("Game.TButton", font=("Arial", 12), padding=8, relief="flat", background="#2196F3", foreground="white")
    style.map("Company.TButton", background=[('active', '#45a049')], foreground=[('active', 'black')])
    style.map("Game.TButton", background=[('active', '#1E88E5')], foreground=[('active', 'black')])

    root.mainloop()
