from database_connection import get_database_connection
from entities.department import Department


def get_department_by_row(row):
    if row:
        return Department(
            department_id=row["department_id"],
            store_id=row["store_id"],
            name=row["name"],
            check_days_before=row["check_days_before"]
        )
    return None


class DepartmentRepository:
    """Luokka, joka vastaa osastoihin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection: Connection-olio, joka on tietokantayhteys.
        """
        self._connection = connection

    def create(self, department: Department):
        """Tallentaa osaston tietokantaan.

        Args:
            department: Osasto, joka tallennetaan tietokantaan.
        """

        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO departments (department_id, store_id, name, check_days_before) "
            "VALUES (?, ?, ?, ?) ",
            (department.department_id,
             department.store_id,
             department.name,
             department.check_days_before))
        self._connection.commit()

    def get_by_store(self, store_id):
        """Palauttaa kaupan osastot.

        Args:
            store_id: Merkkijono, joka on sen kaupan id, jonka osastot palautetaan.

        Returns:
            Lista Department-olioita.
        """

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT department_id, store_id, name, check_days_before "
            "FROM departments "
            "WHERE store_id = ? ",
            (store_id,))

        rows = cursor.fetchall()
        return [get_department_by_row(row) for row in rows]
    
    def delete_all(self):
        """Poistaa kaikki osastot tietokannasta.
        """
        cursor = self._connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("DELETE FROM departments")
        self._connection.commit()


department_repository = DepartmentRepository(get_database_connection())
