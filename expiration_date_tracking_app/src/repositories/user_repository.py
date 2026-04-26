from database_connection import get_database_connection

from entities.merchant import Merchant
from entities.employee import Employee
from entities.user_role import UserRole


def get_user_by_row(row):
    if row:
        if row["role"] == UserRole.MERCHANT:
            user = Merchant(
                user_id=row["user_id"],
                username=row["username"],
                password=row["password"],
            )
            return user
        if row["role"] == UserRole.EMPLOYEE:
            user = Employee(
                user_id=row["user_id"],
                username=row["username"],
                password=row["password"],
                employer_id=row["employer_id"]
            )
            user.password_is_temporary = bool(row["password_is_temporary"])
            return user
    return None


class UserRepository:
    """Luokka, joka vastaa käyttäjään liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection: Connection-olio, joka on tietokantayhteys.
        """

        self._connection = connection

    def create(self, user):
        """Tallentaa käyttäjän tietokantaan.

        Args:
            user: User-olio, joka kuvaa tallennettavaa käyttäjää.

        Returns:
            Tallennettu käyttäjä-olio.
        """

        cursor = self._connection.cursor()

        password_is_temporary = int(user.password_is_temporary) if hasattr(
            user, 'password_is_temporary') else 0
        employer_id = None if user.role == UserRole.MERCHANT else user.employer_id

        cursor.execute(
            "INSERT INTO users "
            "(user_id, username, password, role, password_is_temporary, employer_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                user.user_id,
                user.username,
                user.password,
                user.role,
                password_is_temporary,
                employer_id
            )
        )

        self._connection.commit()

        return user

    def delete_all(self):
        """Poistaa kaikki käyttäjät tietokannasta.
        """
        cursor = self._connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("DELETE FROM users")
        self._connection.commit()

    def get_all(self):
        """Palauttaa kaikki käyttäjät.

        Returns:
            Lista käyttäjä-olioista.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()

        return list(map(get_user_by_row, rows))

    def find_by_username(self, username):
        """Palauttaa käyttäjänimen perusteella löydetyn käyttäjän.

        Args:
            username: Käyttäjätunnus, jota vastaava käyttäjä palautetaan.

        Returns:
            Palauttaa User-olion, jos käyttäjä on olemassa, muussa tapauksessa None.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        row = cursor.fetchone()

        return get_user_by_row(row)

    def get_user_by_id(self, user_id):
        """Palauttaa id:n perusteella löydetyn käyttäjän.

        Args:
            user_id: Merkkijono, joka on sen käyttäjän id, joka palautetaan.

        Returns:
            User-olion, jos on olemassa, muussa tapauksessa None.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )

        row = cursor.fetchone()

        return get_user_by_row(row)

    def update_password(self, user_id, new_password, password_is_temporary):
        """Päivittää käyttäjän salasanan.

        Args:
            user_id: Merkkijono, joka on käyttäjän id, jonka salasana päivitetään.
            new_password: Merkkijono, joka on uusi päivitettävä salasana.
            password_is_temporary: Boolean arvo, joka kuvaa sitä onko kertakäyttösalasana vaihdettu.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "UPDATE users "
            "SET password = ?, password_is_temporary = ? "
            "WHERE user_id = ?",
            (new_password, int(password_is_temporary), user_id)
        )

        self._connection.commit()

    def find_all_by_employer_id(self, employer_id):
        """Palauttaa kaikki kauppiaan id:n perusteella löydetyt työntekijät.

        Args:
            employer_id: Kauppiaan id, jonka työntekijät palautetaan.

        Returns:
            Lista Työntekijä-olioita, jotka ovat kauppiaalla töissä.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE employer_id = ?",
            (employer_id,)
        )
        rows = cursor.fetchall()

        return [get_user_by_row(dict(row)) for row in rows]


user_repository = UserRepository(get_database_connection())
