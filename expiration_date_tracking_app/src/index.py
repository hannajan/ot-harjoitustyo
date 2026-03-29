import os
from tkinter import Tk
from ui.ui import UI

dirname = os.path.dirname(__file__)

def main():
  window = Tk()
  window.title("Expiration date tracking app")

  ui_view = UI(window)
  ui_view.start()

  window.mainloop()

if __name__ == "__main__":
    main()