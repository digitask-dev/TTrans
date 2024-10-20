import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
import src.app as app

if __name__ == "__main__":
    try:
        root = tk.Tk()
        gui = app.App(root)
        root.mainloop()
    except Exception as e:
        print(e)
    