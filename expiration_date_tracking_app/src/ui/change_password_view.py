from tkinter import ttk, StringVar, constants
from services.user_service import user_service


class ChangePasswordView():
    def __init__(self, root, show_home_view):
        self._root = root
        self._show_home_view = show_home_view
        self._entry_password = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)
        self._frame.update_idletasks()

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        user = user_service.get_current_user()

        title = ttk.Label(
            master=self._frame,
            text="Change your password",
            font=(None, 20, "bold")
        )

        username_label = ttk.Label(
            master=self._frame,
            text=f"Username: {user.username}"
        )

        new_password_label = ttk.Label(
            master=self._frame,
            text="New password:"
        )

        self._entry_password = StringVar()
        new_password_entry = ttk.Entry(
            master=self._frame,
            textvariable=self._entry_password,
            show="*"
        )

        submit_button = ttk.Button(
            master=self._frame,
            text="Change Password",
            command=self._handle_change_password
        )
        submit_button.grid(row=3, column=0, columnspan=2,
                           pady=(10, 0), sticky="EW")

        title.grid(row=0, column=0, columnspan=2, sticky="W", pady=(0, 10))
        username_label.grid(row=1, column=0, sticky="W", padx=(0, 2))
        new_password_label.grid(row=2, column=0, sticky="W", padx=(0, 2))
        new_password_entry.grid(row=2, column=1, sticky="EW", padx=(0, 2))
        new_password_entry.focus()

    def _handle_change_password(self):
        user_service.update_employee_password(self._entry_password.get().strip())
        self._show_home_view()
