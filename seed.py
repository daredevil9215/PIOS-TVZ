from app import db, create_app
from app.models import User, Ticket

app = create_app()


def seed_users():
    users = [
        User(firstname="admin", lastname="admin", email="admin@tim09.hr", username="admin1",
             password_hash="pbkdf2:sha256:600000$WLlhsm1tjmmTKiYA$b6b8e134385f41950091bdea0244b6258a092cfb45174df8ad321baa2db649c3", is_admin=1, balance=0),
        User(firstname="asd", lastname="asd", email="asd@asd.com", username="asd",
             password_hash="pbkdf2:sha256:600000$FwCwXGy0AtpX7ynx$49f105246ad1c31fea49a5577da11b1937f5643514ca367507621e7518cc3c3d", is_admin=0, balance=500)
    ]
    for user in users:
        db.session.add(user)
    db.session.commit()


def seed_tickets():
    tickets = [
        Ticket(city="Zagreb", name="231 BORONGAJ - DUBEC",
               route="BORONGAJ - DUBEC", total_seats=100, reserved_seats=0, price=1.00),
        Ticket(city="Zagreb", name="102 BRITANSKI TRG - MIHALJEVAC",
               route="BRITANSKI TRG - MIHALJEVAC", total_seats=150, reserved_seats=1, price=1.00),
        Ticket(city="Zagreb", name="121 ČRNOMEREC - KARAŽNIK - GAJNICE", route="ČRNOMEREC - KARAŽNIK - GAJNICE",
               total_seats=100, reserved_seats=0, price=1.00),
        Ticket(city="Zagreb", name="274 ZAGREB (DUBEC) - SESVETE - LAKTEC", route="ZAGREB (DUBEC) - SESVETE - LAKTEC",
               total_seats=100, reserved_seats=0, price=1.00),
        Ticket(city="Zagreb", name="243 GLAVNI KOLODVOR - KAJZERICA", route="GLAVNI KOLODVOR - KAJZERICA",
               total_seats=10000, reserved_seats=0, price=1.00),
        Ticket(city="Zagreb", name="Dnevna karta Zagreb", route="",
               total_seats=10000, reserved_seats=0, price=4.00),
        Ticket(city="Zagreb", name="Tjedna karta Zagreb", route="",
               total_seats=10000, reserved_seats=0, price=10.00),
        Ticket(city="Zagreb", name="Mjesečna karta Zagreb", route="",
               total_seats=10000, reserved_seats=0, price=20.00),
        Ticket(city="Zagreb", name="Godišnja karta Zagreb", route="",
               total_seats=10000, reserved_seats=0, price=50.00),
        Ticket(city="Rijeka", name="Dnevna karta Rijeka", route="",
               total_seats=10000, reserved_seats=0, price=4.00),
        Ticket(city="Rijeka", name="Tjedna karta Rijeka", route="",
               total_seats=10000, reserved_seats=0, price=10.00),
        Ticket(city="Rijeka", name="Mjesečna karta Rijeka", route="",
               total_seats=10000, reserved_seats=0, price=20.00),
        Ticket(city="Rijeka", name="Godišnja karta Rijeka", route="",
               total_seats=10000, reserved_seats=0, price=50.00),
        Ticket(city="Osijek", name="Dnevna karta Osijek", route="",
               total_seats=10000, reserved_seats=0, price=4.00),
        Ticket(city="Osijek", name="Tjedna karta Osijek", route="",
               total_seats=10000, reserved_seats=0, price=10.00),
        Ticket(city="Osijek", name="Mjesečna karta Osijek", route="",
               total_seats=10000, reserved_seats=0, price=20.00),
        Ticket(city="Osijek", name="Godišnja karta Osijek", route="",
               total_seats=10000, reserved_seats=0, price=50.00),
        Ticket(city="Split", name="Dnevna karta Split", route="",
               total_seats=10000, reserved_seats=0, price=4.00),
        Ticket(city="Split", name="Tjedna karta Split", route="",
               total_seats=10000, reserved_seats=0, price=10.00),
        Ticket(city="Split", name="Mjesečna karta Split", route="",
               total_seats=10000, reserved_seats=0, price=20.00),
        Ticket(city="Split", name="Godišnja karta Split", route="",
               total_seats=10000, reserved_seats=0, price=50.00),
        Ticket(city="Pula", name="Dnevna karta Pula", route="",
               total_seats=10000, reserved_seats=0, price=4.00),
        Ticket(city="Pula", name="Tjedna karta Pula", route="",
               total_seats=10000, reserved_seats=0, price=10.00),
        Ticket(city="Pula", name="Mjesečna karta Pula", route="",
               total_seats=10000, reserved_seats=0, price=20.00),
        Ticket(city="Pula", name="Godišnja karta Pula", route="",
               total_seats=10000, reserved_seats=0, price=50.00),
    ]

    for ticket in tickets:
        db.session.add(ticket)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        seed_users()
        seed_tickets()
