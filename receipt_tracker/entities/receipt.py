class Receipt():
    """Receipt data.

    Args:
        id (int): Unique serial id generated by the database (primary key).

        date (datetime): Date of purchase.

        seller (str): Name of seller.

        total (float): Cost of purchase.

        person (int): Foreign key from Person class

        description (str): [Optional] Description of purchase (product, etc).

    """

    def __init__(self, id, date, seller, total, person, description=None):
        super().__init__()
        self.id = id
        self.date = date
        self.seller = seller
        self.total = total
        self.person = person
        self.description = description

    @classmethod
    def from_dict(cls, dct):
        """Instantiate class from a dictionary.

        Args:
            dct (dict): Receipt information in the form of a dict.

        Returns:
            Receipt: Receipt instance
        """
        return cls(
            id=dct['id'],
            date=dct['date'],
            seller=dct['seller'],
            total=dct['total'],
            person=dct['person'],
            description=dct.get('description'),
        )

    def to_dict(self):
        """Construct dictionary of Receipt instance.

        Returns:
            dict: Receipt information in the form of a dict.
        """
        return {
            'id': self.id,
            'date': self.date,
            'seller': self.seller,
            'total': self.total,
            'person': self.person,
            'description': self.description,
        }