from database_connection import get_database_connection
from entities.permission import Permission


class PermissionRepository:
    """Luokka, joka vastaa käyttöoikeuksiin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection: Connection-olio, joka on tietokantayhteys.
        """
        self._connection = connection

    def find_permission(self, employee_id, store_id):
        """Palauutaa työntekijän kauppakohtaisen käyttöoikeuden.

        Args:
            employee_id: 
                Merkkijono, joka on sen työntekijän yksilöivä id,
                jonka käyttöoikeus palautetaan.
            store_id:
                Merkkijono, joka on sen kaupan id,
                jonka työntekijäkohtainen käyttöoikeus palautetaan.

        Returns:
            Permission, jos on olemassa, muussa tapauksessa "no access".
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT permission "
            "FROM employee_store_permissions "
            "WHERE employee_id = ? AND store_id = ? ",
            (employee_id, store_id)
        )

        row = cursor.fetchone()

        if row:
            return row["permission"]

        return Permission.NOACCESS

    def set_permission(self, employee_id, store_id, permission):
        """Päivittää käyttöoikeuden tietokantaan.

        Args:
            employee_id: 
                Merkkijono, joka on työntekijän id, 
                jonka käyttöoikeus lisätään tietokantaan.
            store_id: 
                Merkkijono, joka on sen kaupan id,
                jota käyttöoikeus koskee.
            permission: Merkkijono, joka kuvaa käyttöoikeuden tasoa.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO employee_store_permissions (employee_id, store_id, permission) "
            "VALUES (?, ?, ?) "
            "ON CONFLICT(employee_id, store_id) "
            "DO UPDATE SET permission = excluded.permission ",
            (employee_id, store_id, permission)
        )

        self._connection.commit()

    def find_permissions_by_employee_id(self, employee_id):
        """Palauttaa käyttöoikeudet, jotka työntekijällä on.

        Args:
            employee_id: Merkkijono, joka on sen työhntekijän id, jonka käyttöoikeudet palautetaan.

        Returns:
            Lista työntekijän käyttöoikeuksista.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * "
            "FROM employee_store_permissions "
            "WHERE employee_id = ? ",
            (employee_id,)
        )

        rows = cursor.fetchall()

        return [dict(row) for row in rows]


permission_repository = PermissionRepository(get_database_connection())
