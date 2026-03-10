import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
  def setUp(self):
    self.kassa = Kassapaate()
    self.kortti = Maksukortti(1000)

  def test_luodun_kassan_rahamaara_on_oikein(self):
    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)

  def test_luodun_kassan_myytyjen_lounaiden_maara_on_nolla(self):
    self.assertEqual(self.kassa.edulliset, 0)

  def test_kassan_rahamaara_kasvaa_oikein_kun_ostetaan_kateisella_edullinen_lounas(self):
    self.kassa.syo_edullisesti_kateisella(250)

    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1002.4)

  def test_kassa_antaa_vaihtorahan_oikein_kun_syodaan_edullisesti(self):
    self.assertEqual(self.kassa.syo_edullisesti_kateisella(250), 10)

  def test_kassan_rahamaara_kasvaa_oikein_kun_ostetaan_kateisella_maukas_lounas(self):
    self.kassa.syo_maukkaasti_kateisella(500)

    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1004.0)

  def test_kassa_antaa_vaihtorahan_oikein_kun_syodaan_maukkaasti(self):
    self.assertEqual(self.kassa.syo_maukkaasti_kateisella(500), 100)

  def test_myytyjen_edullisten_lounaiden_maara_kasvaa_oikein_kateisella(self):
    self.kassa.syo_edullisesti_kateisella(250)

    self.assertEqual(self.kassa.edulliset, 1)

  def test_myytyjen_maukkaiden_lounaiden_maara_kasvaa_oikein_kateisella(self):
    self.kassa.syo_maukkaasti_kateisella(500)

    self.assertEqual(self.kassa.maukkaat, 1)

  def test_kassan_rahamaara_ei_muutu_jos_kateinen_ei_riita_edulliseen_lounaaseen(self):
    self.kassa.syo_edullisesti_kateisella(100)

    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)

  def test_kassan_rahamaara_ei_muutu_jos_kateinen_ei_riita_maukaaseen_lounaaseen(self):
    self.kassa.syo_maukkaasti_kateisella(300)

    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)

  def test_kaikki_vaihtorahat_palautetaan_jos_kateinen_ei_riita_edulliseen_lounaaseen(self):
    self.assertEqual(self.kassa.syo_edullisesti_kateisella(100), 100)

  def test_kaikki_vaihtorahat_palautetaan_jos_kateinen_ei_riita_maukkaaseen_lounaaseen(self):
    self.assertEqual(self.kassa.syo_maukkaasti_kateisella(300), 300)

  def test_myytyjen_lounaiden_maara_ei_muutu_jos_kateinen_ei_riita_edulliseen_lounaaseen(self):
    self.kassa.syo_edullisesti_kateisella(50)

    self.assertEqual(self.kassa.edulliset, 0)

  def test_myytyjen_lounaiden_maara_ei_muutu_jos_kateinen_ei_riita_maukkaaseen_lounaaseen(self):
    self.kassa.syo_maukkaasti_kateisella(220)

    self.assertEqual(self.kassa.maukkaat, 0)

  def test_korttiosto_palauttaa_true_edullista_lounasta_ostettaessa(self):
    self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.kortti), True)

  def test_korttiosto_palauttaa_true_maukasta_lounasta_ostettaessa(self):
    self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.kortti), True)

  def test_kassa_veloittaa_oikean_summan_kortilta_edullista_lounasta_ostettaessa(self):
    self.kassa.syo_edullisesti_kortilla(self.kortti)

    self.assertEqual(self.kortti.saldo_euroina(), 7.6)

  def test_kassa_veloittaa_oikean_summan_kortilta_maukasta_lounasta_ostettaessa(self):
    self.kassa.syo_maukkaasti_kortilla(self.kortti)

    self.assertEqual(self.kortti.saldo_euroina(), 6.0)

  def test_myytyjen_edullisten_lounaiden_maara_kasvaa_kortilla_maksettaessa(self):
    self.kassa.syo_edullisesti_kortilla(self.kortti)

    self.assertEqual(self.kassa.edulliset, 1)

  def test_myytyjen_maukkaiden_lounaiden_maara_kasvaa_kortilla_maksettaessa(self):
    self.kassa.syo_maukkaasti_kortilla(self.kortti)

    self.assertEqual(self.kassa.maukkaat, 1)

  def test_kassa_palauttaa_false_jos_kortilla_ei_tarpeeksi_rahaa_edulliseen_lounaaseen(self):
    kortti = Maksukortti(239)

    self.assertEqual(self.kassa.syo_edullisesti_kortilla(kortti), False)

  def test_kassa_palauttaa_false_jos_kortilla_ei_tarpeeksi_rahaa_maukkaaseen_lounaaseen(self):
    kortti = Maksukortti(390)

    self.assertEqual(self.kassa.syo_maukkaasti_kortilla(kortti), False)

  def test_kortilta_ei_veloiteta_rahaa_jos_raha_ei_riita_edulliseen_lounaaseen(self):
    kortti = Maksukortti(239)
    self.kassa.syo_edullisesti_kortilla(kortti)

    self.assertEqual(kortti.saldo_euroina(), 2.39)

  def test_kortilta_ei_veloiteta_rahaa_jos_raha_ei_riita_maukkaaseen_lounaaseen(self):
    kortti = Maksukortti(390)
    self.kassa.syo_maukkaasti_kortilla(kortti)

    self.assertEqual(kortti.saldo_euroina(), 3.90)

  def test_myytyjen_edullisten_lounaiden_maara_ei_muutu_jos_raha_ei_riita_kortilla(self):
    kortti = Maksukortti(239)
    self.kassa.syo_edullisesti_kortilla(kortti)

    self.assertEqual(self.kassa.edulliset, 0)

  def test_myytyjen_maukkaiden_lounaiden_maara_ei_muutu_jos_raha_ei_riita_kortilla(self):
    kortti = Maksukortti(380)
    self.kassa.syo_maukkaasti_kortilla(kortti)

    self.assertEqual(self.kassa.maukkaat, 0)

  def test_kassan_rahamaara_ei_muutu_kun_ostetaan_edullinen_lounas_kortilla(self):
    self.kassa.syo_edullisesti_kortilla(self.kortti)

    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)

  def test_kassan_rahamaara_ei_muutu_kun_ostetaan_maukas_lounas_kortilla(self):
    self.kassa.syo_maukkaasti_kortilla(self.kortti)

    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)

  def test_ladatessa_korttia_kortin_saldo_kasvaa(self):
    self.kassa.lataa_rahaa_kortille(self.kortti, 500)

    self.assertEqual(self.kortti.saldo_euroina(), 15.0)

  def test_ladatessa_korttia_kassan_rahamaara_kasvaa(self):
    self.kassa.lataa_rahaa_kortille(self.kortti, 500)

    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1005.0)

  def test_negatiivisen_saldon_lataus_ei_muuta_kortin_saldoa(self):
    self.kassa.lataa_rahaa_kortille(self.kortti, -100)

    self.assertEqual(self.kortti.saldo_euroina(), 10.0)

  def test_negatiivisen_saldon_lataus_ei_muuta_kassan_rahamaaraa(self):
    self.kassa.lataa_rahaa_kortille(self.kortti, -100)

    self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)