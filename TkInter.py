import tkinter as tk
from tkinter import filedialog, messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Form")
        self.root.geometry("550x430")

        # Layout principal
        self.vertical_frame = tk.Frame(self.root)
        self.vertical_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Adresa
        self.label_address = tk.Label(self.vertical_frame, text="Address")
        self.label_address.pack()

        self.input_text_address = tk.Entry(self.vertical_frame)
        self.input_text_address.pack(expand=True, fill=tk.X)

        # Root Folder
        self.label_rootfolder = tk.Label(self.vertical_frame, text="Root Folder")
        self.label_rootfolder.pack()

        self.input_text_rootfolder = tk.Entry(self.vertical_frame)
        self.input_text_rootfolder.pack(expand=True, fill=tk.X)

        # Browse button
        self.button_browse = tk.Button(self.vertical_frame, text="Browse", command=self.browse_folder)
        self.button_browse.pack()

        # Start button
        self.button_start = tk.Button(self.vertical_frame, text="Start", command=self.start_process)
        self.button_start.pack(pady=10)

    def browse_folder(self):
        # Deschide un dialog pentru a alege un folder
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.input_text_rootfolder.insert(0, folder_selected)

    def start_process(self):
        # Poți adăuga aici logica de start
        address = self.input_text_address.get()
        root_folder = self.input_text_rootfolder.get()
        messagebox.showinfo("Start Process", f"Starting with Address: {address}\nRoot Folder: {root_folder}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
