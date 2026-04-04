from entities.store import Store

from repositories.store_repository import (
    store_repository as default_store_repository
)

from services.user_service import user_service


class StoreService:
    def __init__(self, store_repository=default_store_repository):
        self._store_repository = store_repository

    def create_store(self, name):
        if not name:
            raise ValueError("Store name must be given.")

        if len(name) < 3:
            raise ValueError("Store name must be at least 3 characters long.")

        user = user_service.get_current_user()
        if not user:
            raise ValueError("User not found. Store must have owner.")

        store = Store(name, owner_id=user.user_id)
        return self._store_repository.create(store)

store_service = StoreService()
