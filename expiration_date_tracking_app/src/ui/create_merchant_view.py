from tkinter import ttk, constants

class CreateMerchantView:
  def __init__(self, root, handle_register_merchant):
    self._root = root
    self._handle_register_merchant = handle_register_merchant
    self._frame = None
    self._entry_username = None
    self._entry_password = None

    self._initialize()

  def pack(self):
    self._frame.pack(fill=constants.X)

  def destroy(self):
    self._frame.destroy()

  def _registeration_handler(self):
    username = self._entry_username.get()
    password = self._entry_password.get()

    self._handle_register_merchant(username, password)

  def _initialize(self):
    self._frame = ttk.Frame(master=self._root)
    title = ttk.Label(master=self._frame, text="Register as merchant")

    label_username = ttk.Label(master=self._frame, text="Username")
    self._entry_username = ttk.Entry(master=self._frame)

    label_password = ttk.Label(master=self._frame, text="Password")
    self._entry_password = ttk.Entry(master=self._frame, show="*")
    
    button = ttk.Button(
        master=self._frame,
        text="Register",
        command=self._registeration_handler
    )

    title.grid(row=0, column=0, columnspan=2, pady=5)
    label_username.grid(row=1, column=0, padx=5, pady=5)
    self._entry_username.grid(row=1, column=1, padx=5, pady=5)
    label_password.grid(row=2, column=0, padx=5, pady=5)
    self._entry_password.grid(row=2, column=1, padx=5, pady=5)
    button.grid(row=3, column=0, columnspan=2, pady=10)