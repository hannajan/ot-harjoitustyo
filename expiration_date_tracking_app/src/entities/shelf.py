import uuid


class Shelf:
    """Luokka, joka kuvaa hyllyä.
    """

    def __init__(self, department_id, name, is_default=False, shelf_id=None):
        """Luokan konstruktori, joka luo uuden hyllyn.

        Args:
            department_id: Merkkijono, joka viittaa osaston id:hen, johon hylly kuuluu.
            name: Merkkijono, joka kuvaa hyllyn nimeä.
            is_default: 
              Boolean, joka kuvaa onko hylly osaston luomisen 
              yhteydessä luotu oletusarvohylly.
            shelf_id: Merkkijono, joka on hyllyn yksilöivä id.
        """
        self.shelf_id = shelf_id or str(uuid.uuid4())
        self.department_id = department_id
        self.name = name
        self.is_default = is_default
