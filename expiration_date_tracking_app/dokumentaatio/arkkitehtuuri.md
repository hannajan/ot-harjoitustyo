# Arkkitehtuuri

## Luokkakaavio

```mermaid
classDiagram
  class User {
    user_id,
    username,
    password_hash,
    role
  }
  class Merchant {
    stores
  }
  class Store {
    store_id,
    name,
    owner_id
  }
  Merchant --|> User
  Merchant "1" -- "*" Store
```
