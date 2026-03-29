from tkinter import ttk, StringVar, constants
from services.user_service import user_service
import threading

class LoginView():
  def __init__(self, root, handle_login, handle_create_merchant_view):
    self._root = root
    self._frame = None
    self._entry_username = None
    self._entry_password = None
    self._handle_login = handle_login
    self._handle_show_create_merchant_view = handle_create_merchant_view

    self._initialize()

  def pack(self):
    self._frame.pack(fill=constants.X)

  def destroy(self):
    self._frame.destroy()

  def _login_handler(self):
    username = self._entry_username.get()
    password = self._entry_password.get()

    self._status_label.config(text="Logging in...")
    self._frame.update_idletasks()
    threading.Thread(target=self._do_login, args=(username, password), daemon=True).start()

  def _do_login(self, username, password):
    try:
      user_service.login(username, password)
      self._root.after(0, lambda: self._handle_login())
    except ValueError as e:
      print(e)

  def _initialize(self):
    self._frame = ttk.Frame(master=self._root)
    title = ttk.Label(master=self._frame, text="Login")

    label_username = ttk.Label(master=self._frame, text="Username")
    self._entry_username = ttk.Entry(master=self._frame)

    label_password = ttk.Label(master=self._frame, text="Password")
    self._entry_password = ttk.Entry(master=self._frame, show="*")
    self._status_label = ttk.Label(self._frame, text="")
    self._status_label.grid(row=4, column=0, columnspan=2, pady=5)
    
    login_button = ttk.Button(
        master=self._frame,
        text="Login",
        command=self._login_handler
    )

    register_button = ttk.Button(
      master=self._frame,
      text ="Register as Merchant",
      command=self._handle_show_create_merchant_view

    )

    title.grid(row=0, column=0, columnspan=2, pady=5)
    label_username.grid(row=1, column=0, padx=5, pady=5)
    self._entry_username.grid(row=1, column=1, padx=5, pady=5)
    label_password.grid(row=2, column=0, padx=5, pady=5)
    self._entry_password.grid(row=2, column=1, padx=5, pady=5)
    login_button.grid(row=3, column=0, columnspan=2, pady=10)
    register_button.grid(padx=5, pady=5, sticky=constants.EW)