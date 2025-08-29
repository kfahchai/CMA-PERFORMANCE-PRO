# main.py
import tkinter as tk
from sales_ui import SalesUI

def main():
    """
    Entry point for the Sales Performance Analyzer application.
    """
    root = tk.Tk()
    app = SalesUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
