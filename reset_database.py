from app import db, create_app, models

app = create_app()


def delete_database():
    """
    Function for deleting the existing database and creating a new one.
    """
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        delete_database()
