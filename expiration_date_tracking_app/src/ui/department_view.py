from datetime import datetime

from tkinter import ttk, StringVar
from services.user_service import user_service
from services.shelf_service import shelf_service
from services.department_service import department_service
from services.product_service import product_service

from ui.components.hover_label import HoverLabel

# Luokan pohja generoitu alunperin tekoälyllä ja täydennetty omalla koodilla


class DepartmentView:
    """Näkymä, joka näyttää ja jossa voi hallinnoida osaston tietoja.
    """

    def __init__(self, root, department, user, store, show_store_view, show_shelf_view):
        """Luokan konstruktori.

        Args:
            root: TKinter-elemnetti, jonka sisään näkymä luodaan.
            department: Department-olio, jonka näkymä näytetään.
            user: User-olio, joka on käyttäjä.
            store: Store-olio, joka on kauppa, johon osasto kuuluu.
            show_store_view: Kutsuttava-arvo, joka vastaa kauppanäkymään siirtymisestä.
            show_shelf_view: Kutsuttava-arvo, joka vastaa hyllynäkymään siirtymisestä.
        """
        self._root = root
        self._department = department
        self._user = user
        self._store = store
        self._show_store_view = show_store_view
        self._show_shelf_view = show_shelf_view

        self._frame = None
        self._add_shelf_frame = None
        self._rename_frame = None
        self._edit_days_frame = None

        self._save_days_button = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän.
        """
        self._frame.pack(fill="both", expand=True)

    def destroy(self):
        """Piilottaa näkymän.
        """
        self._frame.destroy()

    def _handle_back(self):
        self._show_store_view(self._store)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root, padding=20)

        title = ttk.Label(
            self._frame,
            text=f"{self._department.name}",
            font=(None, 24, "bold")
        )

        self._days_label = ttk.Label(
            self._frame,
            text=f"Check days before: {self._department.check_days_before}"
        )

        back_button = ttk.Button(
            self._frame,
            text="Back",
            command=self._handle_back
        )

        self._status_label = ttk.Label(self._frame, text="")

        shelves_title = ttk.Label(
            self._frame,
            text="Shelves:",
            font=(None, 20, "bold")
        )

        self._shelves_frame = ttk.Frame(self._frame)

        self._products_to_check_frame = ttk.Frame(self._frame)

        title.grid(row=0, column=0, sticky="W")
        back_button.grid(row=0, column=1, sticky="E")
        self._status_label.grid(
            row=1, column=0, columnspan=2, sticky="W", pady=5)
        self._days_label.grid(row=2, column=0, columnspan=2, sticky="W")
        shelves_title.grid(row=3, column=0, columnspan=2,
                           sticky="W", pady=(10, 0))
        self._shelves_frame.grid(
            row=4, column=0, columnspan=2, sticky="W", pady=5)
        self._products_to_check_frame.grid(
            row=6, column=0, columnspan=2, sticky="W", pady=(20, 0)
        )

        self._load_shelves()

        if self._can_manage():
            self._add_shelf_button = ttk.Button(
                self._frame,
                text="Add shelf",
                command=self._show_add_shelf
            )

            self._edit_days_button = ttk.Button(
                self._frame,
                text="Edit",
                command=self._show_edit_days
            )
            self._edit_days_button.grid(row=2, column=2, sticky="E")
            self._add_shelf_button.grid(row=5, column=0, sticky="W", pady=10)

    def _can_manage(self):
        if not self._user.is_employee():
            return True

        permissions = user_service.get_employee_permissions(self._user.user_id)

        return any(
            p["store_id"] == self._department.store_id and p["permission"] == "manage"
            for p in permissions
        )

    def _load_shelves(self):
        for widget in self._shelves_frame.winfo_children():
            widget.destroy()

        try:
            shelves = shelf_service.get_shelves_by_department(
                self._department.department_id
            )
        except Exception as e:
            self._status_label.config(text=f"Error loading shelves: {e}")
            return

        if not shelves:
            ttk.Label(
                self._shelves_frame,
                text="No shelves"
            ).grid(row=0, column=0, sticky="W")
            return

        for i, shelf in enumerate(shelves):
            shelf_frame = ttk.Frame(self._shelves_frame)
            shelf_frame.grid(row=i, column=0, sticky="W", pady=5)

            shelf_title = HoverLabel(
                master=shelf_frame,
                text=f"{shelf.name}" +
                (" (default)" if shelf.is_default else ""),
                command=lambda s=shelf: self._handle_shelf_click(s)
            )

            shelf_title.grid(row=0, column=0, sticky="W", pady=3)

            if self._can_manage():
                ttk.Button(
                    shelf_frame,
                    text="Edit name",
                    command=lambda s=shelf: self._show_rename_shelf(s)
                ).grid(row=0, column=1, padx=8, sticky="W")

            products = product_service.get_products_to_check_by_shelf(
                shelf.shelf_id)

            for j, product in enumerate(products):
                product_info = product_service.find_product_by_ean(
                    product.ean_code
                )

                row_frame = ttk.Frame(shelf_frame)
                row_frame.grid(row=j + 1, column=0, columnspan=2,
                               sticky="EW", padx=(20, 0))

                name_label = ttk.Label(
                    row_frame,
                    text=product_info.name,
                    font=(None, 14, "bold")
                )

                try:
                    formatted_date = datetime.fromisoformat(
                        product.expiration_date
                    ).strftime("%d-%m-%Y")
                except ValueError:
                    formatted_date = product.expiration_date

                date_label = ttk.Label(
                    row_frame,
                    text=formatted_date,
                    font=(None, 14, "bold")
                )

                ean_label = ttk.Label(
                    row_frame,
                    text=product.ean_code,
                    font=(None, 12)
                )

                set_date_button = ttk.Button(
                    row_frame,
                    text="Set date",
                    command=lambda row_frame=row_frame, product=product: self._show_set_date_form(
                        row_frame, product)
                )

                row_frame.grid_columnconfigure(0, weight=1)
                row_frame.grid_columnconfigure(1, weight=1)

                name_label.grid(row=0, column=0, sticky="W")
                date_label.grid(row=0, column=1, sticky="E")
                ean_label.grid(row=1, column=0, sticky="W")
                set_date_button.grid(row=1, column=2, sticky="E", padx=(10, 0))

    def _handle_shelf_click(self, shelf):
        self._show_shelf_view(shelf, self._department, self._store)

    def _show_add_shelf(self):
        if self._add_shelf_frame:
            return

        self._add_shelf_frame = ttk.Frame(self._frame)
        self._add_shelf_frame.grid(
            row=4, column=0, columnspan=2, pady=10, sticky="W")

        ttk.Label(
            self._add_shelf_frame,
            text="Shelf name"
        ).grid(row=0, column=0, sticky="W")

        self._shelf_name_var = StringVar()
        name_entry = ttk.Entry(
            self._add_shelf_frame,
            textvariable=self._shelf_name_var,
            width=30
        )
        name_entry.grid(row=0, column=1, padx=5)

        save_button = ttk.Button(
            self._add_shelf_frame,
            text="Save",
            command=self._handle_save_shelf
        )
        save_button.grid(row=1, column=0, pady=5, sticky="W")

        cancel_button = ttk.Button(
            self._add_shelf_frame,
            text="Cancel",
            command=self._cancel_add_shelf
        )
        cancel_button.grid(row=1, column=1, pady=5, sticky="W")

        name_entry.focus()

    def _cancel_add_shelf(self):
        self._add_shelf_frame.destroy()
        self._add_shelf_frame = None
        self._status_label.config(text="")

    def _handle_save_shelf(self):
        name = self._shelf_name_var.get().strip()

        if not name:
            self._status_label.config(text="Error: shelf name required")
            return

        try:
            shelf_service.create_shelf(
                department_id=self._department.department_id,
                name=name
            )

            self._status_label.config(text="Shelf created")

            self._cancel_add_shelf()
            self._load_shelves()

        except Exception as e:
            self._status_label.config(text=f"Error: {str(e)}")

    def _show_rename_shelf(self, shelf):
        if self._rename_frame is not None:
            return

        self._rename_frame = ttk.Frame(self._frame)
        self._rename_frame.grid(
            row=5, column=0, columnspan=2, sticky="W", pady=10)

        label = ttk.Label(
            self._rename_frame,
            text="New name"
        )
        label.grid(row=0, column=0, sticky="W")

        self._rename_var = StringVar(value=shelf.name)

        entry = ttk.Entry(
            self._rename_frame,
            textvariable=self._rename_var,
            width=30
        )
        entry.grid(row=0, column=1, padx=5)

        def save():
            try:
                shelf_service.rename_shelf(
                    shelf,
                    self._rename_var.get().strip()
                )
                self._rename_frame.destroy()
                self._rename_frame = None
                self._refresh_shelves()
            except Exception as e:
                self._status_label.config(text=str(e))

        ttk.Button(
            self._rename_frame,
            text="Save",
            command=save
        ).grid(row=1, column=0, pady=5, sticky="W")

        entry.focus()

    def _refresh_shelves(self):
        if hasattr(self, "_rename_frame") and self._rename_frame:
            self._rename_frame.destroy()
            self._rename_frame = None

        self._load_shelves()

    # generoitu koodi alkaa
    # muokattu toimivaksi
    def _show_edit_days(self):
        self._edit_days_button.grid_remove()

        self._days_var = StringVar(
            value=str(self._department.check_days_before)
        )

        self._days_entry = ttk.Entry(
            self._frame,
            textvariable=self._days_var,
            width=10
        )

        self._days_entry.grid(row=2, column=2, sticky="W")

        def save():
            try:
                new_check_days_before = int(self._days_var.get())

                self._department.check_days_before = new_check_days_before

                department_service.update_department(self._department)

                self._days_label.config(
                    text=f"Check days before: {new_check_days_before}"
                )

                self._days_entry.destroy()
                self._days_entry = None
                self._save_days_button.destroy()

                self._edit_days_button.grid()
                self._status_label.config(text="")

            except ValueError:
                self._status_label.config(text="Must be number")

        self._save_days_button = ttk.Button(
            self._frame,
            text="Save",
            command=save
        )
        self._save_days_button.grid(row=2, column=3, sticky="E")

    def _show_set_date_form(self, row_frame, product):
        for widget in row_frame.grid_slaves(row=1, column=1):
            widget.destroy()

        expiration_var = StringVar()

        entry = ttk.Entry(
            row_frame,
            textvariable=expiration_var,
            width=10
        )

        def save():
            try:
                product_service.update_tracked_product_date(
                    tracked_product_id=product.tracked_product_id,
                    new_expiration_date=expiration_var.get().strip()
                )

                self._load_shelves()

            except ValueError as error:
                self._status_label.config(text=str(error))

        save_button = ttk.Button(
            row_frame,
            text="Save",
            command=save
        )

        entry.grid(row=1, column=1, sticky="E")
        save_button.grid(row=1, column=2, sticky="E", padx=(5, 0))
    # generoitu koodi päättyy
