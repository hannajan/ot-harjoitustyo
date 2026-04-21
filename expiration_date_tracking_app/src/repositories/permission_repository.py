from database_connection import get_database_connection
from entities.permission import Permission

class PermissionRepository:
    def __init__(self, connection):
        self._connection = connection


    def find_permission(self, employee_id, store_id):
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