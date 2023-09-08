import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
import customtkinter as ctk
from recorder import Recorder

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class Window:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.tabview = ctk.CTkTabview(master=self.root)
        self.tabview.pack(expand=True, fill="both")

        self.tabview.add("record")  # add tab at the end
        self.tabview.add("edit")
        self.tabview.add("upload")  # add tab at the end
        self.tabview.set("record")  # set currently visible tab

        self.child_w:tk.Toplevel


    def create_loading(self) -> None:
        child_w = tk.Toplevel(self.root)
        print("\nCHILD CREATED\n")

        def on_closing_before_saved():
            if askokcancel("Quit", "Do you want to quit?\nThis is going to corrupt current operation", icon=WARNING):
                child_w.destroy()

        child_w.protocol("WM_DELETE_WINDOW", on_closing_before_saved)
        child_w.geometry("400x150")
        child_w.resizable(False,False)
        child_w.title("Operation in progress")

        self.child_w = child_w


    def update_loading(self, value:int) -> None:
        ...        


    def run_app(self) -> None:
        Recorder(self.tabview.tab("record"))
        self.root.mainloop()


window = Window()
