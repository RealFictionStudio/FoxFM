from os import get_terminal_size
from time import sleep

class ProgressBar:
    def __init__(self, current_value:float, full_value:float, character:str="#") -> None:
        self.current_value = current_value
        self.full_value = full_value
        self.character = character

    def update(self, progress_value:float) -> bool:
        self.current_value += progress_value
        columns = get_terminal_size().columns
        percentage_progress = int(((self.current_value / self.full_value)*(columns-2)))
        print(f"[{self.character * percentage_progress}{' ' * (columns - 2 - percentage_progress)}]", end="\r")

        if self.current_value >= self.full_value:
            print(end="\n")
            return True
        return False