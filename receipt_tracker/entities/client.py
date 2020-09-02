

class Client(object):
    """Client data.

    Args:
        id (int): Unique serial id generated by the database (primary key).
        fname (str): First name of client.
        lname (str): Last name of client.
    """

    def __init__(self, id, fname, lname):
        self.id = id
        self.fname = fname
        self.lname = lname

    @classmethod
    def from_dict(cls, dct):
        """Instantiate class from a dictionary.

        Args:
            dct (dict): Client information in the form of a dict.

        Returns: Client instance
        """
        return cls(
            id=dct['id'],
            fname=dct['fname'],
            lname=dct['lname']
        )

    def to_dict(self):
        """Construct dictionary of Client instance.

        Returns:
            dict: Client information in the form of a dict.
        """
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname
        }



