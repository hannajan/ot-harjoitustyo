# Arkkitehtuurikuvaus

## Rakenne

Sovelluksen rakenne noudattaa kerrosarkkitehtuuria.

Pakkaus _entities_ sisältää luokat, jotka kuvaavat sovelluksen käyttämiä olioita.  
Pakkaus _repositories_ sisältää koodin, joka vastaa tietokantaoperaatioista.  
Pakkaus _services_ sisältää koodin, joka vastaa käyttöliittymän ja repositorioiden välisestä sovelluslogiikasta.  
Pakkaus _ui_ sisältää käyttöliittymään liittyvän koodin.  

## Käyttöliittymä

Käyttöliittymässä on _ui.py_, joka vastaa siitä, mikä näkymä käyttäjälle näytetään. Näkymiä ovat:
  - Sisäänkirjautumisnäkymä
  - Kauppiaan rekisteröintinäkymä
  - Koti-näkymä
  - Salasanan vaihtonäkymä
  - Työntekijöiden listaus ja hallintointinäkymä
  - Työntekijän käyttöoikeuksien hallinnointinäkymä
  - Kauppanäkymä, jossa osastojen listaus ja hallinnointi
  - Osastonäkymä, jossa hyllyjen listaus ja hallinnointi, sekä listaus tarkistettavista tuotteista ja merkitä uuden parasta ennen -päiväyksen
  - Hyllynäkymä, jossa voi hallinnoida seurannassa olevia tuotteita ja niiden parasta ennen -päiväyksiä

Jokaisella näkymällä on oma luokka, joka vastaa näkymästä ja käyttöliitymän koodi on eriytetty muusta sovelluslogiikasta. Käyttöliittymä kutsuu _service_-luokkien metodeja.

## Sovelluslogiikka

Sovelluksesta löytyvät olio-luokat:
  - User
  - Merchant
  - Employee
  - Store
  - Permission
  - Department
  - Shelf
  - Product
  - TrackedProduct

_Merchant_ ja _Employee_ ovat _User_-luokat periviä olioita, jotka määrittävät millaisia käyttöoikeuksia kyseisillä käyttäjillä voi olla sovelluksessa. _Permission_-luokka määrittelee tarkemmin _Employee_-olioiden käyttöoikeuksien tason. 

_Store_-luokka kuvaa kauppaa, jonka osastoja kuvaa _Department_-luokka, joilla on tarkistussääntö, kuinka monta päivää etukäteen parasta ennen -päiväyksiä tarkistetaan. _Shelf_-luokka, on osaston hyllyjä kuvaava luokka helpottamaan tuotteiden paikantamista osaston sisällä.


_Product_-luokka kuvaa tuotetta, jolla on EAN-koodi ja nimi. _TrackedProduct_-luokka kuvaa seurannassa olevaa tuotetta, sillä samaa tuotetta voi olla useilla eri hyllyillä/osastoilla ja eri parasta ennen -päiväyksillä.

### Luokkakaavio

```mermaid
classDiagram
  class User {
    user_id,
    username,
    password_is_temporary,
    employer_id,
    password,
    role
  }
  class Merchant {
    stores
    employees  
  }
  class Employee {
 
  }
  class Store {
    store_id,
    name,
    owner_id
  }
  class Department {
    department_id,
    store_id,
    name,
    check_days_before
  }
  class Shelf {
    shelf_id,
    department_id,
    name,
    is_default
  }
  class Product {
    ean_code,
    name
  }
  class TrackedProduct {
    tracked_product_id,
    ean_code,
    expiration_date,
    shelf_id,
    check_days_before
  }
  Merchant --|> User
  Employee --|> User
  Merchant "1" -- "*" Store
  Merchant "1" -- "*" Employee
  Store "1" -- "*" Department
  Department "1" -- "1..*" Shelf
  Employee ..> Store : Permission
  Shelf "1" -- "*" TrackedProduct
  note for Product "contains product info tied to EAN-code"
  TrackedProduct .. Product

```

