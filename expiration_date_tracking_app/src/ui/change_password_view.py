from tkinter import ttk, StringVar, constants
from services.user_service import user_service


class ChangePasswordView():
    """Näkymä, joka vastaa kertakirjautumissalasanan vaihdosta
    """

    def __init__(self, root, show_home_view):
        """Luokan konstruktori

        Args:
            root: TKinter-elementti, jonka sisään näkymä luodaan.
            show_home_view: Kutsuttava-elementti, joka vastaa aloitusnäkymään siirtymisestä.
        """
        self._root = root
        self._show_home_view = show_home_view
        self._entry_password = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän.
        """
        self._frame.pack(fill=constants.X)
        self._frame.update_idletasks()

    def destroy(self):
        """Piilottaa näkymän.
        """
        self._frame.destroy()

    def _initialize(self):
        """Alustaa näkymän.
        """
        self._frame = ttk.Frame(master=self._root)
        user = user_service.get_current_user()

        title = ttk.Label(
            master=self._frame,
            text="Change your password",
            font=(None, 20, "bold")
        )

        username_label = ttk.Label(
            master=self._frame,
            text=f"Username:"
        )

        username_bold = ttk.Label(
            master=self._frame,
            text=f"{user.username}",
            font=(None, 14, "bold")
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

        confirm_password_label = ttk.Label(
            master=self._frame,
            text="Confirm password:"
        )

        self._entry_password_confirm = StringVar()
        confirm_password_entry = ttk.Entry(
            master=self._frame,
            textvariable=self._entry_password_confirm,
            show="*"
        )

        self._error_message = ttk.Label(
            master=self._frame,
            text=""
        )

        submit_button = ttk.Button(
            master=self._frame,
            text="Change Password",
            command=self._handle_change_password
        )

        title.grid(row=0, column=0, columnspan=2, sticky="W", pady=(5, 10))
        username_label.grid(row=1, column=0, sticky="EW", padx=(5, 2))
        username_bold.grid(row=1, column=1, sticky="EW", padx=(5, 2))
        new_password_label.grid(row=2, column=0, sticky="EW", padx=(5, 2))
        new_password_entry.grid(row=2, column=1, sticky="EW", padx=(5, 2))
        confirm_password_label.grid(row=3, column=0, sticky="EW", padx=(5, 2))
        confirm_password_entry.grid(row=3, column=1, sticky="EW", padx=(5, 2))
        self._error_message.grid(row=4, column=0, columnspan=2, pady=(5, 2))
        submit_button.grid(row=5, column=0, pady=(
            10, 2), padx=(5, 5), sticky="EW")
        new_password_entry.focus()

    def _handle_change_password(self):
        """Handleri, joka vastaa salasanan vaihdosta.
        """
        password = self._entry_password.get().strip()
        password_confirm = self._entry_password_confirm.get().strip()

        try:
            self._do_password_change(password, password_confirm)
        except ValueError as error:
            self._error_message.config(text=f"Error: {error}")

    def _do_password_change(self, password, password_confirm):
        """Vaihtaa salasanan

        Args:
            password: Merkkijono, joka on salasanan syötekenttään annettu arvo.
            password_confirm: Merkkijono, joka on annettu salasanan vahvistuskenttään.

        Raises:
            ValueError, jos salasana ja salasanan vahvistus eivät täsmää.
        """
        if password != password_confirm:
            raise ValueError("Passwords don't match")

        try:
            user_service.update_employee_password(password)
            self._show_home_view()
        except ValueError as error:
            self._error_message.config(text=f"Error: {error}")
