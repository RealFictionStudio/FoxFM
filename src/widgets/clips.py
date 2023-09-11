import customtkinter as ctk

class AudioClip(ctk.CTkFrame):
    def __init__(self, display, clip, **kwargs) -> None:
        super().__init__(display, **kwargs)
        self.configure(fg_color="grey")
        self.filename = ctk.CTkLabel(self, text=clip.filename)
        self.filename.place(relx=0.4)

class VideoClip(ctk.CTkFrame):
    def __init__(self, display, clip, **kwargs) -> None:
        super().__init__(display, **kwargs)

