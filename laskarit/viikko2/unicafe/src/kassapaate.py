class Kassapaate:
    TYPE_EDULLINEN = "edullinen"
    TYPE_MAUKAS = "maukas"

    def __init__(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0
        self.edullinen_hinta = 240
        self.maukas_hinta = 400

    def rahat_riittaa(self, lounastyyppi, maksu):
        if lounastyyppi == self.TYPE_EDULLINEN: 
            return True if maksu >= self.edullinen_hinta else False
        if lounastyyppi == self.TYPE_MAUKAS:
            return True if maksu >= self.maukas_hinta else False
        return False
    
    def paivita_kassan_saldo(self, maara):
        self.kassassa_rahaa = self.kassassa_rahaa + maara

    def vaihtorahamaara(self, hinta, maksu):
        return maksu - hinta
    
    def syo_kateisella(self, maksu, hinta, lounastyyppi):
        if self.rahat_riittaa(lounastyyppi, maksu):
            self.paivita_kassan_saldo(hinta)
            if lounastyyppi == self.TYPE_EDULLINEN:
                self.edulliset += 1
            elif lounastyyppi == self.TYPE_MAUKAS:
                self.maukkaat += 1
            return self.vaihtorahamaara(hinta, maksu)
        return maksu
    
    def syo_kortilla(self, kortti, hinta, tyyppi):
        if kortti.ota_rahaa(hinta):
            if tyyppi == self.TYPE_EDULLINEN:
                self.edulliset += 1
            elif tyyppi == self.TYPE_MAUKAS:
                self.maukkaat += 1
            return True
        return False

    def syo_edullisesti_kateisella(self, maksu):
        return self.syo_kateisella(maksu, self.edullinen_hinta, self.TYPE_EDULLINEN)

    def syo_maukkaasti_kateisella(self, maksu):
        return self.syo_kateisella(maksu, self.maukas_hinta, self.TYPE_MAUKAS)

    def syo_edullisesti_kortilla(self, kortti):
        return self.syo_kortilla(kortti, self.edullinen_hinta, self.TYPE_EDULLINEN)

    def syo_maukkaasti_kortilla(self, kortti):
        return self.syo_kortilla(kortti, self.maukas_hinta, self.TYPE_MAUKAS)

    def lataa_rahaa_kortille(self, kortti, summa):
        if summa >= 0:
            kortti.lataa_rahaa(summa)
            self.paivita_kassan_saldo(summa)

    def kassassa_rahaa_euroina(self):
        return self.kassassa_rahaa / 100
