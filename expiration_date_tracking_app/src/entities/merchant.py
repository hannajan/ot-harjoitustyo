from .user import User
from .user_role import UserRole


class Merchant(User):
    """Luokka, joka kuvaa kauppiasta, joka on User-luokasta periytyvä käyttäjätyyppi.
    """

    def __init__(self, username, password, user_id=None):
        """Konstruktori, joka luo uuden kauppiaan.

        Args:
        username: Merkkijono, joka kuvaa kauppiaan käyttäjänimeä.
        password: Merkkjono, joka on kauppiaan salasana.
        user_id: Merkkijono, joka kuvaa käyttäjän yksilöivää id:tä.
        """
        super().__init__(
            username=username,
            password=password,
            role=UserRole.MERCHANT,
            user_id=user_id)
        self.stores = None
        self.employees = None
