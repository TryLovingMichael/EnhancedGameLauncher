import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread

SETTINGS_FILE = "game_launcher_settings.json"

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Game Launcher")
        self.games = {}  # Dictionary to store game names and paths
        self.main_game_folder = None  # User-selected main game folder

        # Load settings
        self.load_settings()

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Style
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        # Listbox with scrollbar
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        self.listbox = tk.Listbox(frame, width=50, height=15)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.add_button = ttk.Button(self.button_frame, text="Add Game", command=self.add_game)
        self.add_button.grid(row=0, column=0, padx=5)

        self.launch_button = ttk.Button(self.button_frame, text="Launch Game", command=self.launch_game)
        self.launch_button.grid(row=0, column=1, padx=5)

        self.remove_button = ttk.Button(self.button_frame, text="Remove Game", command=self.remove_game)
        self.remove_button.grid(row=0, column=2, padx=5)

        self.auto_search_button = ttk.Button(self.button_frame, text="Auto Search", command=self.auto_search)
        self.auto_search_button.grid(row=0, column=3, padx=5)

        self.set_folder_button = ttk.Button(self.button_frame, text="Set Main Game Folder", command=self.set_main_folder)
        self.set_folder_button.grid(row=0, column=4, padx=5)

        self.status_label = ttk.Label(self.root, text="Welcome to Enhanced Game Launcher", anchor="center")
        self.status_label.pack(pady=5)

    def add_game(self):
        file_path = filedialog.askopenfilename(title="Select Game Executable",
                                               filetypes=(("Executables", "*.exe"), ("All Files", "*.*")))
        if file_path:
            game_name = os.path.basename(file_path)
            if game_name not in self.games:
                self.games[game_name] = file_path
                self.listbox.insert(tk.END, game_name)
                self.status_label.config(text=f"{game_name} added successfully!")
            else:
                messagebox.showwarning("Warning", "Game already exists!")

    def launch_game(self):
        selected_game = self.listbox.get(tk.ACTIVE)
        if selected_game:
            game_path = self.games[selected_game]
            try:
                os.startfile(game_path)  # Launch the game
                self.status_label.config(text=f"Launching {selected_game}...")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch {selected_game}\n{e}")
        else:
            messagebox.showwarning("Warning", "No game selected!")

    def remove_game(self):
        selected_game = self.listbox.get(tk.ACTIVE)
        if selected_game:
            self.games.pop(selected_game, None)
            self.listbox.delete(tk.ACTIVE)
            self.status_label.config(text=f"{selected_game} removed successfully!")
        else:
            messagebox.showwarning("Warning", "No game selected!")

    def set_main_folder(self):
        # Open folder selection dialog
        folder_path = filedialog.askdirectory(title="Select Main Game Folder")
        if folder_path:
            self.main_game_folder = folder_path
            self.save_settings()  # Save the updated folder to settings
            self.status_label.config(text=f"Main Game Folder set to: {folder_path}")
        else:
            messagebox.showwarning("Warning", "No folder selected!")

    def auto_search(self):
        self.status_label.config(text="Searching for games... This may take a while.")
        Thread(target=self._search_for_games, daemon=True).start()

    def _search_for_games(self):
        # Common directories to search
        search_dirs = [
            os.path.expanduser("~\\Desktop"),  # User's desktop
            "C:\\Program Files (x86)\\Steam\\steamapps\\common",  # Steam
            "C:\\Program Files (x86)\\GOG Galaxy\\Games",  # GOG
            "C:\\Program Files\\Epic Games",  # Epic Games
            "C:\\Program Files (x86)\\Ubisoft\\Ubisoft Game Launcher\\games",  # Ubisoft Connect
            "D:\\Games",  # Example custom directory
            "E:\\Games"  # Example for an additional hard drive
        ]

        # Add user-selected main folder to the search
        if self.main_game_folder:
            search_dirs.append(self.main_game_folder)

        found_games = {}
        for directory in search_dirs:
            if os.path.exists(directory):  # Check if directory exists
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith(".exe"):  # Adjust for your platform
                            game_name = os.path.basename(file)
                            found_games[game_name] = os.path.join(root, file)

        # Update UI with results
        self.root.after(0, self._update_game_list, found_games)

    def _update_game_list(self, found_games):
        if found_games:
            for game_name, game_path in found_games.items():
                if game_name not in self.games:
                    self.games[game_name] = game_path
                    self.listbox.insert(tk.END, game_name)
            self.status_label.config(text="Auto Search completed! Games added.")
        else:
            self.status_label.config(text="No games found during Auto Search.")

    def load_settings(self):
        # Load settings from JSON file
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as file:
                    settings = json.load(file)
                    self.main_game_folder = settings.get("main_game_folder")
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save_settings(self):
        # Save settings to JSON file
        settings = {
            "main_game_folder": self.main_game_folder
        }
        try:
            with open(SETTINGS_FILE, "w") as file:
                json.dump(settings, file, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()
