from .user import User
from .user_role import UserRole


class Employee(User):
    """Luokka, joka kuvaa työntekijää, joka on User-luokasta periytyvä käyttäjätyyppi.
    """

    def __init__(self, username, password, employer_id, user_id=None):
        """Luokan konstruktori, joka luo uuden työntekijän.

        Args:
            username: Merkkijono, joka kuvaa työntekijän käyttäjätunnusta.
            password: Merkkijono, joka kuvaa työntekijän salasanaa.
            employer_id: 
                Merkkijono, joka on kauppiaaseen viittavaa id. 
                Työntekijän luonut ja omistava kauppias.
            user_id: Merkkijono, joka on käyttäjän yksilöivä id.
        """
        super().__init__(
            username=username,
            password=password,
            role=UserRole.EMPLOYEE,
            user_id=user_id
        )
        self.employer_id = employer_id
        self.password_is_temporary = True

    def set_password_is_temporary_to_false(self):
        """Muuttaa "salasana on väliaikainen" booleanin Falseksi, 
            kun kertakirjautumissalasana on vaihdettu.

        Returns:
            Työntekijä-olion.
        """
        self.password_is_temporary = False

        return self
