import os
from initialize_database import initialize_database
from config import DATABASE_FILE_PATH


def build():
    db_dir = os.path.dirname(DATABASE_FILE_PATH)
    os.makedirs(db_dir, exist_ok=True)

    initialize_database()


if __name__ == "__main__":
    build()
