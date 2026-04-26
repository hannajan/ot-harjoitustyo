from entities.merchant import Merchant
from entities.employee import Employee
from entities.user_role import UserRole
from entities.temporary_password import TemporaryPassword
from entities.permission import Permission

from repositories.user_repository import (
    user_repository as default_user_repository
)

from repositories.permission_repository import (
    permission_repository as default_permission_repository
)


class UserService:
    """Luokka, joka vastaa käyttöliittymän ja UserRepositoryn välisestä sovelluslogiikasta.
    """

    def __init__(
        self,
        user_repository=default_user_repository,
        permission_repository=default_permission_repository
    ):
        """Luokan konstruktori.

        Args:
            user_repository: 
                UserRepository-olio, joka käyttäjiin liittyvistä 
                tietokantaoperaatioista vastaava luokka.
            permission_repository: 
                PermissionRepository-olio, joka on käyttöoikeuksien 
                tietokantaoperaatiosita vastaava luokka.
        """
        self._user_repository = user_repository
        self._permission_repository = permission_repository
        self._user = None

    def validate_username(self, username):
        """Validoi, että käyttäjänimi on tarpeeksi pitkä ja uniikki.

        Args:
            username: Merkkijono, joka kuvaa käyttäjänimeä.

        Raises:
            ValueError, jos käyttäjänimi on alle 5 merkkiä pitkä.
            ValueError, jos käyttäjänimi on jo olemassa.

        Returns:
            True, jos käyttäjänimen validointi on onnistunut.
        """
        if len(username) < 5:
            raise ValueError("Username must be at least 5 characters long")

        if self._user_repository.find_by_username(username):
            raise ValueError("Username already exists")

        return True

    def validate_password(self, password):
        """Validoi salasanan.

        Args:
            password: Merkkijono, joka kuvaa salasanaa.

        Raises:
            ValueError, jos salasana on alle 8 merkkiä pitkä.

        Returns:
            True, jos salasanan validointi on onnistunut.
        """

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        return True

    def register_merchant(self, username=None, password=None):
        """Rekisteröi kauppiaan sovellukseen.

        Args:
            username: Merkkijono, joka kuvaa käyttäjätunnusta.
            password: Merkkijono, joka kuvaa salasanaa.

        Raises:
            ValueError, jos käyttäjätunnusta tai salasanaa ei ole syötetty.

        Returns:
            User-olio, joka on sovellukseen rekisteröity kauppias.
        """

        if not username or not password:
            raise ValueError("Username or password missing")

        self.validate_username(username)
        self.validate_password(password)

        merchant = Merchant(username, password)
        created_user = self._user_repository.create(merchant)

        return created_user

    def login(self, username=None, password=None):
        """Kirjaa käyttäjän sisään sovellukseen.

        Args:
            username: Merkkijono, joka on syötetty käyttäjätunnus.
            password: Merkkijono, joka on syötetty salasana.

        Raises:
            ValueError, jos käyttäjätunnusta tai salasanaa ei ole syötetty.
            ValueError, jos käyttäjää ei löydy.
            ValueError, jos salasana on väärin.

        Returns:
            _type_: _description_
        """
        if not username or not password:
            raise ValueError("Username or password missing")

        user = self._user_repository.find_by_username(username)

        if not user:
            raise ValueError("Wrong username or password")

        if user.check_password(password):
            self._user = user
            return user

        raise ValueError("Wrong username or password")

    def get_current_user(self):
        """Palauttaa kirautuneen käyttäjän.

        Returns:
            User-olio, joka on kirjautunut käyttäjä.
        """
        return self._user

    def get_user_by_id(self, user_id=None):
        """Palauttaa käyttäjän id:n perusteella.

        Args:
            user_id: Merkkijono, joka on palautettavan käyttäjän id.

        Raises:
            ValueError, jos user_id argumentti puuttuu.

        Returns:
            User-olio.
        """
        if not user_id:
            raise ValueError("User id missing")

        user = self._user_repository.get_user_by_id(user_id)

        return user

    def create_new_employee(self, username=None):
        """Luo uuden työntekijän.

        Args:
            username: Merkkijono, joka kuvaa käyttäjän käyttäjätunnusta.

        Raises:
            ValueError, jos käyttäjän luonti yrittävän käyttän rooli ei ole kauppias.
            ValueError, käyttäjätunnusta ei ole annettu argumenttina.

        Returns:
            Merkkijono, joka on luodun työntekijän kertakäyttösalasana.
        """
        generator = TemporaryPassword()

        current_user = self.get_current_user()
        if not current_user.role == UserRole.MERCHANT:
            raise ValueError("Only merchants can create new employees")

        if not username:
            raise ValueError("Username missing")

        self.validate_username(username)
        password = generator.generate_temporary_password()
        print(password)

        employee = Employee(username, password, current_user.user_id)
        self._user_repository.create(employee)

        return password

    def update_employee_password(self, new_password):
        """Päivittää työntekijän salasanan.

        Args:
            new_password: Merkkijono, joka on uusi salasana.

        Raises:
            ValueError, jos käyttäjä, jonka salasaanaa yritetään päivittää ei ole työntekijä.
            ValueError, jos uusi salasana on alle 8 merkkiä pitkä.
        """
        if self._user.role != UserRole.EMPLOYEE:
            raise ValueError("User role is not employee")

        if not self.validate_password(new_password):
            raise ValueError("New password must be 8 characters long")
        self._user = self._user.set_password(new_password)
        self._user = self._user.set_password_is_temporary_to_false()
        self._user_repository.update_password(
            self._user.user_id,
            self._user.password,
            self._user.password_is_temporary
        )

    def get_employees(self):
        """Palauttaa kirjautuneen käyttäjän työntekijät.

        Returns:
            Lista Employee-olioita.
        """
        current_user = self.get_current_user()
        if not current_user or current_user.role != UserRole.MERCHANT:
            return []

        return self._user_repository.find_all_by_employer_id(current_user.user_id)

    def logout(self):
        """Kirjaa käyttäjän ulos sovelluksesta.
        """
        self._user = None

    def get_employee_store_permission(self, employee_id, store_id):
        """Palauttaa työntekijän käyttöoikeuden tiettyyn yksittäiseen kauppaan.

        Args:
            employee_id: Merkkijono, joka on työntekijän id.
            store_id: Merkkijono, joka on kaupan id.

        Returns:
            Merkkijono, joka on työntekijän käyttöoikeus yksittäiseen kauppaan.
        """
        return self._permission_repository.find_permission(employee_id, store_id)

    def set_employee_store_permission(self, employee_id, store_id, permission):
        """Asettaa työntekijän käyttöoikeuden yksittäiseen kauppaan.

        Args:
            employee_id: Merkkijono, joka on työntekijän id.
            store_id: Merkkijono, joka on kaupan id.
            permission: Merkkijono, joka kuvaa käyttöoikeuden tasoa.
        """
        self._permission_repository.set_permission(
            employee_id, store_id, permission)

    def get_employee_permissions(self, employee_id):
        """Palauttaa kaikki työntekijään liittyvät käyttöoikeudet, jotka antavat katseluoikeuden.

        Args:
            employee_id: Merkkijono, joka on työntekijän id.

        Returns:
            Palauttaa listan, jolle on filteröity katseluoikeun antavat käyttöoikeudet.
        """
        permissions = self._permission_repository.find_permissions_by_employee_id(
            employee_id)

        valid_permissions = [
            permission
            for permission in permissions
            if permission["permission"] != Permission.NOACCESS
        ]

        return valid_permissions


user_service = UserService()
