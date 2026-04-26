from tkinter import Tk
from ui.create_merchant_view import CreateMerchantView
from ui.login_view import LoginView
from ui.home_view import HomeView
from ui.employees_view import EmployeesView
from ui.change_password_view import ChangePasswordView
from ui.employee_view import EmployeeView
from ui.store_view import StoreView
from ui.department_view import DepartmentView
from services.user_service import user_service


class UI:
    """Luokka, joka vastaa sovelluksen käyttöliittymässä näytettävästä näkymästä.
    """

    def __init__(self, root):
        """Luokan konstruktori, joka

        Args:
            root (_type_): _description_
        """
        self._root = root
        self._current_view = None

    def start(self):
        """Käynnistää käyttöliittymän
        """
        self._show_login_view()

    def _hide_current_view(self):
        """Piilottaa nykyisen näkymän.
        """
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_login_view(self):
        """Näyttää kirjautumisnäkymän
        """
        self._hide_current_view()

        self._current_view = LoginView(
            self._root,
            self._after_login_success,
            self._show_create_merchant_view
        )

        self._current_view.pack()

    def _show_home_view(self):
        """Näyttää aloitusnäkymän
        """
        self._hide_current_view()

        self._current_view = HomeView(
            self._root,
            self._show_employees_view,
            self._show_login_view,
            self._show_store_view
        )
        self._current_view.pack()

        self._current_view._frame.update_idletasks()

        user = user_service.get_current_user()
        self._current_view.set_user(user)

    def _show_create_merchant_view(self):
        """Näyttää kauppiaan rekisteröintinäkymän
        """
        self._hide_current_view()

        self._current_view = CreateMerchantView(
            self._root,
            self._show_login_view
        )

        self._current_view.pack()

    def _show_employees_view(self):
        """Näyttää työntekijöiden hallinointi-näkymän
        """
        self._hide_current_view()

        self._current_view = EmployeesView(
            self._root,
            self._show_home_view,
            self._show_employee_view
        )

        self._current_view.pack()

    def _show_employee_view(self, employee):
        """Näyttää yksittäisen työntekijän hallinnointi-näkymän

        Args:
            Employee-olio, joka on näytettävä työntekijä.
        """
        self._hide_current_view()

        self._current_view = EmployeeView(
            self._root,
            employee,
            self._show_employees_view
        )

        self._current_view.pack()

    def _show_change_password_view(self):
        """Näyttää salasananvaihtonäkymän
        """
        self._hide_current_view()

        self._current_view = ChangePasswordView(
            self._root,
            self._show_home_view
        )

        self._current_view.pack()

    def _after_login_success(self):
        """Näyttää kertakäyttösalasanalla kirjautumisen jälkeen salasananvaihtonäkymän, muutoin aloitusnäkymän
        """
        user = user_service.get_current_user()

        if user.password_is_temporary:
            self._show_change_password_view()
        else:
            self._show_home_view()

    def _show_store_view(self, store):
        """Näyttää kaupan hallinnointi-näkymän

        Args:
            store: Store-olio, joka on näytettävä kauppa.
        """
        self._hide_current_view()

        user = user_service.get_current_user()

        self._current_view = StoreView(
            self._root,
            store,
            user,
            self._show_home_view,
            self._show_department_view
        )

        self._current_view.pack()

    def _show_department_view(self, store, department):
        """Näyttää yksittäisen osaston hallinnointiin liittyvän näkymän

        Args:
            store: Store-olio, joka kuvaa kaupaa, jonka osasto näytetään.
            department: Department-olio, joka on näytettävä osasto.
        """
        self._hide_current_view()

        self._current_view = DepartmentView(
            self._root,
            department,
            user_service.get_current_user(),
            store,
            self._show_store_view
        )

        self._current_view.pack()
