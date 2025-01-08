import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer")
        self.root.geometry("720x600")

        # Layout principal
        self.vertical_frame = ttk.Frame(self.root, padding=20)
        self.vertical_frame.pack(expand=True, fill=BOTH)

        # Select Root Folder
        self.label_rootfolder = ttk.Label(self.vertical_frame, text="Root Folder", bootstyle="light")
        self.label_rootfolder.pack(pady=5)

        self.input_text_rootfolder = ttk.Entry(self.vertical_frame)
        self.input_text_rootfolder.pack(expand=True, fill=X, pady=5)

        self.button_browse = ttk.Button(
            self.vertical_frame,
            text="Browse",
            bootstyle=INFO,
            command=self.browse_folder
        )
        self.button_browse.pack(pady=5)

        # Treeview pentru afișarea fișierelor și directoarelor
        self.tree = ttk.Treeview(self.vertical_frame, selectmode="browse")
        self.tree.pack(expand=True, fill=BOTH, pady=10)
        self.tree.bind("<<TreeviewOpen>>", self.expand_tree)  # Când utilizatorul deschide un nod

        # Buton pentru deschiderea fișierului selectat
        self.button_open_file = ttk.Button(
            self.vertical_frame,
            text="Open File",
            bootstyle=SUCCESS,
            command=self.open_file
        )
        self.button_open_file.pack(pady=5)

        # Text widget pentru afișarea conținutului fișierului
        self.text_file_content = ttk.Text(self.vertical_frame, height=10, state="disabled")
        self.text_file_content.pack(expand=True, fill=BOTH, pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.input_text_rootfolder.delete(0, END)
            self.input_text_rootfolder.insert(0, folder_selected)

            # Reîncărcăm treeview
            self.tree.delete(*self.tree.get_children())
            self.insert_tree_nodes("", folder_selected)

    def insert_tree_nodes(self, parent, path):
        """Adaugă noduri pentru directoare și fișiere."""
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    node = self.tree.insert(parent, "end", text=item, values=[item_path], open=False)
                    self.tree.insert(node, "end")  # Adaugăm un nod fals pentru expandare
                else:
                    self.tree.insert(parent, "end", text=item, values=[item_path])
        except PermissionError:
            messagebox.showwarning("Permission Error", f"Cannot access {path}")

    def expand_tree(self, event):
        """Extinde directoarele când utilizatorul le deschide."""
        selected_node = self.tree.focus()
        path = self.tree.item(selected_node, "values")[0]
        self.tree.delete(*self.tree.get_children(selected_node))
        self.insert_tree_nodes(selected_node, path)

    def open_file(self):
        """Deschide fișierul selectat și afișează conținutul acestuia."""
        selected_node = self.tree.focus()
        if not selected_node:
            messagebox.showerror("Error", "Please select a file!")
            return

        path = self.tree.item(selected_node, "values")[0]
        if os.path.isdir(path):
            messagebox.showerror("Error", "The selected item is a directory!")
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_file_content.configure(state="normal")
                self.text_file_content.delete(1.0, END)
                self.text_file_content.insert(1.0, content)
                self.text_file_content.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")


# Inițializare aplicație
app = ttk.Window(themename="darkly")
App(app)
app.mainloop()