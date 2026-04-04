from tkinter import ttk, constants, StringVar
from services.user_service import user_service
from services.store_service import store_service


class HomeView():
    def __init__(self, root):
        self._root = root
        self._frame = None
        self._user = None
        self._stores = []
        self._add_store_shown = False

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root, padding=20)

        self._title = ttk.Label(
            master=self._frame, text="Welcome", font=(None, 32, "bold"))
        self._status_label = ttk.Label(
            master=self._frame, text="Loading user...")
        self._stores_frame = ttk.Frame(master=self._frame)
        self._add_store_button = ttk.Button(
            master=self._frame, text="Add store", command=self._show_add_store_entry)

        self._title.grid(row=0, column=0, sticky="NW", pady=(0, 10))
        self._status_label.grid(row=1, column=0, sticky="NW", pady=(0, 10))
        self._stores_frame.grid(row=2, column=0, sticky="NW")
        self._frame.rowconfigure(3, weight=1)
        self._add_store_button.grid(row=4, column=0, sticky=constants.EW, pady=(5,0))

    def set_user(self, user):
        self._user = user
        self._status_label.config(text=f"Logged in as {user.username}")
        self._populate_stores()

    def _populate_stores(self):
        for store in self._stores:
            store.destroy()
        self._stores = []

        stores = store_service.get_stores_by_owner(self._user.user_id)

        if not stores:
            print("No stores")
        else:
            for i, store in enumerate(stores):
                store_button = ttk.Button(
                    master=self._stores_frame,
                    text=store.name,
                    command=lambda: print(f"{store.name} button pressed")
                )

                store_button.grid(row=i, column=0, sticky="NW", pady=2)
                self._stores.append(store_button)

    def _handle_save_store(self):
        store_name = self._store_name_var.get().strip()

        if not store_name:
            raise ValueError("Store name must be given.")
        
        try:
            store_service.create_store(store_name)
            self._add_store_frame.destroy()
            self._add_store_shown = False
            self._add_store_button.grid(row=4, column=0, sticky=constants.EW, pady=(5,0))
            self._populate_stores()
        except Exception as e:
            error_message = str(e)
            self._root.after(
                0, lambda msg=error_message: self._status_label.config(text=f"Error: {msg}"))

    def _show_add_store_entry(self):
        if self._add_store_shown:
            return
        self._add_store_shown = True

        self._add_store_button.grid_remove()

        self._add_store_frame = ttk.Frame(self._frame)

        self._store_name_label = ttk.Label(
            self._add_store_frame,
            text="Store name"
        )
        self._store_name_var = StringVar()
        self._store_name_entry = ttk.Entry(self._add_store_frame, textvariable=self._store_name_var)
        self._save_store_button = ttk.Button(
            master=self._add_store_frame,
            text="Save",
            command=self._handle_save_store
        )

        self._add_store_frame.grid(row=4, column=0, columnspan=2, sticky=constants.EW, pady=(5,0))
        
        self._store_name_label.grid(row=0,column=0, sticky=constants.EW, padx=(0,2))
        self._store_name_entry.grid(row=0, column=1, sticky=constants.EW, padx=(0, 100))
        self._save_store_button.grid(row=0, column=2, sticky=constants.EW, padx=(5,0))

        self._store_name_entry.focus()

