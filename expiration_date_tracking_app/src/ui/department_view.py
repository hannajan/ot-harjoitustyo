from tkinter import ttk, StringVar
from services.user_service import user_service
from services.shelf_service import shelf_service


class DepartmentView:
    def __init__(self, root, department, user, store, show_store_view):
        self._root = root
        self._department = department
        self._user = user
        self._store = store
        self._show_store_view = show_store_view
        self._rename_frame = None

        self._frame = None
        self._add_shelf_frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill="both", expand=True)

    def destroy(self):
        self._frame.destroy()

    def _handle_back(self):
        self._show_store_view(self._store)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root, padding=20)

        title = ttk.Label(
            self._frame,
            text=f"{self._department.name}",
            font=(None, 20, "bold")
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
          font=(None, 14, "bold")
      )

        self._shelves_frame = ttk.Frame(self._frame)

        title.grid(row=0, column=0, sticky="W")
        back_button.grid(row=0, column=1, sticky="E")
        self._status_label.grid(row=1, column=0, columnspan=2, sticky="W", pady=5)
        shelves_title.grid(row=2, column=0, columnspan=2, sticky="W", pady=(10, 0))
        self._shelves_frame.grid(row=3, column=0, columnspan=2, sticky="W", pady=5)
        self._shelves_frame.grid(row=3, column=0, columnspan=2, sticky="W", pady=10)

        self._load_shelves()

        if self._can_manage():
          self._add_shelf_button = ttk.Button(
              self._frame,
              text="Add shelf",
              command=self._show_add_shelf
          )
          self._add_shelf_button.grid(row=4, column=0, sticky="W", pady=10)

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
            label = ttk.Label(
                self._shelves_frame,
                text=f"{shelf.name}" + (" (default)" if shelf.is_default else ""),
                font=(None, 12, "bold"),
                cursor="arrow"
            )

            label.grid(row=i, column=0, sticky="W", pady=2)

            label.bind(
                "<Button-1>",
                lambda e, s=shelf: self._handle_shelf_click(s)
            )

    def _handle_shelf_click(self, shelf):
      if not self._can_manage():
          self._status_label.config(text="No permission to edit shelf")
          return

      self._show_rename_shelf(shelf)

    def _show_add_shelf(self):
        if self._add_shelf_frame:
            return

        self._add_shelf_frame = ttk.Frame(self._frame)
        self._add_shelf_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="W")

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
      self._rename_frame.grid(row=5, column=0, columnspan=2, sticky="W", pady=10)

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