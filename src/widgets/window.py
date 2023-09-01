import tkinter as tk
from tkinter import ttk

class Window:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.notebook = ttk.Notebook(self.root)

        self.record_tab = tk.Frame(self.notebook)
        self.edit_tab = tk.Frame(self.notebook)
        self.export_tab = tk.Frame(self.notebook) 

        self.notebook.add(self.record_tab,text="Record")
        self.notebook.add(self.edit_tab,text="Edit")
        self.notebook.add(self.export_tab,text="Export")
        self.notebook.pack(expand=True,fill="both")


    def run_app(self):
        self.root.mainloop()


window = Window()
