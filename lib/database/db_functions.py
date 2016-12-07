"""Functions that perform operations on DB"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import Contacts, Messages, BASE

ENGINE = create_engine('sqlite:///../../contacts.db')

# Bind engine to the Base class metadata
BASE.metadata.bind = ENGINE

DB_SESSION = sessionmaker(bind=ENGINE)
SESSION = DB_SESSION()

class DbManipulator(object):
    """Contains the methods that perform database manipulation"""
    def __init__(self):
        pass

    # Create a new contact
    def create(self, fname, phone, lname=None):
        """Creates a new contact and saves it to DB"""
        new_contact = Contacts(first_name=fname, last_name=lname or 'NULL', phone_number=phone)
        SESSION.add(new_contact)
        SESSION.commit()
        return new_contact

    def get(self, fname=None, lname=None, phone=None):
        """Fetches contacts from the DB"""
        if not (fname or lname or phone):
            # Get all records
            contacts = SESSION.query(Contacts).all()
            return contacts
        else:
            # Get specific records
            if fname:
                # Query using the fname
                contacts = SESSION.query(Contacts).filter(Contacts.first_name == fname).all()
                return contacts
            if lname:
                # Query using the lname, if more than one record, ask for lname
                pass
            if phone:
                # Query using phone
                pass
            if fname and lname:
                # Query using the fname, lname
                pass


    def update(self, fname=None, lname=None, phone=None):
        """Updates a particular contact"""
        pass

    def delete(self, fname=None, lname=None, phone=None):
        """Deletes a contact"""
        pass
