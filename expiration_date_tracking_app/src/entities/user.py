import uuid
import bcrypt
from .user_role import UserRole


def _hash_password(password):
    """Hashaa salasanan.

    Args:
        password: Merkkijono, joka kuvaa käyttäjän salasanaa.

    Raises:
        Nostaa ValueError, jos salasanaa ei ole syötetty

    Returns:
        Merkkijonon, joka on salasana-hash.
    """
    if password:
        if isinstance(password, str):
            if not password.startswith("$2b$"):
                return bcrypt.hashpw(password.encode("utf-8"),
                                     bcrypt.gensalt()).decode("utf-8")
        if isinstance(password, bytes):
            if not password.startswith(b"$2b$"):
                return bcrypt.hashpw(password, bcrypt.gensalt())
        return password

    raise ValueError("Password must be provided")


class User:
    """Luokka joka kuvaa käyttäjää.
    """

    def __init__(self, username, role, password=None, user_id=None):
        """Luokan konstruktori, joka luo uuden käyttäjän.

        Args:
            username: 
                Merkkijono, joka on käyttäjän uniikki käyttäjätunnus, 
                jolla sovellukseen kirjaudutaan
            role: 
                Merkkijono. Joko kauppias tai työntekijä, 
                määrittää sovelluksen käyttäjän roolin ja oikeudet
            password: 
                Merkkijono, joka kuvaa salasanaa, 
                jolla käyttäjä kirjautuu sovellukseen.
            user_id: Merkkijono, joka on käyttäjän yksilöivä id.

        Raises:
            ValueError: 
                Antaa virheilmoituksen, 
                jos käyttäjän rooli ei ole kauppais tai työntekijä.
        """

        self.user_id = user_id or str(uuid.uuid4())
        self.username = username
        self.password_is_temporary = False
        self.employer_id = None
        self.password = _hash_password(password)

        if role in (UserRole.EMPLOYEE, UserRole.MERCHANT):
            self.role = role
        else:
            raise ValueError("Invalid role")

    def check_password(self, password):
        """Tarkistaa salasanan.

        Args:
            password: Merkkijono, joka kuvaa sisäänkirjautumisessa syötettyä salasanaa

        Returns:
            True, jos syötetty salasana on oikein, muutoin False.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def set_password(self, new_password):
        """Vaihtaa salasanan.

        Args:
            new_password: Merkkijono, joka on käyttäjän syöttämä uusi salasana.

        Returns:
            Käyttäjä-olion, jonka salasana on uusi salasana.
        """
        self.password = bcrypt.hashpw(new_password.encode("utf-8"),
                                      bcrypt.gensalt()).decode("utf-8")
        return self

    def is_employee(self):
        """Tarkistaa onko käyttäjän rooli työntekijä.

        Returns:
            True, jos käyttäjän rooli on työntekijä, muutoin False.
        """
        return self.role == UserRole.EMPLOYEE
