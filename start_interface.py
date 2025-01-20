from tkinter import Tk, Frame, Label, Button
import ai as ai
from game_interface import initialize_game_interface

class StartInterface:
    def __init__(self):
        self.root = Tk()
        self.root.title("Yinsh")
        self.root.geometry("500x500")
        self.startinterface()

    # Fonction pour lancer l'interface
    def startinterface(self):
        self.clear_screen()
        self.title_label = Label(self.root, text="Yinsh", font=("Helvetica", 40), fg="blue")
        self.title_label.pack(pady=50)

        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=20)

        self.single_player_button = Button(self.button_frame, text="Single Player", font=("Helvetica", 20), command=self.ai_game)
        self.single_player_button.pack(side='left', padx=20)

        self.multiplayer_button = Button(self.button_frame, text="Multiplayers", font=("Helvetica", 20), command=self.multiplayer_options)
        self.multiplayer_button.pack(side='right', padx=20)

    # Fonction pour afficher les options de base
    def multiplayer_options(self):
        self.clear_screen()
        self.title_label = Label(self.root, text="Multiplayers Options", font=("Helvetica", 40), fg="blue")
        self.title_label.pack(pady=50)

        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=20)

        self.local_button = Button(self.button_frame, text="Local", font=("Helvetica", 20), command=self.local_multiplayer_options)
        self.local_button.pack(side='left', padx=10)

        self.online_button = Button(self.button_frame, text="Online", font=("Helvetica", 20), command=self.online_multiplayer)
        self.online_button.pack(side='left', padx=10)

        self.back_button = Button(self.button_frame, text="Back", font=("Helvetica", 20), command=self.startinterface)
        self.back_button.pack(side='bottom', pady=20)

    # Fonction pour afficher les options de multijoueur local
    def local_multiplayer_options(self):
        self.clear_screen()
        self.title_label = Label(self.root, text="Select Game Mode", font=("Helvetica", 40), fg="blue")
        self.title_label.pack(pady=50)

        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=20)

        self.normal_button = Button(self.button_frame, text="Normal", font=("Helvetica", 20), command=self.start_normal_game)
        self.normal_button.pack(side='left', padx=20)

        self.blitz_button = Button(self.button_frame, text="Blitz", font=("Helvetica", 20), command=self.start_blitz_game)
        self.blitz_button.pack(side='left', padx=20)

        self.back_button = Button(self.button_frame, text="Back", font=("Helvetica", 20), command=self.multiplayer_options)
        self.back_button.pack(side='bottom', pady=20)

    # Fonction pour lancer une partie normale
    def start_normal_game(self):
        self.root.destroy()
        game_interface = initialize_game_interface("normal")
        game_interface.master.mainloop()

    # Fonction pour lancer une partie blitz
    def start_blitz_game(self):
        self.root.destroy()
        game_interface = initialize_game_interface("blitz")
        game_interface.master.mainloop()

    # Fonction pour lancer une partie contre l'IA
    def ai_game(self):
        self.root.destroy()
        game_interface = initialize_game_interface("ai")
        game_interface.master.mainloop()

    # Fonction pour lancer une partie en ligne (non fonctionnelle, voir le dossier "jeu_reseau")
    def online_multiplayer(self):
        pass

    # Fonction pour effacer l'écran
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Fonction pour lancer l'interface
    def run(self):
        self.root.mainloop()
