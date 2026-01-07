import customtkinter as ctk
import minecraft_launcher_lib
import subprocess
import threading
import os
from PIL import Image # pip install pillow

# --- KONFIGURACJA ---
NAZWA_LAUNCHERA = "Fwmboy Launcher"
VERSION = "1.20.1"
CZARNA_LISTA_SLOW = ['chuj', 'kurwa', 'pizda', 'jebac'] # Twoja pełna lista tutaj

ctk.set_appearance_mode("dark")

class TLauncherStyle(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(NAZWA_LAUNCHERA)
        self.geometry("900x500")
        self.resizable(False, False)

        # GŁÓWNY UKŁAD (Dwa panele: Lewy obrazek, Prawy logowanie)
        self.grid_columnconfigure(0, weight=2) # Lewo
        self.grid_columnconfigure(1, weight=1) # Prawo
        self.grid_rowconfigure(0, weight=1)

        # --- LEWY PANEL (OBRAZEK/NEWSY) ---
        self.left_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1e1e1e")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        try:
            # Ładowanie Twojej tekstury tła
            bg_img = ctk.CTkImage(light_image=Image.open("Fwmboy Launcher.png"),
                                  dark_image=Image.open("Fwmboy Launcher.png"),
                                  size=(600, 500))
            self.bg_label = ctk.CTkLabel(self.left_frame, image=bg_img, text="")
            self.bg_label.pack()
        except:
            self.bg_label = ctk.CTkLabel(self.left_frame, text="WSTAW PLIK background.png\nDO FOLDERU", font=("Arial", 20))
            self.bg_label.pack(expand=True)

        # --- PRAWY PANEL (LOGOWANIE) ---
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#2d2d2d")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.right_frame, text="FWMB", font=("Arial Black", 40), text_color="#3fb950")
        self.logo_label.pack(pady=(40, 10))

        self.sub_label = ctk.CTkLabel(self.right_frame, text="Launcher", font=("Arial", 15))
        self.sub_label.pack(pady=(0, 30))

        # Wejście na nick (Styl TLauncher)
        self.nickname_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Nazwa użytkownika", 
                                          width=220, height=35)
        self.nickname_entry.pack(pady=10)

        # Wybór wersji (Na sztywno 1.20.1)
        self.version_label = ctk.CTkLabel(self.right_frame, text=f"Wersja: {VERSION}", text_color="gray")
        self.version_label.pack(pady=5)

        # Status i Progress
        self.status_label = ctk.CTkLabel(self.right_frame, text="Gotowy", font=("Arial", 11), text_color="gray")
        self.status_label.pack(pady=(20, 0))

        self.progress_bar = ctk.CTkProgressBar(self.right_frame, width=200, height=8)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # PRZYCISK GRAJ (Wielki jak w TLauncherze)
        self.launch_button = ctk.CTkButton(self.right_frame, text="ROZPOCZNIJ GRĘ", 
                                          command=self.start_thread,
                                          font=("Arial Black", 14),
                                          width=220, height=45,
                                          fg_color="#3fb950", hover_color="#349443")
        self.launch_button.pack(pady=20)

    def set_status(self, text):
        self.status_label.configure(text=text)

    def update_progress(self, current, total, name):
        progress = float(current) / float(total)
        self.progress_bar.set(progress)
        self.set_status(f"Pobieranie...")

    def start_thread(self):
        nick = self.nickname_entry.get().strip()
        if not nick or any(s in nick.lower() for s in CZARNA_LISTA_SLOW):
            self.set_status("Błąd: Zły nick!")
            return
        threading.Thread(target=self.launch_game, args=(nick,), daemon=True).start()

    def launch_game(self, nick):
        minecraft_dir = os.path.join(os.getcwd(), ".fwmboy_minecraft")
        try:
            self.launch_button.configure(state="disabled", text="ŁADOWANIE...")
            callback = {"setStatus": self.set_status, "setProgress": self.update_progress, "setMax": lambda x: None}

            # Auto-Java i Auto-Install
            minecraft_launcher_lib.runtime.install_jvm_runtime(VERSION, minecraft_dir, callback=callback)
            java_path = minecraft_launcher_lib.runtime.get_executable_path(VERSION, minecraft_dir)
            minecraft_launcher_lib.install.install_minecraft_version(VERSION, minecraft_dir, callback=callback)
            
            options = {"username": nick, "uuid": "", "token": "", "executablePath": java_path}
            command = minecraft_launcher_lib.command.get_minecraft_command(VERSION, minecraft_dir, options)
            
            self.withdraw()
            subprocess.call(command)
            self.deiconify()
        except Exception as e:
            self.set_status("Błąd startu")
        finally:
            self.launch_button.configure(state="normal", text="ROZPOCZNIJ GRĘ")
            self.progress_bar.set(0)

if __name__ == "__main__":
    app = TLauncherStyle()
    app.mainloop()