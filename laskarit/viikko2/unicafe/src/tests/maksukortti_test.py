import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_luodun_kortin_saldo_on_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(200)

        self.assertEqual(self.maksukortti.saldo_euroina(), 12.0)

    def test_saldo_vahenee_oikein_jos_rahaa_on_tarpeeksi(self):
        self.maksukortti.ota_rahaa(300)

        self.assertEqual(self.maksukortti.saldo_euroina(), 7.0)

    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(3000)

        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_ota_rahaa_palauttaa_true_jos_rahat_riittavat(self):   
        self.assertEqual(self.maksukortti.ota_rahaa(250), True)

    def test_ota_rahaa_palauttaa_false_jos_rahat_eivat_riita(self):   
        self.assertEqual(self.maksukortti.ota_rahaa(1700), False)

    def test_string_metodi_palauttaa_oikean_tulosteen(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")