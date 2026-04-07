# Alustava vaatimusmäärittely

## Sovelluksen tarkoitus
**Päiväyshallintasovellus**, jolla voi seurata kaupassa myynnissä olevien tuotteiden _parasta ennen -päiväyksiä_. 

## Käyttäjät
_Kauppias_, joka voi luoda kaupan, lisätä ja poistaa _työntekijöitä_, joilla on oikeudet hallinnoida kaupan tuotteita sekä käyttää sovelluksen normaaleja päiväyshallinnointitoimintoja.

_Työntekijä_, joka voi käyttää sovelluksen normaaleja toimintoja, kuten lisätä tuotteen päiväysseurannan piiriin ja seurata tuotteiden parasta ennen -päiväyksiä.

Myöhemmin sovellukseen saatetaan vielä lisätä _pääkäyttäjä_, jolla on korkeammat käyttöoikeuden ja voi muun muassa muokata tai poistaa sovellukseen rekisteröityneitä _kauppiaita_.

## Suunnitellut toiminnallisuudet

### Ennen kirjautumista
- [x] _Kauppias_ voi luoda sovellukseen käyttäjätunnuksen.
  - [x] _Työntekijäroolin_ tunnuksia ei voi luoda, vaan ne luo sovellukseen kirjautunut kauppias.
  - [x] Etusivulla on _rekisteröidy_ linkki, jota klikkaamalla aukeaa rekisteröitymislomake.
  -  [x] Käyttäjätunnuksen on oltava uniikki ja vähintään 5 merkkiä pitkä.
  - [x] Salasana on syötettävä kahdesti ja oltava sama ja vähintään 8 merkkiä pitkä
  - [x] Jos rekisteröityminen ei onnistu annetaan virheilmoitus, jossa kerrotaan syy.
- [x] _Kauppias_ tai _työntekijä_ voi kirjautua sisään sovellukseen.
  - [x] Etusivulla on kirjautumislomake, johon syötetään käyttäjätunnus ja salasana.
  - [x] Jos kirjautuminen ei onnistu annetaan virheilmoitus, jossa kerrotaan syy.

### Kirjautumisen jälkeen 
#### Kauppias
- [x] voi luoda kaupan
- [x] voi lisätä työntekijän
  - [x] sovellus luo alustavan salasanan työntekijälle, jonka tulee vaihtaa salasana ensimmäisen kirjautumisen yhteydessä.
- [ ] voi lisätä työntekijälle käyttöoikeudet kauppaan ja poistaa käyttöoikeudet.

#### Kauppias tai työntekijä
- [ ] voi lisätä _osaston_ kauppaan 
  - [ ] voi lisätä _hyllyn_ osastoon
  - [ ] voi lisätä _hyllyrivin_ hyllyyn (ei pakollinen, oletuksena yksi hyllyrivi)
  - [ ] voi lisätä _tarkistussäännön_ osastoon, jonka perusteella tuotteita voi tarkastella (esim. 3 päivää ennen)
  - [ ] voi muokata osaston tietoja (nimeä, hyllyjä...)
- [ ] voi lisätä _tuotteen_ hyllyyn
  - [ ] tuotteen yksilöivä id on tuotteen _EAN-koodi_
  - [ ] tuotteelle annetaan _nimi_
  - [ ] tuotteelle annetaan _parasta ennen -päiväys_
  - [ ] tuotteelle voi määritellä hyllyrivin
  - [ ] tuotteelle voi määritellä osaston säännöstä poikkeavan _tarkistussäännön_
- [ ] voi muokata _tuotteen_ tietoja: nimeä, ean-koodia, parasta ennen -päiväystä, hyllyriviä...
- [ ] näkee tarkistussäännön mukaisen listauksen tuotteista, joiden parasta ennen päiväys on tulossa tai mennyt jo
  - [ ] listaus näkyy osastoittain ja hyllyittäin (ja hyllyriveittäin, jos määritelty)
  - [ ] voi listauksesta merkitä tuotteelle uuden parasta ennen -päiväyksen
  - [ ] voi ohittaa tuotteen yhden päivän ajaksi

### Jatkokehitysideoita
- Sovellus antaa haluttaessa ilmoituksen/muistutuksen, esim. sähköpostiin jos on tarkistettavia tuotteita
- Yksittäisten tuotteiden tietoja voi hakea ja tarkastella (esim. suoraan skannaamalla EAN-koodi päänäkymästä)
- Tuotteille voi listätä kuvan, joka helpottaa tuotteen etsimistä