## Tietojen pysyväistallennus

Sovellus käyttää SQLite-tietokantaa, joka tallentaa sovelluksen tarvitseman data käyttäjän omalle koneelle. Pakkauksen _repositories_ luokat vastaavat tietokantaan tallennuksesta ja muista tietokantaoperaatioista. Pakkauksen _service_ luokat kutsuvat _repositories_ pakkauksen luokkia ja käyttöliittymä on eryitetty niistä niin, että kommunikointi repositorioiden ja käyttöliittymän välillä tapahtuu vain _service_ luokkien kautta.

Sovellus tallentaa tiedot SQLite-tietokantataululuihin:
  - users
  - stores
  - employee_store_permissions
  - departments
  - shelves
  - products
  - tracked_products

## Päätoiminnallisuudet

### Kauppiaan rekisteröinti

Kauppias voi rekisteröityä sovellukseen syötämällä käyttäjätunnuksen (uniikki) ja salasanan. Sovellus pyytää myös vahvistamaan salasanan ja sen tulee täsmätä. 

### Käyttäjän sisäänkirjautuminen

Käyttäjä voi kirjautua sisään syöttämällä käyttäjänimensä ja salasanansa niille varattuihin syötekenttiin.

### Työntekijän luominen Employees näkymässä

Kauppias voi luoda uusia työntekijäroolin omaavia käyttäjiä. Työntekijän luominen etenee seuraavasti:

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant UserService
  participant TemporaryPassword
  participant UserRepository
  User->>UI: click "Save" button
  UI->>UserService: create_new_employee("maijamehilainen")
  UserService->>UserService: get_current_user()
  UserService->>UserService: check current_user is merchant
  UserService->>UserService: validate_username("maijamehilainen")
  UserService->>TemporaryPassword: generate_temporary_password()
  TemporaryPassword-->>UserService: "popcycle123"
  create participant maijamehilainen
  UserService->>maijamehilainen: Employee("maijamehilainen", "popcycle123", current_user.user_id)
  UserService->>UserRepository: create(maijamehilainen)
  UserRepository->>UserRepository: save in database
  UserRepository-->>UserService: user
  UserService-->>UI: "popcycle123"
  UI->>UI: show temporary password in messagebox
  UI->>UI: populate_employees()
