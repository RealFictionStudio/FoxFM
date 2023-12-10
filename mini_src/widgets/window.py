import customtkinter as ctk

#from recorder import Recorder
from editor import Editor
from downloader import Downloader
from player import Player

#from load_config import load_config_settings

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class Window:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.title("FoxFM Studio v1.2")
        
        self.tabview = ctk.CTkTabview(master=self.root)
        self.tabview.pack(expand=True, fill="both")

        self.tabview.add("download")
        #self.tabview.add("record")
        self.tabview.add("  edit  ")
        #self.tabview.add("upload")
        self.tabview.add("player")

        self.tabview.set("download")


    def run_app(self) -> None:
        #Recorder(self.tabview.tab("record"))
        Editor(self.tabview.tab("  edit  "))
        Downloader(self.tabview.tab("download"), self.root)
        Player(self.tabview.tab("player"))
        self.root.mainloop()


window = Window()
