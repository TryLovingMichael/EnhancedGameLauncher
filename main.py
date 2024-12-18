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
                               'jab', 'jaccess', 'java', 'jfr', 'jrun', 'keytool', 'kinit', 'klist',
                               'ktab', 'rmi', 'rmiregistry', 'window3d', 'compiler', 'atg', 'dotNet',
                               'oalinst', 'vcredist', 'vc_redist', 'VC_redist', 'openssl', 'installer',
                               'launcher', 'diagnostic', 'apputil', 'microsoft', 'winr', 'ui32', 'ui64',
                               'steamredown', 'wallpaperservice', 'webwallpaper', 'applicationwallpaperinject',
                               'edgewallpaper', 'server', 'dx', 'steam', 'java', 'javaw', 'javaw', 'jfr']  # Hardcoded filter list
        self.search_var = tk.StringVar()  # Store the search query
        self.games_buttons_frame = None  # Frame to hold the search result buttons
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
                print(f"Loaded games for {company}: {games_list}")  # Debugging to ensure games are loaded

        # Create the search bar and search button
        self.create_search_bar()

    def create_search_bar(self):
        """Create a search bar for filtering games"""
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, fill="x", padx=50)

        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12))
        search_entry.pack(side="left", fill="x", expand=True)

        search_button = ttk.Button(search_frame, text="Search", command=self.filter_games)
        search_button.pack(side="right", padx=10)

        # Bind the search variable to filter the games whenever the text changes
        self.search_var.trace("w", lambda *args: self.filter_games())

    def filter_games(self):
        """Filter the games based on the search query"""
        search_query = self.search_var.get().lower()  # Convert search query to lowercase for case-insensitive matching
        print(f"Filtering games with query: {search_query}")  # Debugging to check what is entered

        # Create a new frame for the search results if it's not already created
        if self.games_buttons_frame is None:
            self.games_buttons_frame = ttk.Frame(self.root)
            self.games_buttons_frame.pack(pady=10, fill="x", padx=50)

        # If query is empty, just show all games again
        if not search_query:
            self.clear_search_results()  # Clear any previous search results
            return

        found_games = False  # Track if we find any games matching the query

        # Add buttons for each game that matches the search query
        for company, games_list in self.games.items():
            for game in games_list:
                game_name = os.path.basename(game)[:-4]  # Remove the .exe extension
                if search_query in game_name.lower():  # Case-insensitive matching
                    found_games = True
                    game_button = ttk.Button(self.games_buttons_frame, text=game_name, style="Game.TButton", command=lambda g=game: self.launch_game(g))
                    game_button.pack(pady=5, fill="x", padx=20)
                    print(f"Game found: {game_name}")  # Debugging to check if game matches the search query

        # If no games are found, show a message
        if not found_games:
            no_results_label = ttk.Label(self.games_buttons_frame, text="No games found", font=("Arial", 12))
            no_results_label.pack(pady=10)

    def clear_search_results(self):
        """Clear all search results from the screen"""
        if self.games_buttons_frame:
            for widget in self.games_buttons_frame.winfo_children():
                widget.destroy()  # Remove previous search results

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
            game_button = ttk.Button(buttons_frame, text=os.path.basename(game)[:-4], style="Game.TButton", command=lambda g=game: self.launch_game(g))
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

    def launch_game(self, game_path):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncherApp(root)

    # Configure the style for buttons
    style = ttk.Style()
    style.configure("Company.TButton", font=("Arial", 14), padding=10, relief="flat", background="#4CAF50", foreground="white")
    style.configure("DisabledCompany.TButton", font=("Arial", 14), padding=10, relief="flat", background="#d3d3d3", foreground="gray")
    style.configure("Game.TButton", font=("Arial", 12), padding=8, relief="flat", background="#2196F3", foreground="white")
    style.map("Company.TButton", background=[('active', '#45a049')], foreground=[('active', 'black')])
    style.map("Game.TButton", background=[('active', '#1E88E5')], foreground=[('active', 'black')])

    root.mainloop()
