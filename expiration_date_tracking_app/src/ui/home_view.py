from tkinter import ttk, constants
from services.user_service import user_service


class HomeView():
    def __init__(self, root):
        self._root = root
        self._frame = None
        self._user = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root, padding=20)

        self._title = ttk.Label(
            master=self._frame, text="Welcome", font=(None, 32, "bold"))
        self._status_label = ttk.Label(
            master=self._frame, text="Loading user...")

        self._title.grid(row=0, column=0, sticky="NW", pady=(0, 10))
        self._status_label.grid(row=1, column=0, sticky="NW", pady=(0, 10))

    def set_user(self, user):
        self._user = user
        self._status_label.config(text=f"Logged in as {user.username}")
