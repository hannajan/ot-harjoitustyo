from tkinter import ttk, constants, StringVar
from services.store_service import store_service
from services.user_service import user_service

# generoitu tekoälyllä

class EmployeeView:
    def __init__(self, root, employee, show_employees_view):
        self._root = root
        self._employee = employee
        self._show_employees_view = show_employees_view

        self._user = user_service.get_current_user()

        self._frame = None
        self._rows = []
        self._role_vars = {}

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root, padding=20)

        title = ttk.Label(
            master=self._frame,
            text=f"Employee: {self._employee.username}",
            font=(None, 20, "bold")
        )

        back_button = ttk.Button(
            master=self._frame,
            text="Back",
            command=self._show_employees_view
        )

        self._stores_frame = ttk.Frame(master=self._frame)

        title.grid(row=0, column=0, sticky="W", pady=(0, 10))
        back_button.grid(row=0, column=1, sticky=constants.E)
        self._stores_frame.grid(row=1, column=0, columnspan=2, sticky="W")

        self._stores_frame.columnconfigure(0, weight=1)

        self._populate_stores()

    def _populate_stores(self):
        for row in self._rows:
            for widget in row:
                widget.destroy()
        self._rows = []

        stores = store_service.get_stores_by_owner(self._user.user_id)

        ROLES = ["noaccess", "view", "edit", "manage"]

        for i, store in enumerate(stores):
            store_label = ttk.Label(
                master=self._stores_frame,
                text=store.name,
                font=(None, 12, "bold")
            )

            current_role = user_service.get_employee_store_role(
                self._employee.user_id,
                store.store_id
            )

            role_var = StringVar(
                value=current_role if current_role else "view")
            self._role_vars[store.store_id] = role_var

            role_menu = ttk.OptionMenu(
                self._stores_frame,
                role_var,
                role_var.get(),
                *ROLES,
                command=lambda value, s=store: self._handle_role_change(
                    s, value)
            )

            store_label.grid(row=i, column=0, sticky="W", pady=4, padx=(0, 10))
            role_menu.grid(row=i, column=1, sticky="W")

            self._rows.append((store_label, role_menu))

    def _handle_role_change(self, store, role):
        try:
            user_service.set_employee_store_role(
                self._employee.user_id,
                store.store_id,
                role
            )
        except Exception as e:
            print("Error:", e)