```

Käyttäjä syöttää työntekijälle _käyttäjänimen_ ja painaa "Save"-painiketta. UI:n tapahtumankäsittelijä kutsuu `UserService`-luokan sovelluslogiikkaa, joka vastaa uuden työntekijän luonnista. `UserService` validoi syötteen ja luo uuden _kertakäyttösalasanan_. Tämän jälkeen `UserService` pyytää `UserRepository`-luokkaa tallentamaan uuden käyttäjän tietokantaan. `UserService` palauttaa UI:lle _kertakäyttösalasanan_ ja UI näyttää salasanan käyttäjälle ilmoitusikkunassa. UI kutsuu omaa tapahtumankäsittelijäänsä, joka lataa uuden päivitetyn listan työntekijöistä, joka näytetään käyttäjälle.


### Kaupan luominen

Kauppias voi luoda kauppoja. Työtekijät näkymässä kauppias voi antaa yksittäisille työntekijöille käyttöoikeuksia kauppaan: katseluoikeus, muokkausoikeus ja hallinnointioikeus.

Katseluoikeudella voi tarkastella parasta ennen -päiväyksiä ja merkitä niitä. Muokkasoikeudella voi lisätä ja poistaa tuotteita hyllyistä. Hallinnointioikeudella voi muokata kaupan osasto- ja hyllyrakennetta.

### Osaston luominen

Kaupan näkymän kautta voi luoda uuden osaston. Osastolle luodaan oletusarvoisesti yksi hylly. Sen nimeä voi muokata.

### Hyllyn luominen

Osaston näkymässä voi luoda osastolle uusia hyllyjä ja muokata niiden nimiä.

### Tuotteen lisääminen seurantaan

Hyllyn näkymässä voi lisätä tuotteita seurantaan niiden _parasta ennen-päiväyksen_ perusteella. Tuotteen lisäämisen yhteydessä sovellus pyytää lisäämään tuotteen tiedot (nimen), jos tuotetta ei löydy tietokannasta. Tässä tapauksessa tuotteen lisääminen etenee hyllyn näkymästä seuraavasti:


```mermaid
sequenceDiagram
  actor User
  participant UI
  participant ProductService
  participant ProductRepository
  participant TrackedProductRepository
  User->>UI: click "Add product" button
  User->>UI: types in EAN-code and clicks "Add to tracking" button
  UI->>ProductService: find_product_by_ean("6408430033904")
  ProductService->>ProductRepository: get_by_ean_code("6408430033904")
  ProductRepository-->>ProductService: None
  ProductService-->>UI: None'
  UI->>UI: _show_missing_info_form("6408430033904")
  User->>UI: clicks "Save" button
  UI->>ProductService: add_product_info("6408430033904", "Valio pizzajuustoraaste 150g")
  create participant pizzajuustoraaste
  ProductService ->> pizzajuustoraaste: Product("6408430033904", "Valio pizzajuustoraaste 150g")
  Pizzajuustoraaste -->> ProductService: pizzajuustoraaste
  ProductService ->> ProductRepository: create(pizzajuustoraaste)
  ProductRepository ->> ProductRepository: saves pizzajuustoraaste to database
  ProductRepository -->> ProductService: pizzajuustoraaste
  ProductService -->> UI: pizzajuustoraaste
  UI ->> UI: _handle_save_to_tracking(pizzajuustoraaste)
  UI ->> ProductService: add_tracked_product("6408430033904","130526",shelf_id)
  create participant tracked_pizzajuustoraaste
  ProductService ->> tracked_pizzajuustoraaste: TrackedProduct("6408430033904","130526",shelf_id)
  tracked_pizzajuustoraaste -->> ProductService: tracked_pizzajuustoraaste
  ProductService->>TrackedProductRepository: create(tracked_pizzajuustoraaste)
  TrackedProductRepository->>TrackedProductRepository: saves tracked_pizzajuustoraaste to database
  TrackedProductRepository-->>ProductService: tracked_pizzajuustoraaste
  ProductService-->>UI: tracked_pizzajuustoraaste
  UI->>UI: _load_products()
  UI-->>User: shows updated list of tracked products
```

Käyttäjä painaa "Add product"-painiketta. UI avaa syötekentän _EAN-koodia_ varten. Käyttäjä syöttää _EAN-koodin_ ja painaa "Add to tracking"-painiketta. UI:n tapahtumankäsittelijä kutsuu `ProductService`-luokan sovelluslogiikkametodia, joka tarkistaa löytyykö tuotteen tiedot tietokannasta `ProductRepository`-luokan kautta. Koska ei löydy palautetaan _None_. UI näyttää käyttäjälle _missing info_-lomakkeen ja käyttäjä syöttää tuotteelle _nimen_ sekä _parasta ennen-päiväyksen_. UI:n tapahtumankäsittelijä kutsuu jälleen `ProducService`sovelluslogiikkaa, joka vastaa tuotteen tietojen ja tuotteen seurantaan lisäämisestä. `ProductService` kutsuu `ProductRepository`ja `TrackedProductRepository`-luokkia, jotka vastaavat tiedon pysyväistallennuksesta tietokantaan. UI kutsuu omaa tapahtumankäsittelijäänsä, joka lataa käyttäjälle näytettävän päivitetyn listan seurannassa olevista tuotteista.

## Ohjelman rakenteeseen jääneet heikkoudet

Tällä hetkellä kaikki haut tapahtuvat tietokannan välityksellä ja haut saattavat olla raskaita ja toisinaan hitaita, varsinkin kun datan määrä kasvaa ja seurannassa olevien tuotteiden määrä kasvaa voi optimointi olla paikallaan.
