import tkinter as tk
import time

def pick_vial(surf: tk.Canvas, index: int, on_off: bool) -> None:
    n = -1 if on_off else 1
    for i in range(10):
        surf.move(f"vial{index}", 0, 4*n)
        time.sleep(0.001)
        surf.update()

def create_vial(surf: tk.Canvas, x: float, y: float, 
                tag: str|tuple = "", color: str = "#000000") -> None:
    """
    Create vial-shaped group of shapes with given tag
    """
    surf.create_rectangle(x, y-20, x+60, y+180, outline="", fill="", tags=tag)
    surf.create_arc(x, y+120, x+60, y+180, start=180, extent=180, style=tk.ARC,
                    outline=color, tags=tag, width=2)
    surf.create_line(x, y-20, x, y+150, fill=color, tags=tag, width=2)
    surf.create_line(x+60, y-20, x+60, y+150, fill=color, tags=tag, width=2)

def create_vial_fill(surf: tk.Canvas, x: float, y: float, 
                     part: int, tag: str|tuple, color: str = "#000000") -> None:
    """
    Create fill of given part of vial
    """
    if part != 3:
        surf.create_rectangle(x+1, y+(45*part), x+59, y+(45*(part+1)), 
                              fill=color, tags=tag, outline="")
    else: 
        surf.create_rectangle(x+1, y+135, x+59, y+150, 
                              fill=color, tags=tag, outline="")
        surf.create_arc(x+2, y+120, x+58, y+179, start=180, extent=180, style=tk.CHORD,
                        fill=color, outline="", tags=tag)