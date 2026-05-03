# Vaatimusmäärittely

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
  - [x] salasana on syötettävä kahdesti ja oltava sama ja vähintään 8 merkkiä pitkä
- [x] voi lisätä työntekijälle käyttöoikeudet kauppaan ja poistaa käyttöoikeudet.

#### Kauppias tai työntekijä
- [x] näkee listauksen kaupoista
- [x] voi lisätä _osaston_ kauppaan 
  - [x] voi lisätä _hyllyn_ osastoon
  - [x] voi lisätä _tarkistussäännön_ osastoon, jonka perusteella tuotteita voi tarkastella (esim. 3 päivää ennen)
  - [x] voi muokata osaston tietoja (nimeä, hyllyjä...)
- [x] voi lisätä _tuotteen_ hyllyyn
  - [x] tuotteen yksilöivä id on tuotteen _EAN-koodi_
  - [x] tuotteelle annetaan _nimi_
  - [x] tuotteelle annetaan _parasta ennen -päiväys_
- [x] voi muokata _tuotteen_ parasta ennen -päiväystä, hyllyriviä...
- [x] näkee tarkistussäännön mukaisen listauksen tuotteista, joiden parasta ennen päiväys on tulossa tai mennyt jo
  - [x] listaus näkyy osastonja hyllyittäin ryhmiteltynä
  - [x] voi listauksesta merkitä tuotteelle uuden parasta ennen -päiväyksen


### Jatkokehitysideoita
- Tuotteen tarkistuksen voi ohittaa yhden päivän ajaksi
- Tuotteelle voi määritellä osaston säännöstä poikkeavan _tarkistussäännön_
- Sovellus antaa haluttaessa ilmoituksen/muistutuksen, esim. sähköpostiin jos on tarkistettavia tuotteita
- Yksittäisten tuotteiden tietoja voi hakea ja tarkastella (esim. suoraan skannaamalla EAN-koodi päänäkymästä)
- Tuotteille voi listätä kuvan, joka helpottaa tuotteen etsimistä