import uuid


class Department:
    """Luokka, joka kuvaa kaupan osastoa.
    """

    def __init__(self, store_id, name, check_days_before, department_id=None):
        """Luokan, konstruktori, joka luo uuden osaston.

        Args:
            store_id: Merkkijono, joka viittaa kaupan id:hen. Kauppa, johon osasto kuuluu.
            name: Merkkijono, joka kuvaa osaston nimeä.
            check_days_before: 
              Kokonaisluku, joka kuvaa sääntöä, jonka perusteella päiväykset tarkistetaan. 
              Kuinka monta päivää ennen.
            department_id: Merkkijono, joka on osaston yksilöivä id.
        """

        self.department_id = department_id or str(uuid.uuid4())
        self.store_id = store_id
        self.name = name
        self.check_days_before = check_days_before
