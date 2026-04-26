from tkinter import ttk, StringVar
from services.user_service import user_service
from services.department_service import department_service

# Luokan runko generoitu tekoälyllä


class StoreView:
    """Näkymä, joka vastaa kaupan tietojen näyttämisestä
    """

    def __init__(self, root, store, user, show_home_view, show_department_view):
        """Luokan konstruktori, joka luo uuden kauppanäkymän.

        Args:
            root: TKinter-elementti, jonka sisään näkymä luodaan.
            store: Store-olio, joka on näytettävä kauppa
            user: User-olio, joka on kirjautuneena sovellukseen.
            show_home_view: Kutsuttava-arvo, joka vastaa aloitusnäkymään siirtymisestä
            show_department_view: Kutsuttava-arvo, joka vastaa osastonäkymään siirtymisestä.
        """
        self._root = root
        self._store = store
        self._user = user
        self._show_home_view = show_home_view
        self._show_department_view = show_department_view

        self._frame = None
        self._add_department_frame = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän
        """
        self._frame.pack(fill="both", expand=True)

    def destroy(self):
        """Piilottaa näkymän
        """
        self._frame.destroy()

    def _handle_back(self):
        """Handleri, joka vastaa aloitusnäkymän näyttämisestä, kun back-nappia painetaan.
        """
        self._show_home_view()

    def _initialize(self):
        """Alustaa kauppanäkymän.
        """
        self._frame = ttk.Frame(master=self._root, padding=20)

        title = ttk.Label(
            self._frame,
            text=f"{self._store.name}",
            font=(None, 20, "bold")
        )

        back_button = ttk.Button(
            self._frame,
            text="Back",
            command=self._handle_back
        )

        self._status_label = ttk.Label(self._frame, text="")

        self._department_section = ttk.Frame(self._frame)
        self._departments_frame = ttk.Frame(self._frame)

        title.grid(row=0, column=0, sticky="W", pady=(0, 10))
        back_button.grid(row=0, column=1, sticky="E")
        self._status_label.grid(row=1, column=0, columnspan=2, sticky="W")
        self._department_section.grid(
            row=2, column=0, columnspan=2, sticky="W", pady=10)
        self._departments_frame.grid(
            row=3, column=0, columnspan=2, sticky="W", pady=10)

        self._load_departments()

        if self._can_manage():
            self._add_department_button = ttk.Button(
                self._department_section,
                text="Add department",
                command=self._show_add_department
            )
            self._add_department_button.grid(row=0, column=0, sticky="W")

        self._frame.columnconfigure(0, weight=1)

    def _can_manage(self):
        """Tarkistaa onko käyttäjällä manage-käyttöoikeus

        Returns:
            True, jos käyttäjällä on manage-käyttöoikeus, muutoin False
        """
        if not self._user.is_employee():
            return True

        permissions = user_service.get_employee_permissions(self._user.user_id)

        return any(
            p["store_id"] == self._store.store_id and p["permission"] == "manage"
            for p in permissions
        )

    def _show_add_department(self):
        """Näyttää syötkentän, kun painetaan lisää osasto-nappia
        """
        if self._add_department_frame:
            return

        self._add_department_frame = ttk.Frame(self._department_section)
        self._add_department_frame.grid(row=1, column=0, pady=10, sticky="W")

        ttk.Label(
            self._add_department_frame,
            text="Department name"
        ).grid(row=0, column=0, sticky="W")

        self._department_name_var = StringVar()
        name_entry = ttk.Entry(
            self._add_department_frame,
            textvariable=self._department_name_var,
            width=30
        )
        name_entry.grid(row=0, column=1, padx=5)

        ttk.Label(
            self._add_department_frame,
            text="Check days before"
        ).grid(row=1, column=0, sticky="W", pady=(5, 0))

        self._department_days_var = StringVar()
        days_entry = ttk.Entry(
            self._add_department_frame,
            textvariable=self._department_days_var,
            width=10
        )
        days_entry.grid(row=1, column=1, padx=5, pady=(5, 0), sticky="W")

        save_button = ttk.Button(
            self._add_department_frame,
            text="Save",
            command=self._handle_save_department
        )
        save_button.grid(row=2, column=0, pady=10, sticky="W")

        cancel_button = ttk.Button(
            self._add_department_frame,
            text="Cancel",
            command=self._cancel_add_department
        )
        cancel_button.grid(row=2, column=1, pady=10, sticky="W")

        name_entry.focus()

    def _cancel_add_department(self):
        """Piilottaa lisää osasto syötekentän.
        """
        self._add_department_frame.destroy()
        self._add_department_frame = None
        self._status_label.config(text="")

    def _handle_save_department(self):
        """Handleri, joka vastaa osaston tallentamisesta.
        """
        name = self._department_name_var.get().strip()

        try:
            days = int(self._department_days_var.get())
        except ValueError:
            self._status_label.config(text="Error: days must be a number")
            return

        if not name:
            self._status_label.config(text="Error: department name required")
            return

        try:
            department_service.create_department(
                store_id=self._store.store_id,
                name=name,
                check_days_before=days
            )

            self._status_label.config(text="Department created successfully")

            self._cancel_add_department()

            self._load_departments()

        except Exception as e:
            self._status_label.config(text=f"Error: {str(e)}")

    def _load_departments(self):
        """Hakee ja näyttää listauksen osastoista näkymässä.
        """
        for widget in self._departments_frame.winfo_children():
            widget.destroy()

        try:
            departments = department_service.get_departments_by_store(
                self._store.store_id)
        except Exception as e:
            self._status_label.config(text=f"Error loading departments: {e}")
            return

        if not departments:
            ttk.Label(
                self._departments_frame,
                text="No departments yet"
            ).grid(row=0, column=0, sticky="W")
            return

        for i, dept in enumerate(departments):
            label = ttk.Label(
                self._departments_frame,
                text=dept.name,
                font=(None, 12, "bold"),
                cursor="arrow"
            )
            label.grid(row=i, column=0, sticky="W", pady=2)

            label.bind(
                "<Button-1>",
                lambda e, d=dept: self._handle_department_click(d)
            )

    def _handle_department_click(self, department):
        """Handleri, joka vastaa osastonäkymään siirtymisestä, kun osaston nimeä klikataan.

        Args:
            department: Department-olio, joka on näytettävä osasto
        """
        self._show_department_view(self._store, department)
