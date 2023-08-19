import tkinter as tk
import random
import math
import time
import vial_display as VialDisplay
import os
import sys
from tkinter import font

class App:

    def __init__(self) -> None:
        # declare constants
        self.HEIGHT = 700
        self.WIDTH = 1000
        self.LIQUID_COLORS = [["", "#B91A1A", "#112B8B", "#1A9924", "#D8C929", "#881FAE", "#A14F5F", 
                               "#B4693F", "#105616", "#5C1578", "#0EA8A3", 
                               "#A78760", "#4768DF", "#A9267B", "#60462B"]]
        # gui colors (0 - main bg, 1 - outlines, 2 - buttons bg)
        self.GUI_COLORS = [["#20273F", "#0F1939", "#31499B"]]
        # declare variables
        self.vials = []
        self.previous_vials = []
        self.vial_dist = [0, 0]
        self.current_vial = -1
        self.flag_menu = False
        # init app
        self.master = tk.Tk()
        self.master.title("Water sort puzzle")
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.master.resizable(False, False)
        self.normal_font = lambda s, w: font.Font(family="Gill Sans MT", size=s, weight=w)
        self.canvas = tk.Canvas(self.master, height=self.HEIGHT, width=self.WIDTH, bd=0,
                                highlightthickness=0, bg=self.GUI_COLORS[0][0])
        self.canvas.place(x=0,y=0)
        self.canvas.create_oval(self.WIDTH-80, 20, self.WIDTH-20, 80, width=3, fill=self.GUI_COLORS[0][2],
                                outline=self.GUI_COLORS[0][1], tags=("undo_btn"))
        self.canvas.create_text(self.WIDTH-50, 50, justify='center', anchor='center',
                                text="\u293A", font=font.Font(size=30, weight='bold'),
                                fill="#0F1939", state='disabled')
        self.canvas.tag_bind("undo_btn", "<Button-1>", lambda event: self.undo_move())
        self.load_game()
        self.check_win()
        self.master.mainloop()

    def res_path(self, rel_path: str) -> str:
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = sys.path[0]
        return os.path.join(base_path, rel_path)

    def top_layer_quantity(self, index: int) -> list:
        """
        Return list with amount of same numbers not including zero starting from end of list and this number,
        or [0, 0] if list consists only of zeros
        """
        n = 0
        counter = 0
        for i in range(3, -1, -1):
            if self.vials[index][i] != 0 and n == 0:
                n = self.vials[index][i]
                counter += 1
            elif self.vials[index][i] == n and n != 0:
                counter += 1
            elif self.vials[index][i] != n and n != 0:
                return [counter, n]
        return [counter, n]

    def vial_row(self, index: int) -> int:
        return 0 if index < math.ceil(len(self.vials)/2) else 1
    
    def vial_col(self, index: int) -> int:
        return index%math.ceil(len(self.vials)/2)

    def new_game(self) -> None:
        """
        Generate new game
        """
        self.canvas.delete("win_panel")
        for i in range(16):
            self.canvas.delete(f"vial{i}")
        n = random.randint(8, 16)
        all_liquids = [i for j in range(4) for i in range(1, n-(1 if n < 13 else 2))]
        self.vials = [[] for i in range(n)]
        random.shuffle(all_liquids)
        for i in range(len(all_liquids)):
            self.vials[i//4].append(all_liquids[i])
        for i in range(len(self.vials)):
            if self.vials[i] == []:
                self.vials[i] = [0 for i in range(4)]
        self.previous_vials = [[x[:] for x in self.vials]]
        self.vial_dist = [(self.WIDTH-60*math.ceil(len(self.vials)/2))/(math.ceil(len(self.vials)/2)+1),
                               (self.WIDTH-60*len(self.vials)//2)/(len(self.vials)//2+1)]
        link = lambda x: (lambda event: self.vial_onclick(x))
        for i in range(len(self.vials)):
            VialDisplay.create_vial(self.canvas, 
                                        self.vial_dist[self.vial_row(i)]*(self.vial_col(i)+1)+self.vial_col(i)*60, 
                                        170+self.vial_row(i)*300, f"vial{i}", "#FFFFFF")
            self.canvas.tag_bind(f"vial{i}", "<Button-1>", link(i))
            self.update_vial(i)
        self.save_game()

    def update_vial(self, index: int) -> None:
        """
        Update vial colors with main matrix
        """
        for i in range(4):
            self.canvas.delete(f"liquid{index}_{i}")
            if self.vials[index][i] != 0:
                VialDisplay.create_vial_fill(self.canvas, 
                                            self.vial_dist[self.vial_row(index)]*(self.vial_col(index)+1)
                                            +60*self.vial_col(index), 170+self.vial_row(index)*300, 3-i, 
                                            (f"liquid{index}_{i}", f"vial{index}"), 
                                            self.LIQUID_COLORS[0][self.vials[index][i]])
        self.canvas.tag_bind(f"vial{index}", "<Button-1>", lambda event: self.vial_onclick(index))
    
    def undo_move(self) -> None:
        """
        Restore vials to state before last move
        """
        if len(self.previous_vials) > 1:
            self.previous_vials.pop(-1)
            self.vials = [x[:] for x in self.previous_vials[-1]]
            for i in range(len(self.vials)):
                self.update_vial(i)
            self.save_game()

    def check_win(self) -> bool:
        """
        Check if game is won
        """
        for i in self.vials:
            if i.count(i[0]) != 4:
                return False
        self.flag_menu = True
        self.canvas.create_rectangle(100, 100, self.WIDTH-100, self.HEIGHT-100,
                                     fill=self.GUI_COLORS[0][0], outline=self.GUI_COLORS[0][1], 
                                     width=3, tags=("win_panel"))
        self.canvas.create_rectangle(self.WIDTH//2-100, self.HEIGHT-240,
                                     self.WIDTH//2+100, self.HEIGHT-180,
                                     fill=self.GUI_COLORS[0][2], outline=self.GUI_COLORS[0][1],
                                     width=3, tags=("win_panel", "win_restart_btn"))
        self.canvas.create_text(self.WIDTH//2, self.HEIGHT-210, font=self.normal_font(30, 'normal'),
                                text="Next level", justify='center', anchor='center',
                                tags=("win_panel"), state='disabled')
        self.canvas.tag_raise("win_panel")
        self.canvas.tag_bind("win_restart_btn", "<Button-1>", lambda event: self.new_game())
        return True
        
    

    def save_game(self) -> None:
        """
        Save the game status to save.txt
        """
        file = open(self.res_path("save.txt"), "w")
        file.write(";".join([":".join([str(bin(y)) for y in x]) for x in self.vials])+"\n")
        for i in self.previous_vials:
            file.write(";".join([":".join([str(bin(y)) for y in x]) for x in i])+"\n")
        file.close()

    def load_game(self) -> bool:
        """
        Try to load game status from save.txt, when encounter an error call for new game
        """
        try:
            file = open(self.res_path("save.txt"), "r").readlines()
            for i in range(len(file)):
                if i == 0:
                    self.vials = [[int(y, 2) for y in z] for z in 
                                  [x.split(":") for x in file[i].rstrip().split(";")]]
                else:
                    self.previous_vials.append([[int(y, 2) for y in z] for z in 
                                                [x.split(":") for x in file[i].rstrip().split(";")]])
            self.vial_dist = [(self.WIDTH-60*math.ceil(len(self.vials)/2))/(math.ceil(len(self.vials)/2)+1),
                               (self.WIDTH-60*len(self.vials)//2)/(len(self.vials)//2+1)]
            link = lambda x: (lambda event: self.vial_onclick(x))
            for i in range(len(self.vials)):
                VialDisplay.create_vial(self.canvas, 
                                            self.vial_dist[self.vial_row(i)]*(self.vial_col(i)+1)+self.vial_col(i)*60, 
                                            170+self.vial_row(i)*300, f"vial{i}", "#FFFFFF")
                self.canvas.tag_bind(f"vial{i}", "<Button-1>", link(i))
                self.update_vial(i)
            return True
        except Exception as e:
            print(e)
            self.new_game()
            return False

    def vial_onclick(self, index: int) -> None:
        """
        Method connected to left-click on vial
        """
        if not self.flag_menu:
            if self.current_vial == -1 and self.vials[index].count(0) != 4:
                self.current_vial = index
                VialDisplay.pick_vial(self.canvas, index, True)
            elif self.current_vial != -1:
                new_one = self.top_layer_quantity(index)
                old_one = self.top_layer_quantity(self.current_vial)
                if old_one[0] <= self.vials[index].count(0) and (old_one[1]==new_one[1] or new_one[1] == 0):
                    new_one[0] = old_one[0]
                    for i in range(4):
                        if self.vials[index][i] == 0:
                            self.vials[index][i] = old_one[1]
                            old_one[0] -= 1
                        if old_one[0] == 0:
                            break
                    for i in range(3, -1, -1):
                        if self.vials[self.current_vial][i] == old_one[1]:
                            self.vials[self.current_vial][i] = 0
                            new_one[0] -= 1
                        if new_one[0] == 0:
                            break
                    if len(self.previous_vials) == 6:
                        self.previous_vials.pop(0)
                    self.previous_vials.append([x[:] for x in self.vials])
                    self.save_game()
                    self.check_win()
                VialDisplay.pick_vial(self.canvas, self.current_vial, False)
                self.update_vial(self.current_vial)
                self.update_vial(index)
                self.current_vial = -1

if __name__ == "__main__":
    App()