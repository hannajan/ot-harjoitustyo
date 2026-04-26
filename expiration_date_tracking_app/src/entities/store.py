import uuid


class Store:
    """Luokka, joka kuvaa kauppaa.
    """

    def __init__(self, name, owner_id, store_id=None):
        """Luokan konstruktori, joka luo uuden kaupan.

        Args:
            name: Merkkijono, joka kuvaa kaupan nimeä.
            owner_id: Merkkijono, joka viittaa kaupan omistajavan käyttäjän id:hen.
            store_id: Merkkijono, joka on kaupan yksilöivä id.
        """
        self.store_id = store_id or str(uuid.uuid4())
        self.name = name
        self.owner_id = owner_id
