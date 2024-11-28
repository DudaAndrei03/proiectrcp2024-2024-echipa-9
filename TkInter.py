import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox  # Importăm messagebox din tkinter


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Form")
        self.root.geometry("540x720")

        # Layout principal
        self.vertical_frame = ttk.Frame(self.root, padding=20, takefocus=1)
        self.vertical_frame.pack(expand=True, fill=BOTH,pady=5)


        #self.label_address = ttk.Label(self.vertical_frame, text="-", bootstyle="light")
        #self.label_address.pack()

        #self.input_text_address = ttk.Entry(self.vertical_frame)
        #self.input_text_address.pack(expand=True, fill=X)

        # Root Folder
        self.label_rootfolder = ttk.Label(self.vertical_frame, text="Root Folder", bootstyle="light")
        self.label_rootfolder.pack(pady=5)

        self.input_text_rootfolder = ttk.Entry(self.vertical_frame)  # Fără bootstyle
        self.input_text_rootfolder.pack(expand=True, fill=X,pady=5)

        # Browse button for selecting Root Folder
        self.button_browse = ttk.Button(
            self.vertical_frame,
            text="Browse",
            bootstyle=INFO,
            command=self.browse_folder  # Conectare funcționalitate
        )
        self.button_browse.pack(pady=5)

        # Select file from the Root Folder
        self.label_file = ttk.Label(self.vertical_frame, text="File Selected", bootstyle="light")
        self.label_file.pack(pady=5)

        self.input_text_file = ttk.Entry(self.vertical_frame, state="disabled")  # Fără bootstyle
        self.input_text_file.pack(expand=True, fill=X,pady=5)

        self.button_openfile = ttk.Button(
            self.vertical_frame,
            text="Open File",
            bootstyle=INFO,
            command=self.open_file  # Conectare funcționalitate pentru deschiderea fișierului
        )
        self.button_openfile.pack(pady=5)

        # Câmp pentru a arăta conținutul fișierului selectat
        self.label_file_content = ttk.Label(self.vertical_frame, text="File Content", bootstyle="light")
        self.label_file_content.pack(pady=20)

        self.text_file_content = ttk.Text(self.vertical_frame, height=10, state="disabled")  # Fără bootstyle
        self.text_file_content.pack(expand=True, fill=BOTH,pady=10)

        # Start button
        self.button_start = ttk.Button(
            self.vertical_frame,
            text="Start",
            bootstyle=SUCCESS,
            command=self.start_process
        )
        self.button_start.pack(expand = True, fill = BOTH ,pady=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:  # Dacă utilizatorul selectează un folder
            self.input_text_rootfolder.delete(0, END)  # Șterge textul vechi
            self.input_text_rootfolder.insert(0, folder_selected)  # Inserează folderul selectat

    def open_file(self):
        root_folder = self.input_text_rootfolder.get()  # Obținem calea folderului root
        if not root_folder:  # Verificăm dacă nu este setat Root Folder
            messagebox.showerror("Error", "Please select a Root Folder first!")
            return

        file_selected = filedialog.askopenfilename(
            initialdir=root_folder,  # Setăm directorul inițial ca fiind Root Folder asta pentru OpenFile
            title="Select a File",  # Titlu fereastră
            filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"))  # Tipuri de fișiere permise
        )
        if file_selected:  # Dacă utilizatorul selectează un fișier
            self.input_text_file.configure(state="normal")  # Activăm câmpul de fișier
            self.input_text_file.delete(0, END)  # Ștergem orice text existent
            self.input_text_file.insert(0, file_selected)  # Inserăm calea fișierului selectat
            self.input_text_file.configure(state="disabled")  # Dezactivam capacitatea de a edita

            # Citim și afișăm conținutul fișierului (dacă este un fișier text)
            with open(file_selected, "r") as file:
                file_content = file.read()  # Citim conținutul fișierului
                self.text_file_content.configure(state="normal")  # Activăm câmpul de text pentru a-l actualiza
                self.text_file_content.delete(1.0, END)  # Ștergem orice conținut existent
                self.text_file_content.insert(1.0, file_content)  # Inserăm conținutul fișierului
                self.text_file_content.configure(state="disabled")  # Dezactivăm câmpul pentru a nu-l modifica

    def start_process(self):
        """Preia datele din câmpuri și afișează un mesaj."""
        #address = self.input_text_address.get()

        root_folder = self.input_text_rootfolder.get()
        selected_file = self.input_text_file.get()
        messagebox.showinfo("Start Process",
                            f"Root Folder: {root_folder}\nFile Selected: {selected_file}")


# Inițializare aplicație
app = ttk.Window(themename="darkly")  # Temă întunecată
app.geometry("550x600")
App(app)
app.mainloop()
