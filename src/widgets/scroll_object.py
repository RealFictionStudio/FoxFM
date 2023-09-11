import customtkinter

class Scroll_Object(customtkinter.CTkScrollableFrame):
    def __init__(self, master, orientation:str="vertical", **kwargs):
        super().__init__(master, **kwargs)

        self._orientation = orientation
        