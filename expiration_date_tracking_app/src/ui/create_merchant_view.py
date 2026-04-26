from tkinter import ttk, constants
from services.user_service import user_service


class CreateMerchantView:
    """Näkymä, joka vastaa kauppiaan rekisteröinnistä.
    """

    def __init__(self, root, handle_show_login_view):
        """Luokan konstruktori, joka luo kauppiaan rekisteröintinäkymän.

        Args:
            root: TKinter-elemnetti, jonka sisään näkymä luodaan.
            handle_show_login_view: Kutsuttava-arvo, joka vastaa sisäänkirjautumsinäkymän näyttämisestä
        """
        self._root = root
        self._frame = None
        self._entry_username = None
        self._entry_password = None
        self._handle_show_login_view = handle_show_login_view

        self._initialize()

    def pack(self):
        """Näyttää näkymän
        """
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Piilottaa näkymän
        """
        self._frame.destroy()

    def _registeration_handler(self):
        """Handleri, joka vastaa kauppiaan rekisteröinnistä
        """
        username = self._entry_username.get()
        password = self._entry_password.get()
        password_confirm = self._entry_password_confirm.get()

        try:
            self._do_registeration(username, password, password_confirm)
        except ValueError as error:
            self._error_message.config(text=f"Error: {error}")

    def _do_registeration(self, username, password, password_confirm):
        """Rekisteröi kauppiaan

        Args:
            username: Merkkijono, joka on käyttäjätunnus kenttään annettu syöte
            password: Merkkijono, joka on salasana kenttään annettu syöte
            password_confirm: Merkkijono, jonka tulee vastata salasana-kentän syötettä

        Raises:
            ValueError, jos sama salasana ei ole annettu kaksi kertaa.
        """
        if password != password_confirm:
            raise ValueError("Passwords do not match")

        try:
            user_service.register_merchant(username, password)
            self.destroy()
            self._handle_show_login_view()
        except ValueError as error:
            self._error_message.config(text=f"Error: {error}")

    def _handle_back(self):
        """Handleri, joka vastaa sisäänkirjautumisnäkymän näyttämisestä, kun painaa back-nappia
        """
        self._handle_show_login_view()

    def _initialize(self):
        """Alustaa näkymän
        """
        self._frame = ttk.Frame(master=self._root)
        title = ttk.Label(master=self._frame,
                          text="Register as merchant", font=(None, 24, "bold"))

        back_button = ttk.Button(
            master=self._frame, text="Back", command=self._handle_back)

        label_username = ttk.Label(master=self._frame, text="Username")
        self._entry_username = ttk.Entry(master=self._frame)

        label_password = ttk.Label(master=self._frame, text="Password")
        self._entry_password = ttk.Entry(master=self._frame, show="*")

        label_password_confirm = ttk.Label(
            master=self._frame, text="Confirm password")
        self._entry_password_confirm = ttk.Entry(master=self._frame, show="*")

        self._error_message = ttk.Label(
            master=self._frame, text="", style="Error.Label")

        button = ttk.Button(
            master=self._frame,
            text="Register",
            command=self._registeration_handler
        )

        title.grid(row=0, column=0, columnspan=2, pady=5)
        back_button.grid(row=0, column=2, sticky=constants.NE, pady=(0, 10))
        label_username.grid(row=1, column=0, padx=5, pady=5)
        self._entry_username.grid(row=1, column=1, padx=5, pady=5)
        label_password.grid(row=2, column=0, padx=5, pady=5)
        self._entry_password.grid(row=2, column=1, padx=5, pady=5)
        label_password_confirm.grid(row=3, column=0, padx=5, pady=5)
        self._entry_password_confirm.grid(row=3, column=1, padx=5, pady=5)
        self._error_message.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        button.grid(row=5, column=0, columnspan=2, pady=10)
