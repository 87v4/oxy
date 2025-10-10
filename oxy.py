import time
import json
import os
import threading
from pypresence import Presence
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import StringVar, LEFT, BOTH, X, END, W, VERTICAL, RIGHT, Y
from tkinter import Canvas, Frame, Scrollbar

CONFIG_FOLDER = "profiles"

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self, borderwidth=0)
        scrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

class OxyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Oxy")
        self.running = True
        self.connected = False
        self.start_time = time.time()
        self.rpc = None

        os.makedirs(CONFIG_FOLDER, exist_ok=True)

        # Variables
        self.theme = ttk.StringVar(value="darkly")
        self.profile_name = ttk.StringVar()
        self.client_id = ttk.StringVar()
        self.details = ttk.StringVar()
        self.state = ttk.StringVar()
        self.large_image = ttk.StringVar()
        self.large_text = ttk.StringVar()
        self.small_image = ttk.StringVar()
        self.small_text = ttk.StringVar()

        self.style = ttk.Style(theme=self.theme.get())

        # Window size setup (90% screen)
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        window_w = int(screen_w * 0.9)
        window_h = int(screen_h * 0.9)
        self.center_window(window_w, window_h)

        self.build_ui()
        self.refresh_profiles()
        self.start_updater()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def build_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Theme & Exit
        theme_frame = ttk.Frame(main_frame)
        theme_frame.pack(fill=X, pady=(0,10))
        ttk.Label(theme_frame, text="Theme:").pack(side=LEFT, padx=(0, 5))
        ttk.Combobox(theme_frame, textvariable=self.theme,
                     values=self.style.theme_names(),
                     state="readonly", width=30).pack(side=LEFT)
        ttk.Button(theme_frame, text="Apply Theme", command=self.apply_theme).pack(side=LEFT, padx=5)
        ttk.Button(theme_frame, text="Exit", command=self.quit_app).pack(side=LEFT, padx=20)

        # Profile Manager
        profile_frame = ttk.Labelframe(main_frame, text="Profile Manager", padding=10)
        profile_frame.pack(fill=X, pady=(0,10))

        ttk.Label(profile_frame, text="Profile Name:").pack(anchor=W)
        ttk.Entry(profile_frame, textvariable=self.profile_name).pack(fill=X, pady=3)

        ttk.Label(profile_frame, text="Select Saved Profile:").pack(anchor=W, pady=(5, 0))
        self.profile_menu = ttk.Combobox(profile_frame, textvariable=self.profile_name,
                                         values=[], state="readonly")
        self.profile_menu.pack(fill=X, pady=3)

        profile_btns = ttk.Frame(profile_frame)
        profile_btns.pack(fill=X, pady=5)
        ttk.Button(profile_btns, text="Save Profile", bootstyle=INFO, command=self.save_config).pack(side=LEFT, padx=5)
        ttk.Button(profile_btns, text="Load Profile", bootstyle=SECONDARY, command=self.load_config).pack(side=LEFT)

        # Scrollable form for Presence Data
        form_frame = ScrollableFrame(main_frame)
        form_frame.pack(fill=BOTH, expand=True)

        form = ttk.Labelframe(form_frame.scrollable_frame, text="Oxy Rich Presence", padding=10)
        form.pack(fill=BOTH, expand=True)

        self.add_field(form, "Client ID", self.client_id)
        self.add_field(form, "Details", self.details)
        self.add_field(form, "State", self.state)
        self.add_field(form, "Large Image Key", self.large_image)
        self.add_field(form, "Large Image Text", self.large_text)
        self.add_field(form, "Small Image Key (optional)", self.small_image)
        self.add_field(form, "Small Image Text (optional)", self.small_text)

        ttk.Button(form, text="Start Presence", bootstyle=SUCCESS, command=self.start_presence).pack(pady=10)

        # Status bar bottom
        self.status = ttk.Label(self.root, text="Disconnected", anchor=W, bootstyle=SECONDARY)
        self.status.pack(side="bottom", fill=X)

        # Version label bottom right corner
        version_label = ttk.Label(self.root, text="Version 1.0", bootstyle=INFO)
        version_label.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def add_field(self, parent, label, variable):
        ttk.Label(parent, text=label).pack(anchor=W, pady=(5, 0))
        ttk.Entry(parent, textvariable=variable).pack(fill=X, pady=(0, 5))

    def apply_theme(self):
        self.style.theme_use(self.theme.get())

    def start_presence(self):
        client_id = self.client_id.get().strip()
        if not client_id:
            messagebox.showerror("Missing Info", "Client ID is required.")
            return
        try:
            self.rpc = Presence(client_id)
            self.rpc.connect()
            self.connected = True
            self.status.config(text="Connected", bootstyle=SUCCESS)
            self.update_presence()
        except Exception as e:
            self.connected = False
            self.status.config(text="Failed to connect", bootstyle=DANGER)
            messagebox.showerror("Connection Error", str(e))

    def update_presence(self):
        if self.rpc and self.connected:
            try:
                kwargs = {
                    "details": self.details.get(),
                    "state": self.state.get(),
                    "large_image": self.large_image.get(),
                    "large_text": self.large_text.get(),
                    "start": self.start_time
                }
                # Only include small image if not empty
                if self.small_image.get().strip():
                    kwargs["small_image"] = self.small_image.get()
                if self.small_text.get().strip():
                    kwargs["small_text"] = self.small_text.get()

                self.rpc.update(**kwargs)
            except Exception:
                self.connected = False
                self.status.config(text="Disconnected", bootstyle=WARNING)

    def start_updater(self):
        def loop():
            while self.running:
                if self.rpc and self.connected:
                    self.update_presence()
                time.sleep(15)
        threading.Thread(target=loop, daemon=True).start()

    def save_config(self):
        name = self.profile_name.get().strip()
        if not name:
            messagebox.showerror("Missing Info", "Enter a profile name to save.")
            return
        config = {
            "client_id": self.client_id.get(),
            "details": self.details.get(),
            "state": self.state.get(),
            "large_image": self.large_image.get(),
            "large_text": self.large_text.get(),
            "small_image": self.small_image.get(),
            "small_text": self.small_text.get(),
            "theme": self.theme.get()
        }
        path = os.path.join(CONFIG_FOLDER, f"{name}.json")
        with open(path, "w") as f:
            json.dump(config, f)
        messagebox.showinfo("Saved", f"Profile '{name}' saved.")
        self.refresh_profiles()

    def load_config(self):
        name = self.profile_name.get().strip()
        path = os.path.join(CONFIG_FOLDER, f"{name}.json")
        if not os.path.exists(path):
            messagebox.showerror("Error", f"Profile '{name}' does not exist.")
            return
        with open(path, "r") as f:
            config = json.load(f)
        self.client_id.set(config.get("client_id", ""))
        self.details.set(config.get("details", ""))
        self.state.set(config.get("state", ""))
        self.large_image.set(config.get("large_image", ""))
        self.large_text.set(config.get("large_text", ""))
        self.small_image.set(config.get("small_image", ""))
        self.small_text.set(config.get("small_text", ""))
        theme = config.get("theme", "darkly")
        if theme in self.style.theme_names():
            self.theme.set(theme)
            self.apply_theme()
        messagebox.showinfo("Loaded", f"Profile '{name}' loaded.")

    def refresh_profiles(self):
        profiles = [f[:-5] for f in os.listdir(CONFIG_FOLDER) if f.endswith(".json")]
        self.profile_menu.config(values=profiles)
        if profiles:
            self.profile_name.set(profiles[0])
        else:
            self.profile_name.set("")

    def quit_app(self):
        self.running = False
        if self.rpc and self.connected:
            try:
                self.rpc.clear()
                self.rpc.close()
            except:
                pass
        self.root.destroy()

def main():
    root = ttk.Window()
    app = OxyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
