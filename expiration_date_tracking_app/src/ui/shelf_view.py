from datetime import datetime

from tkinter import ttk, constants, StringVar
from services.user_service import user_service
from services.product_service import product_service


class ShelfView:
    """Näkymä, joka vastaa hyllyn tietojen näyttämisestä ja voi lisätä tuotteita hyllyyn.
    """
    def __init__(self, root, shelf, department, store, show_department_view):
        """Luokan konstruktori, joka luo uuden hylly-näkymän.

        Args:
            root: TKinter-elemnetti, jonka sisään näkymä luodaan.
            shelf: Shelf-olio, jonka näkymä näytetään.
            department: Department-olio, johon näytettävä hylly kuuluu.
            store: Store-olio, kaupppa johon näytettävä hylly kuuluu.
            show_department_view: Kutsuttava-arvo, joka vastaa osaston näkymään siirtymisestä.
        """
        self._root = root
        self._shelf = shelf
        self._department = department
        self._store = store
        self._show_department_view = show_department_view

        self._frame = None
        self._products_frame = None
        self._add_product_frame = None

        self._user = user_service.get_current_user()

        self._initialize()

    def pack(self):
        """Näyttää näkymän.
        """
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Piilottaa näkymän.
        """
        self._frame.destroy()

    def _handle_back(self):
        self._show_department_view(self._store, self._department)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root, padding=20)

        title = ttk.Label(
            self._frame,
            text=f"{self._shelf.name}",
            font=(None, 24, "bold")
        )

        back_button = ttk.Button(
            self._frame,
            text="Back",
            command=self._handle_back
        )

        self._status_var = StringVar()
        self._status_label = ttk.Label(
            self._frame,
            textvariable=self._status_var
        )

        products_title = ttk.Label(
            self._frame,
            text="Products:",
            font=(None, 18, "bold")
        )

        self._products_frame = ttk.Frame(self._frame)
        self._add_product_frame = ttk.Frame(self._frame)

        title.grid(row=0, column=0, sticky="W")
        back_button.grid(row=0, column=2, sticky="E")
        self._status_label.grid(row=1, column=0, sticky="W", pady=5)
        products_title.grid(row=2, column=0, sticky="W", pady=10)
        self._products_frame.grid(
            row=3, column=0, columnspan=2, sticky="W", pady=5)
        self._add_product_frame.grid(row=5, column=0, sticky="W")

        self._products_frame.grid_columnconfigure(0, weight=1)

        if self._can_add_products():
            self._add_product_button = ttk.Button(
                self._frame,
                text="Add product",
                command=self._show_add_product
            )
            self._add_product_button.grid(row=4, column=0, sticky="W", pady=10)

        self._load_products()

    def _load_products(self):
        for widget in self._products_frame.winfo_children():
            widget.destroy()

        try:
            products = product_service.get_tracked_products_for_shelf(
                self._shelf.shelf_id)
        except ValueError as error:
            self._status_var.set(str(error))

        if not products:
            ttk.Label(
                self._products_frame,
                text="No products"
            ).grid(row=0, column=0, sticky="W")
            return

        for i, product in enumerate(products):
            row_frame = ttk.Frame(self._products_frame)
            product_info = product_service.find_product_by_ean(
                product.ean_code)

            name_label = ttk.Label(
                row_frame,
                text=product_info.name,
                font=(None, 14, "bold")
            )

            try:
                formatted_date = datetime.fromisoformat(
                    product.expiration_date).strftime("%d-%m-%Y")
            except ValueError:
                formatted_date = product.expiration_date

            expiration_label = ttk.Label(
                row_frame,
                text=f"Exp: {formatted_date}",
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

            if self._can_add_products():
                delete_button = ttk.Button(
                    row_frame,
                    text="Delete",
                    command=lambda product=product: self._handle_delete_product(
                        product)
                )

                delete_button.grid(row=1, column=2, sticky="E", padx=(5, 0))

            row_frame.grid_columnconfigure(0, weight=1)
            row_frame.grid_columnconfigure(1, weight=1)

            name_label.grid(row=0, column=0, sticky="W", padx=(0, 20))
            expiration_label.grid(row=0, column=1, sticky="E")
            ean_label.grid(row=1, column=0, sticky="W")
            set_date_button.grid(row=1, column=1, sticky="E")

            row_frame.grid(row=i, column=0, sticky="EW", pady=4)

    def _can_add_products(self):
        if not self._user.is_employee():
            return True

        permissions = user_service.get_employee_permissions(self._user.user_id)

        return any(
            p["store_id"] == self._store.store_id and
            p["permission"] in ["manage", "edit"]
            for p in permissions
        )

    def _show_add_product(self):
        for widget in self._add_product_frame.winfo_children():
            widget.destroy()

        ean_label = ttk.Label(
            self._add_product_frame,
            text="EAN-code:"
        )

        self._ean_var = StringVar()
        ean_entry = ttk.Entry(
            self._add_product_frame,
            textvariable=self._ean_var
        )

        add_button = ttk.Button(
            self._add_product_frame,
            text="Add to tracking",
            command=self._handle_add_to_tracking
        )

        ean_label.grid(row=0, column=0, sticky="W")
        ean_entry.grid(row=0, column=1, sticky="W")
        add_button.grid(row=1, column=0, sticky="W")

    def _handle_add_to_tracking(self):
        ean_code = self._ean_var.get().strip()

        try:
            product = product_service.find_product_by_ean(ean_code)

            if product:
                self._show_expiration_form(product)
            else:
                self._show_missing_info_form(ean_code)
        except ValueError as error:
            self._status_var.set(str(error))

    def _show_expiration_form(self, product):
        for widget in self._add_product_frame.winfo_children():
            widget.destroy()

        product_name_label = ttk.Label(
            self._add_product_frame,
            text=f"{product.name}"
        )

        expiration_label = ttk.Label(
            self._add_product_frame,
            text="Expiration date (ddmmyy):"
        )

        self._expiration_var = StringVar()
        self._expiration_entry = ttk.Entry(
            self._add_product_frame,
            textvariable=self._expiration_var
        )

        save_button = ttk.Button(
            self._add_product_frame,
            text="Save",
            command=lambda: self._handle_save_to_tracking(product)
        )

        product_name_label.grid(row=0, column=0, sticky="W")
        expiration_label.grid(row=1, column=0, sticky="W")
        self._expiration_entry.grid(row=1, column=1, sticky="W")
        save_button.grid(row=2, column=0, sticky="W", pady=10)

    def _show_missing_info_form(self, ean_code):
        for widget in self._add_product_frame.winfo_children():
            widget.destroy()

        missing_info_label = ttk.Label(
            self._add_product_frame,
            text="Product info missing"
        )

        ean_label = ttk.Label(
            self._add_product_frame,
            text=f"EAN-code: {ean_code}"
        )

        name_label = ttk.Label(
            self._add_product_frame,
            text="Product name:"
        )

        self._name_var = StringVar()
        name_entry = ttk.Entry(
            self._add_product_frame,
            textvariable=self._name_var
        )

        expiration_label = ttk.Label(
            self._add_product_frame,
            text="Expiration date (dd/mm/yy):"
        )

        self._expiration_var = StringVar()
        self._expiration_entry = ttk.Entry(
            self._add_product_frame,
            textvariable=self._expiration_var
        )

        save_button = ttk.Button(
            self._add_product_frame,
            text="Save",
            command=lambda: self._handle_save_product_and_tracking(ean_code)
        )

        missing_info_label.grid(row=0, column=0, sticky="W")
        ean_label.grid(row=1, column=0, sticky="W")
        name_label.grid(row=2, column=0, sticky="W")
        name_entry.grid(row=2, column=1, sticky="W")
        expiration_label.grid(row=3, column=0, sticky="W")
        self._expiration_entry.grid(row=3, column=1, sticky="W")
        save_button.grid(row=4, column=0, sticky="W", pady=10)

    def _handle_save_product_and_tracking(self, ean_code):
        name = self._name_var.get().strip()
        expiration_date = self._expiration_var.get().strip()

        try:
            product = product_service.add_product_info(
                ean_code,
                name
            )

            self._handle_save_to_tracking(product)

            self._load_products()
            for widget in self._add_product_frame.winfo_children():
                widget.destroy()

        except ValueError as error:
            self._status_var.set(str(error))

    def _handle_save_to_tracking(self, product):
        expiration_date = self._expiration_var.get().strip()

        try:
            product_service.add_tracked_product(
                ean_code=product.ean_code,
                expiration_date=expiration_date,
                shelf_id=self._shelf.shelf_id
            )

            self._load_products()
            for widget in self._add_product_frame.winfo_children():
                widget.destroy()
            self._status_var.set(str(""))

        except ValueError as error:
            self._status_var.set(str(error))

    def _show_set_date_form(self, row_frame, product):
        for widget in row_frame.grid_slaves(row=1, column=1):
            widget.destroy()

        self._expiration_var = StringVar()

        new_date_entry = ttk.Entry(
            row_frame,
            textvariable=self._expiration_var,
            width=10
        )

        save_button = ttk.Button(
            row_frame,
            text="Save",
            command=lambda product=product: self._handle_set_date(product)
        )

        new_date_entry.grid(row=1, column=1, sticky="E")
        save_button.grid(row=1, column=2, sticky="E", padx=(5, 0))

    def _handle_set_date(self, product):
        expiration_date = self._expiration_var.get().strip()

        try:
            product_service.update_tracked_product_date(
                tracked_product_id=product.tracked_product_id,
                new_expiration_date=expiration_date
            )

            self._load_products()
            self._status_var.set(str(""))

        except ValueError as error:
            self._status_var.set(str(error))

    def _handle_delete_product(self, product):
        try:
            product_service.delete_tracked_product(product.tracked_product_id)
            self._load_products()
            self._status_var.set("")

        except ValueError as error:
            self._status_var.set(str(error))
