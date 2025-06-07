import tkinter as tk
from tkinter import filedialog, messagebox, font
import re
import os

BG_COLOR = "#000000"
FG_COLOR = "#00FF99"
FONT_FILE = "Perfect DOS VGA 437.ttf"
FONT_SIZE = 12

LANGUAGES = {
    "en": {
        "title": "Music.kdr Editor",
        "browse": "Browse",
        "add_track": "Add Track",
        "save": "Save",
        "switch_lang": "Русский",
        "dev_name": "Dev Name",
        "title_field": "Title",
        "artist": "Artist",
        "track": "Track",
        "existing_tracks": "Existing Tracks"
    },
    "ru": {
        "title": "Редактор music.kdr",
        "browse": "Обзор",
        "add_track": "Добавить",
        "save": "Сохранить",
        "switch_lang": "English",
        "dev_name": "Имя разработчика",
        "title_field": "Название",
        "artist": "Артист",
        "track": "Трек",
        "existing_tracks": "Существующие треки"
    }
}

class RetroEditor:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.translations = LANGUAGES[self.lang]
        self.parsed_data = []
        self.filepath = None

        # Регистрируем шрифт
        self.custom_font = self.load_pixel_font()

        self.root.title(self.translations["title"])
        self.root.configure(bg=BG_COLOR)
        self.build_ui()

    def load_pixel_font(self):
        try:
            if os.path.exists(FONT_FILE):
                fontname = font.Font(family="DOS", size=FONT_SIZE)
                font.Font(family="DOS", size=FONT_SIZE)
                return fontname
        except:
            pass
        return ("Courier", FONT_SIZE)

    def build_ui(self):
        self.labels = {}

        self.browse_btn = tk.Button(self.root, text=self.translations["browse"], command=self.browse_file, bg=BG_COLOR, fg=FG_COLOR, font=self.custom_font)
        self.browse_btn.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.lang_btn = tk.Button(self.root, text=self.translations["switch_lang"], command=self.toggle_lang, bg=BG_COLOR, fg=FG_COLOR, font=self.custom_font)
        self.lang_btn.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        self.track_text = tk.Text(self.root, height=15, width=80, bg=BG_COLOR, fg=FG_COLOR, font=self.custom_font, insertbackground=FG_COLOR)
        self.track_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.fields = {}
        for idx, key in enumerate(["dev_name", "title_field", "artist", "track"]):
            label = tk.Label(self.root, text=self.translations[key], bg=BG_COLOR, fg=FG_COLOR, font=self.custom_font)
            label.grid(row=2+idx, column=0, sticky="e", padx=5)
            self.labels[key] = label

            entry = tk.Entry(self.root, bg=BG_COLOR, fg=FG_COLOR, font=self.custom_font, insertbackground=FG_COLOR)
            entry.grid(row=2+idx, column=1, sticky="w", padx=5, pady=2)
            self.fields[key] = entry

        self.add_btn = tk.Button(self.root, text=self.translations["add_track"], command=self.add_track, bg=BG_COLOR, fg=FG_COLOR, font=self.custom_font)
        self.add_btn.grid(row=6, column=0, sticky="w", padx=5, pady=5)

        self.save_btn = tk.Button(self.root, text=self.translations["save"], command=self.save_file, bg=BG_COLOR, fg=FG_COLOR, font=self.custom_font)
        self.save_btn.grid(row=6, column=1, sticky="e", padx=5, pady=5)

    def toggle_lang(self):
        self.lang = "ru" if self.lang == "en" else "en"
        self.translations = LANGUAGES[self.lang]
        self.root.title(self.translations["title"])
        self.browse_btn.config(text=self.translations["browse"])
        self.lang_btn.config(text=self.translations["switch_lang"])
        self.add_btn.config(text=self.translations["add_track"])
        self.save_btn.config(text=self.translations["save"])

        for key, label in self.labels.items():
            label.config(text=self.translations[key])

        self.display_tracks()

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("music.kdr", "*.kdr")])
        if path:
            self.filepath = path
            with open(path, "r", encoding="utf-8") as f:
                self.parsed_data = self.parse_kdr(f.read())
                self.display_tracks()

    def parse_kdr(self, text):
        blocks = re.findall(r"\{([^}]+)\}", text, re.DOTALL)
        data = []
        for block in blocks:
            entry = {}
            for line in block.strip().split("\n"):
                if ":" in line:
                    k, v = line.strip().split(":", 1)
                    entry[k.strip()] = v.strip()
            data.append(entry)
        return data

    def display_tracks(self):
        self.track_text.delete("1.0", tk.END)
        artist_dict = {}
        for track in self.parsed_data:
            artist = track.get("artist", "Unknown")
            artist_dict.setdefault(artist, []).append(track)

        for artist, tracks in artist_dict.items():
            self.track_text.insert(tk.END, f"== {artist} ==\n")
            for t in tracks:
                self.track_text.insert(tk.END, f"  • {t.get('title')} [{t.get('track')}]\n")
            self.track_text.insert(tk.END, "\n")

    def add_track(self):
        entry = {
            "dev_name": self.fields["dev_name"].get().strip(),
            "title": self.fields["title_field"].get().strip(),
            "artist": self.fields["artist"].get().strip(),
            "track": self.fields["track"].get().strip(),
            "start": "1"
        }

        if all(entry.values()):
            self.parsed_data.append(entry)
            self.display_tracks()
            for field in self.fields.values():
                field.delete(0, tk.END)
        else:
            messagebox.showwarning("Missing", "Fill all fields!")

    def save_file(self):
        if not self.filepath:
            messagebox.showerror("No file", "File not selected")
            return
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                for block in self.parsed_data:
                    f.write("{\n")
                    for k, v in block.items():
                        f.write(f"\t{k}: {v}\n")
                    f.write("}\n\n")
            messagebox.showinfo("Saved", "File saved!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = RetroEditor(root)
    root.mainloop()
