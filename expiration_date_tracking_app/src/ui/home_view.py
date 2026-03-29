from tkinter import ttk, constants
from services.user_service import user_service

class HomeView():
  def __init__(self, root):
    self._root = root
    self._frame = None
    self._user = user_service.get_current_user()

    self._initialize()

  def pack(self):
    self._frame.pack(fill=constants.X)

  def destroy(self):
    self._frame.destroy()

  def _initialize(self):
    self._frame = ttk.Frame(master=self._root)

    title = ttk.Label(master=self._frame, text="Welcome", font=(None, 32, "bold"))
    text = ttk.Label(master=self._frame, text=f"Logged in as {self._user.username}")

    title.grid(row=0, column=0, columnspan=2, pady=5)
    text.grid(row=1, column=0)