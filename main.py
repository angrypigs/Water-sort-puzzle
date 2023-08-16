import tkinter as tk
import random
import math
import time
import vial_display as VialDisplay
import PIL
import os
import sys

class App:

    def __init__(self) -> None:
        # declare constants
        self.HEIGHT = 700
        self.WIDTH = 1000
        self.LIQUID_COLORS = [["", "#DA2020", "#E7DB14", "#74D81C", "#1C9BD8", "#E89115", "#6B16C5", 
                               "#BDDB3D", "#D61FEB", "#1DDBE0", "#D919B1", 
                               "#249E18", "#313DB8", "#842A2A", "#868686"]]
        # declare variables
        self.vials = []
        self.vial_dist = [0, 0]
        self.current_vial = -1
        # init app
        self.master = tk.Tk()
        self.master.title("Water sort puzzle")
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.canvas = tk.Canvas(self.master, height=self.HEIGHT, width=self.WIDTH, bd=0,
                                highlightthickness=0, bg="#152045")
        self.canvas.place(x=0,y=0)
        self.new_game()
        self.master.mainloop()

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
        self.vial_dist = [(self.WIDTH-60*math.ceil(len(self.vials)/2))/(math.ceil(len(self.vials)/2)+1),
                               (self.WIDTH-60*len(self.vials)//2)/(len(self.vials)//2+1)]
        link = lambda x: (lambda event: self.vial_onclick(x))
        for i in range(len(self.vials)):
            VialDisplay.create_vial(self.canvas, 
                                        self.vial_dist[self.vial_row(i)]*(self.vial_col(i)+1)+self.vial_col(i)*60, 
                                        100+self.vial_row(i)*250, f"vial{i}", "#FFFFFF")
            self.canvas.tag_bind(f"vial{i}", "<Button-1>", link(i))
            if self.vials[i]!=[0, 0, 0, 0]:
                self.update_vial(i)

    def update_vial(self, index: int) -> None:
        """
        Update vial colors with main matrix
        """
        for i in range(4):
            self.canvas.delete(f"liquid{index}_{i}")
            if self.vials[index][i] != 0:
                print(i)
                VialDisplay.create_vial_fill(self.canvas, 
                                            self.vial_dist[self.vial_row(index)]*(self.vial_col(index)+1)
                                            +60*self.vial_col(index), 100+self.vial_row(index)*250, 3-i, 
                                            (f"liquid{index}_{i}", f"vial{index}"), 
                                            self.LIQUID_COLORS[0][self.vials[index][i]])
        print()
        self.canvas.tag_bind(f"vial{index}", "<Button-1>", lambda event: self.vial_onclick(index))
    
    def vial_onclick(self, index: int) -> None:
        """
        Method connected to left-click on vial
        """
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
            VialDisplay.pick_vial(self.canvas, self.current_vial, False)
            self.update_vial(self.current_vial)
            self.update_vial(index)
            self.current_vial = -1
            for i in self.vials:
                print(i)
            print()
            
    
    

if __name__ == "__main__":
    App()