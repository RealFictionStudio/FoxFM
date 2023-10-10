import tkinter as tk
from tkinter.messagebox import askokcancel, WARNING
import customtkinter as ctk

#from recorder import Recorder
from editor import Editor
from downloader import Downloader

#from load_config import load_config_settings

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class Window:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.title("FoxFM Studio v0.8")
        
        self.tabview = ctk.CTkTabview(master=self.root)
        self.tabview.pack(expand=True, fill="both")

        self.tabview.add("download")
        #self.tabview.add("record")
        self.tabview.add("  edit  ")
        #self.tabview.add("upload")
        self.tabview.set("download")

        self.child_w:tk.Toplevel


    def create_loading(self) -> None:
        child_w = ctk.Toplevel(self.root)

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
        #Recorder(self.tabview.tab("record"))
        Editor(self.tabview.tab("  edit  "))
        Downloader(self.tabview.tab("download"), self.root)
        self.root.mainloop()


window = Window()
