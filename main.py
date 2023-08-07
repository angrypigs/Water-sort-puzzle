import tkinter as tk
import vial_display as VialDisplay

class App:

    def __init__(self) -> None:
        # declare constants
        self.HEIGHT = 700
        self.WIDTH = 800
        # declare variables
        self.vials = []
        # init app
        self.master = tk.Tk()
        self.master.title("Water sort puzzle")
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.canvas = tk.Canvas(self.master, height=self.HEIGHT, width=self.WIDTH, bd=0,
                                highlightthickness=0, bg="#DDDDDD")
        self.canvas.place(x=0,y=0)
        
        self.master.mainloop()


if __name__ == "__main__":
    App()