import uuid


class TrackedProduct:
    """Luokka, joka kuvaa hyllyssä olevaa päiväysseurannan piiriin lisättyä tuotetta
    """

    def __init__(
            self,
            *,
            tracked_product_id=None,
            ean_code,
            expiration_date,
            shelf_id,
            check_days_before=None):
        """Luokan konstruktori, joka luo uuden päiväysseurattavan tuotteen

        Args:
            id: Merkkijono, joka on seurannassa olevan tuotteen yksilöivä id
            ean_code: Merkkijono, joka on tuotteen yksilöivä id ja EAN-koodi
            expiration_date: 
                Date-olio, joka on tuotteen seuraava vastaan tuleva parasta ennen -päiväys 
            shelf_id: Merkkijono, joka on sen hyllyn id, jolla tuote sijaitsee
            check_days_before: 
                Integer, kuinka monta päivää ennen tuote tarkistetaan, 
                jos tarkistussääntö poikkeaa osaston säännöstä.
                Oletusarvoisesti None.
        """
        self.tracked_product_id = tracked_product_id or str(uuid.uuid4())
        self.ean_code = ean_code
        self.expiration_date = expiration_date
        self.shelf_id = shelf_id
        self.check_days_before = check_days_before
