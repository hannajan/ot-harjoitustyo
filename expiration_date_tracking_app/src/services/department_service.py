from entities.department import Department

from repositories.department_repository import (
    department_repository as default_department_repository
)

from repositories.shelf_repository import (
    shelf_repository as default_shelf_repository
)


class DepartmentService:
    """Luokka, joka vastaa osastoon liittyvästä sovelluslogiikasta.
    """
    def __init__(
        self,
        department_repository=default_department_repository,
        shelf_repository=default_shelf_repository
    ):
        """Luokan konstruktori. Luo uuden osaston sovelluslogiikasta vastaavan palvelun.

        Args:
            department_repository:
                DepartmentReposioty-olio, 
                joka vastaa osastoon liittyvistä tietokantaoperaatioista.
            shelf_repository: 
                ShelfRepository-olio,
                joka vastaa hyllyyn liittyvistä tietokantaoperaatioistsa.
        """
        self._department_repository = department_repository
        self._shelf_repository = shelf_repository

    def create_department(self, store_id, name, check_days_before):
        """Luo uuden osaston.

        Args:
            store_id: Merkkijono, joka on sen kaupan id, johon ostato luodaan.
            name: Merkkijono, joka on osaston nimi.
            check_days_before: 
                Kokonaislukuarvo, joka on sääntö kuinka monta päivää
                ennen parasta ennen -päiväystä sovellus nostaa tuotteen
                tarkastettavien listalle.

        Raises:
            ValueError, jos osaston nimeä ei ole annettu argumenttina.
            ValueError, jos check_days_before on negatiivinen kokonaisluku.

        Returns:
            Department-olio, joka on luotu.
        """
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
        """Palauttaa listan kaupan id:n perusteella löydetyistä osastoista.

        Args:
            store_id: Merkkijono, joka on sen kaupan id, jonka osastot palautetaan.

        Returns:
            Lista Department-olioita.
        """
        return self._department_repository.get_by_store(store_id)

    def update_department(self, department):
        """Päivittää osaston tiedot.

        Args:
            department: Department-olio, jossa uudet arvot.
        """

        if not department.name:
            raise ValueError("Department name must be given")

        if not department.check_days_before:
            raise ValueError("check days before must be given")

        self._department_repository.update(department)


department_service = DepartmentService()
