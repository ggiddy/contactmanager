"""Functions that perform operations on DB"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.table_def import Contacts, Messages, Base

ENGINE = create_engine('sqlite:///contacts.db')

# Bind engine to the Base class metadata
Base.metadata.bind = ENGINE

DB_SESSION = sessionmaker(bind=ENGINE)
SESSION = DB_SESSION()

# Create a new contact
def create(fname, phone, lname=None):
    """Creates a new contact and saves it to DB"""
    new_contact = Contacts(first_name=fname, last_name=lname, phone_number=phone)
    SESSION.add(new_contact)
    SESSION.commit()
    return new_contact

def get(fname=None, lname=None, phone=None):
    """Fetches contacts from the DB"""
    if not (fname or lname or phone):
        # Get all records
        contacts = SESSION.query(Contacts).all()
        return contacts
    else:
        # Get specific records
        if fname:
            # Query using the fname, if more than one record, ask for lname
            pass

def update(fname=None, lname=None, phone=None):
    """Updates a particular contact"""
    pass

def delete(fname=None, lname=None, phone=None):
    """Deletes a contact"""
    pass
