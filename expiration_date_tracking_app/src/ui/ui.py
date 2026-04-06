from tkinter import Tk
from ui.create_merchant_view import CreateMerchantView
from ui.login_view import LoginView
from ui.home_view import HomeView
from ui.employees_view import EmployeesView
from ui.change_password_view import ChangePasswordView
from services.user_service import user_service


class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_login_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_login_view(self):
        self._hide_current_view()

        self._current_view = LoginView(
            self._root,
            self._after_login_success,
            self._show_create_merchant_view
        )

        self._current_view.pack()

    def _show_home_view(self):
        self._hide_current_view()

        self._current_view = HomeView(
            self._root,
            self._show_employees_view,
            self._show_login_view
        )
        self._current_view.pack()

        self._current_view._frame.update_idletasks()

        user = user_service.get_current_user()
        self._current_view.set_user(user)

    def _show_create_merchant_view(self):
        self._hide_current_view()

        self._current_view = CreateMerchantView(
            self._root,
            self._show_login_view
        )

        self._current_view.pack()

    def _show_employees_view(self):
        self._hide_current_view()

        self._current_view = EmployeesView(
            self._root,
            self._show_home_view
        )

        self._current_view.pack()

    def _show_change_password_view(self):
        self._hide_current_view()

        self._current_view = ChangePasswordView(
            self._root,
            self._show_home_view
        )

        self._current_view.pack()

    def _after_login_success(self):
        user = user_service.get_current_user()

        if user.password_is_temporary:
            self._show_change_password_view()
        else:
            self._show_home_view()
