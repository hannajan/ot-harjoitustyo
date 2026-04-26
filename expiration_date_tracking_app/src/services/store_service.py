from entities.store import Store

from repositories.store_repository import (
    store_repository as default_store_repository
)

from services.user_service import (
    user_service as default_user_service
)


class StoreService:
    """Luokka, joka vastaa käyttöliittymän ja StoreRepositoryn välisestä sovelluslogiikasta.
    """

    def __init__(
        self,
        store_repository=default_store_repository,
        user_service=default_user_service
    ):
        """Luokan konstruktori.

        Args:
            store_repository: 
                StoreRepository-olio, joka on kauppoihin liittyvistä 
                tietokantaoperaatiosita vastaava luokka.
            user_service: 
                UserService-olio, joka on käyttäjiin liittyvästä 
                sovelluslogiikasta vastaava luokka.
        """
        self._store_repository = store_repository
        self._user_service = user_service

    def create_store(self, name=None):
        """Luo kaupan.

        Args:
            name: Merkkijono, joka kuvaa kaupan nimeä.

        Raises:
            ValueError, jos kaupan nimeä ei ole syötetty.
            ValueError, jos kaupan nimi on alle 3 merkkiä pitkä.
            ValueError, jos kirjautunutta käyttäjää ei löydy.

        Returns:
            Store-olio, joka on luotu.
        """
        if not name:
            raise ValueError("Store name must be given")

        if len(name) < 3:
            raise ValueError("Store name must be at least 3 characters long.")

        user = self._user_service.get_current_user()
        if not user:
            raise ValueError("User not found. Store must have owner.")

        store = Store(name, owner_id=user.user_id)
        return self._store_repository.create(store)

    def get_stores_by_owner(self, owner_id):
        """Palauttaa kaikki kauppiaan id:n perusteella löytyvät kaupat.

        Args:
            owner_id: Merkkijono, joka kuvaa kauppiaan käyttäjä id:tä.

        Returns:
            Lista Store-olioita.
        """
        return self._store_repository.find_all_by_owner_id(owner_id)

    def get_store_by_id(self, store_id):
        """Palauttaa kaupan id:n perusteella.

        Args:
            store_id: Merkkijono, joka on sen kaupan id, joka palautetaan.

        Returns:
            Store-olio.
        """
        return self._store_repository.find_by_id(store_id)


store_service = StoreService()
