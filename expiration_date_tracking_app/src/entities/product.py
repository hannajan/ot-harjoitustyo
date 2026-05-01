
class Product:
    """Luokka, joka kuvaa tuotetta.
    """

    def __init__(self, ean_code, name):
        """Luokan konstruktori, joka luo uuden tuotteen

        Args:
            ean_code: Merkkijono, joka on tuotteen EAN-koodi ja yksilöivä id
            name: Merkkijono, joka on tuotteen nimi
        """
        self.ean_code = ean_code
        self.name = name
