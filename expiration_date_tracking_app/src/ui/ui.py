from tkinter import Tk
from ui.create_merchant_view import CreateMerchantView

class UI:
  def __init__(self, root):
    self._root = root
    self._current_view = None

  def start(self):
    self._show_create_merchant_view()

  def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

  def _handle_register_merchant(self,username, password):
    print(f"Username to register: {username}, password: {password}")

  def _show_create_merchant_view(self):
    self._current_view = CreateMerchantView(
        self._root,
        self._handle_register_merchant
    )

    self._current_view.pack()

window = Tk()
window.title("Register")

ui = UI(window)
ui.start()

window.mainloop()