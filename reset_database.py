from app import db


def delete_database():
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    delete_database()
