from entities.shelf import Shelf

from repositories.shelf_repository import (
    shelf_repository as default_shelf_repository
)


class ShelfService:
    def __init__(self, shelf_repository=default_shelf_repository):
        self._shelf_repository = shelf_repository

    def create_shelf(self, department_id, name):
        if not name:
            raise ValueError("Shelf name must be given")

        shelf = Shelf(
            department_id=department_id,
            name=name,
            is_default=False
        )

        self._shelf_repository.create(shelf)

    def get_shelves_by_department(self, department_id):
        return self._shelf_repository.get_shelves_by_department(department_id)

    def rename_shelf(self, shelf, new_name):
        if not new_name:
            raise ValueError("Name must be given")

        shelf.name = new_name
        shelf.is_default = False

        self._shelf_repository.update(shelf)

        return shelf


shelf_service = ShelfService()
