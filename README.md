# Päiväyshallintasovellus

**Päiväyshallintasovellus**, jolla voi seurata kaupassa myynnissä olevien tuotteiden *parasta ennen -päiväyksiä* ja hallinnoida niitä. 

## Dokumentaatio
[Vaatimusmäärittely](https://github.com/hannajan/ot-harjoitustyo/blob/master/expiration_date_tracking_app/dokumentaatio/vaatimusmaarittely.md)    
[Työaikakirjanpito](https://github.com/hannajan/ot-harjoitustyo/blob/master/expiration_date_tracking_app/dokumentaatio/tyoaikakirjanpito.md)  
[Changelog](https://github.com/hannajan/ot-harjoitustyo/blob/master/expiration_date_tracking_app/dokumentaatio/changelog.md)  
[Arkkitehtuuri](https://github.com/hannajan/ot-harjoitustyo/blob/master/expiration_date_tracking_app/dokumentaatio/arkkitehtuuri.md)  
[Release](https://github.com/hannajan/ot-harjoitustyo/releases/tag/viikko5)  
[Käyttöohje](https://github.com/hannajan/ot-harjoitustyo/blob/master/expiration_date_tracking_app/dokumentaatio/kayttoohje.md)  


## Asennus

1. Asennus tehdään komennolla:

```bash
poetry install
```
Komennot tulee suorittaa _expiration_date_tracking_app_-hakemiston sisällä

2. Alustus tehdään komennolla:

```bash
poetry run invoke build
```

## Komentorivitoiminnot

### Ohjelman suorittaminen

Sovellus käynnistetään komennolla:

```bash
poetry run invoke start
```

### Testaus

Testit voi suorittaa komennolla:

```bash
poetry run invoke test
```

### Testikattavuusraportti

Testikattavuusraportin saa generoitua komennolla:

```bash
poetry run invoke coverage-report
```

Selaimessa avattava raportti löytyy _index.html_ tiedostosta, joka generoituu _htmlcov_-hakemistoon.  

### Staattinen analyysi

Pylintin saa ajettua komennolla:

```bash
poetry run invoke lint
```

Koodin automaattinen formatointi tehdään komennolla:


```bash
poetry run invoke format
```
