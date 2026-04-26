from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
      DROP TABLE IF EXISTS shelves;
    ''')

    connection.commit()

    cursor.execute('''
      DROP TABLE IF EXISTS departments;
    ''')

    connection.commit()

    cursor.execute('''
        DROP TABLE IF EXISTS employee_store_permissions;
    ''')

    connection.commit()

    cursor.execute('''
      DROP TABLE IF EXISTS stores;
    ''')

    connection.commit()

    cursor.execute('''
      DROP TABLE IF EXISTS users;
    ''')

    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
        CREATE TABLE users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('merchant', 'employee')),
            password_is_temporary INTEGER NOT NULL,
            employer_id TEXT NULL,
            CONSTRAINT foreignkey_employer
                FOREIGN KEY (employer_id) REFERENCES users(user_id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE stores (
        store_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        owner_id TEXT NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES users(user_id)
        );
    ''')

    connection.commit()

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_users_employer_id
        ON users(employer_id)
    ''')

    connection.commit()

    cursor.execute('''
        CREATE TABLE employee_store_permissions (
        employee_id TEXT,
        store_id TEXT,
        permission TEXT NOT NULL,
        PRIMARY KEY (employee_id, store_id),
        FOREIGN KEY (employee_id) REFERENCES users(user_id),
        FOREIGN KEY (store_id) REFERENCES stores(store_id)
    );
    ''')

    connection.commit()

    cursor.execute('''
        CREATE TABLE departments (
        department_id TEXT PRIMARY KEY,
        store_id TEXT NOT NULL,
        name TEXT NOT NULL,
        check_days_before INTEGER NOT NULL,
        FOREIGN KEY (store_id) REFERENCES stores(store_id)
        );
    ''')

    connection.commit()

    cursor.execute('''
        CREATE TABLE shelves (
        shelf_id TEXT PRIMARY KEY,
        department_id TEXT NOT NULL,
        name TEXT NOT NULL,
        is_default INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        );
    ''')

    connection.commit()


def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()
