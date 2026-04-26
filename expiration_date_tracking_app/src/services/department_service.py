from entities.department import Department

from repositories.department_repository import (
    department_repository as default_department_repository
)

from repositories.shelf_repository import (
    shelf_repository as default_shelf_repository
)


class DepartmentService:
    def __init__(
        self,
        department_repository=default_department_repository,
        shelf_repository=default_shelf_repository
    ):
        self._department_repository = department_repository
        self._shelf_repository = shelf_repository

    def create_department(self, store_id, name, check_days_before):
        if not name:
            raise ValueError("Department name must be given")

        if check_days_before < 0:
            raise ValueError("Check days must be positive integer")

        department = Department(
            store_id=store_id,
            name=name,
            check_days_before=check_days_before
        )

        self._department_repository.create(department)

        self._shelf_repository.create_default_shelf(department.department_id)

        return department

    def get_departments_by_store(self, store_id):
        return self._department_repository.get_by_store(store_id)


department_service = DepartmentService()
