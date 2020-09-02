from receipt_tracker.repo.sql_tables import Seller, Buyer, Receipt


def test_table_initial_inserts(db_session):
    query_buyer = db_session.query(Buyer).all()
    query_seller = db_session.query(Seller).all()
    query_receipt = db_session.query(Receipt).all()

    assert str(query_buyer) == '[Buyer(1, James, Trew), Buyer(2, Eugene, Min)]'
    assert str(query_seller) == '[Seller(1, Steam), Seller(2, No Frills), Seller(3, Amazon), Seller(4, Always Clean Coin Laundry)]'
    assert str(query_receipt) == '[Receipt(1, 2020-08-16, 9.67, Steam game), Receipt(2, 2020-08-17, 17.86, Groceries), Receipt(3, 2020-08-18, 57.36, Random amazon purchases), Receipt(4, 2020-08-19, 2.5, None)]'


def test_table_relationship(db_session):
    james = db_session.query(Buyer).filter(Buyer.id == 1).one()
    steam = db_session.query(Seller).filter(Seller.id == 1).one()

    assert james.first_name == 'James'
    assert str(james.purchases) == '[Receipt(1, 2020-08-16, 9.67, Steam game), Receipt(2, 2020-08-17, 17.86, Groceries)]'

    assert steam.name == 'Steam'
    assert str(steam.sales) == '[Receipt(1, 2020-08-16, 9.67, Steam game)]'
