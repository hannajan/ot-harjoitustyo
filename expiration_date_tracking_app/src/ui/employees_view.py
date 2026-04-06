from tkinter import ttk, constants, StringVar, messagebox
from services.user_service import user_service

# tämän luokan pohja on generoitu tekoälyllä, johon lisätty päälle omaa koodia


class EmployeesView:
    def __init__(self, root, show_home_view):
        self._root = root
        self._show_home_view = show_home_view
        self._frame = None
        self._employees_frame = None
        self._employees = []
        self._add_employee_shown = False

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root, padding=20)

        title = ttk.Label(
            master=self._frame,
            text="Employees",
            font=(None, 24, "bold")
        )

        back_button = ttk.Button(
            master=self._frame,
            text="Back",
            command=self._handle_back
        )

        self._employees_frame = ttk.Frame(master=self._frame)
        self._add_employee_button = ttk.Button(
            master=self._frame,
            text="Add employee",
            command=self._show_add_employee_entry
        )

        title.grid(row=0, column=0, sticky="W", pady=(0, 10))
        back_button.grid(row=0, column=1, sticky=constants.NE, pady=(0, 10))
        self._employees_frame.grid(row=1, column=0, sticky="NW")
        self._add_employee_button.grid(
            row=2, column=0, sticky=constants.EW, pady=(5, 0))

        self._populate_employees()

    def _handle_back(self):
        self._show_home_view()

    def _show_add_employee_entry(self):
        if self._add_employee_shown:
            return

        self._add_employee_shown = True
        self._add_employee_button.grid_remove()

        self._add_employee_frame = ttk.Frame(self._frame)
        self._username_var = StringVar()

        self._username_label = ttk.Label(
            self._add_employee_frame,
            text="Username"
        )
        self._username_entry = ttk.Entry(
            self._add_employee_frame,
            textvariable=self._username_var
        )
        self._save_employee_button = ttk.Button(
            self._add_employee_frame,
            text="Save",
            command=self._handle_save_employee
        )

        self._add_employee_frame.grid(
            row=2, column=0, sticky=constants.EW, pady=(5, 0))
        self._username_label.grid(row=0, column=0, sticky=constants.EW)
        self._username_entry.grid(row=0, column=1, sticky=constants.EW)
        self._save_employee_button.grid(row=0, column=2, padx=(5, 0))

        self._username_entry.focus()

    def _handle_save_employee(self):
        username = self._username_var.get().strip()

        if not username:
            return

        try:
            temp_password = user_service.create_new_employee(username)

            messagebox.showinfo(
                "Temporary password",
                f"Employee created.\nUsername: {username}\nOne-time login password: {temp_password}",
                icon="info"
            )

            self._add_employee_frame.destroy()
            self._add_employee_shown = False
            self._add_employee_button.grid()

            self._populate_employees()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _populate_employees(self):
        for emp in self._employees:
            emp.destroy()
        self._employees = []

        employees = user_service.get_employees()
        for i, emp in enumerate(employees):
            label = ttk.Label(
                self._employees_frame,
                text=emp.username,
                font=(None, 12, "bold")
            )
            label.grid(row=i, column=0, sticky="W", pady=2)
            self._employees.append(label)
