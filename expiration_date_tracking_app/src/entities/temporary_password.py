import random


class TemporaryPassword():
    """Luokka, joka luo uuden kertakäyttösalasanan
    """

    def __init__(self):
        """Luokan konstruktori, jossa määritelty mahdolliset 
            kertakäyttösalasanan merkkijono-osuudet: "chocolate", "popcycle" tai "marshmallow" 
        """
        self.words = ["chocolate", "popcycle", "marshmallow"]

    def generate_temporary_password(self):
        """Luo uuden kertakäyttösalasanan.

        Returns:
            Merkkijono, joka on uusi salasana: 
            satunnainen merkkijono listalta + kolme satunnaista numeroa.
        """
        word = random.choice(self.words)

        numbers = ''.join(str(random.randint(1, 9)) for i in range(3))

        password = word + numbers

        return password
