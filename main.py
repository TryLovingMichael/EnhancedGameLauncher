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
        self.filtered_words = ['ndp', 'test', 'sql', 'uac', 'crashreport', 'ue4', 'eac', 'ue5', 
                               'unitycrash', 'easyanti', 'helper', 'ffmpeg', 'yt-dlp', 
                               'jab', 'jaccess', 'java' 'jfr', 'jrun', 'keytool', 'kinit', 'klist',
                               'ktab', 'rmi', 'rmiregistry', 'window3d', 'compiler', 'atg', 'dotNet',
                               'oalinst', 'vcredist', 'vc_redist', 'VC_redist', 'openssl', 'installer',
                               'launcher', 'diagnostic', 'apputil', 'microsoft', 'winr', 'ui32', 'ui64',
                               'steamredown', 'wallpaperservice', 'webwallpaper', 'applicationwallpaperinject',
                               'edgewallpaper', 'server', 'dx', 'steam', 'java', 'javaw', 'javaw', 'jfr']  # Hardcoded filter list

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
            self.create_company_button(company, directory)  # Create button regardless of directory existence
            if games_list:
                self.games[company] = games_list

    def find_games(self, directory):
        """Search for .exe files in the specified directory and return game names without .exe"""
        games = []
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".exe"):  # Find all .exe files
                        game_name = file[:-4]  # Remove the .exe extension
                        if not self.is_filtered(game_name):  # Check if the game is filtered
                            games.append(os.path.join(root, file))  # Store the full path
        return games

    def is_filtered(self, game_name):
        """Check if the game name contains any of the filtered words"""
        for word in self.filtered_words:
            if word.lower() in game_name.lower():  # Case-insensitive matching
                print(f"Filtering out '{game_name}' because it contains '{word}'")  # Debugging
                return True
        return False

    def create_company_button(self, company, directory):
        """Create a button for each company with styling"""
        button_style = "Company.TButton"
        button_text = company
        command = lambda c=company: self.show_games(c)

        # If directory does not exist, make the button disabled and grayed out
        if not os.path.exists(directory):
            button_style = "DisabledCompany.TButton"
            command = None  # Disable the button's functionality
            button_text += " (Not Detected)"
        
        button = ttk.Button(self.root, text=button_text, style=button_style, command=command)
        button.pack(pady=10, fill="x", padx=50)
        self.buttons[company] = button

        # Add a tooltip for grayed-out buttons
        if not os.path.exists(directory):
            self.create_tooltip(button, "Not Detected, Error? Report to the developer")

    def create_tooltip(self, widget, text):
        """Create a tooltip for a given widget"""
        tooltip = ttk.Label(self.root, text=text, relief="solid", background="lightyellow", borderwidth=1, anchor="w")
        tooltip.place_forget()  # Hide it initially
        
        def on_enter(event):
            tooltip.place(x=event.x_root + 10, y=event.y_root + 10)  # Position near the widget

        def on_leave(event):
            tooltip.place_forget()  # Hide tooltip when mouse leaves the widget
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

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
            game_button = ttk.Button(buttons_frame, text=os.path.basename(game)[:-4], style="Game.TButton", command=lambda g=game: self.launch_game(g, company))
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

    def launch_game(self, game_path, company):
        """Launch the game based on its path"""
        try:
            print(f"Attempting to launch: {game_path}")  # Debugging

            if os.path.exists(game_path):
                os.startfile(game_path)  # Launch the game
                print(f"Launching game: {game_path}")  # Debugging
            else:
                raise FileNotFoundError(f"Game not found: {game_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game: {e}")
            print(f"Error launching game: {e}")  # Debugging

    def get_directory_by_company(self, company):
        """Return the directory path for the given company"""
        directories = {
            'Steam': r'C:\Program Files (x86)\Steam\steamapps\common',
            'Epic Games': r'C:\Program Files\Epic Games',
            'GOG': r'C:\Program Files (x86)\GOG Galaxy\Games',
            'Ubisoft': r'C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games',
        }
        return directories.get(company, "")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncherApp(root)

    # Hardcoded filter list is already defined in the class itself

    # Configure the style for buttons
    style = ttk.Style()
    style.configure("Company.TButton", font=("Arial", 14), padding=10, relief="flat", background="#4CAF50", foreground="white")
    style.configure("DisabledCompany.TButton", font=("Arial", 14), padding=10, relief="flat", background="#d3d3d3", foreground="gray")
    style.configure("Game.TButton", font=("Arial", 12), padding=8, relief="flat", background="#2196F3", foreground="white")
    style.map("Company.TButton", background=[('active', '#45a049')], foreground=[('active', 'black')])
    style.map("Game.TButton", background=[('active', '#1E88E5')], foreground=[('active', 'black')])

    root.mainloop()
