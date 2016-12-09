"""Functions that perform operations on DB"""
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

BASE = declarative_base()

class Contacts(BASE):
    """Define contacts table"""
    __tablename__ = 'contacts'
    # Define columns.
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=True)
    phone_number = Column(String(13), nullable=False, unique=True)


class Messages(BASE):
    """Define messages table"""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(String(250))
    sent_to = Column(Integer, ForeignKey('contacts.id'))

# Create engine.
ENGINE = create_engine('sqlite:///../../contacts.db')

# Bind engine to the Base class metadata
BASE.metadata.bind = ENGINE

DB_SESSION = sessionmaker(bind=ENGINE)
SESSION = DB_SESSION()

# Create a new contact
def create(fname, phone, lname=None):
    """Creates a new contact and saves it to DB"""
    new_contact = Contacts(first_name=fname, last_name=lname or 'NULL', phone_number=phone)
    SESSION.add(new_contact)
    try:
        SESSION.commit()
    except Exception as e:
        SESSION.rollback()
        return Exception
    return new_contact

def get(fname=None, lname=None, phone=None):
    """Fetches contacts from the DB"""
    if not (fname or lname or phone):

        # Get all records if no params passed
        contacts = SESSION.query(Contacts).all()
        return contacts

    else:
        # Get specific records
        if fname:
            # Query using the fname
            contacts = SESSION.query(Contacts).filter(Contacts.first_name.contains(fname)).all()
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
def get_by_id(id):
    """Fetches a contact by id"""
    contact = SESSION.query(Contacts).filter(Contacts.id == id).first()
    if contact:
        return contact

def search(any_param):
    """Searches for possible matches"""
    pass

def update(contact_obj):
    """Updates a particular contact"""
    contact = SESSION.query(Contacts).filter(Contacts.id == contact_obj.id).first()
    contact = contact_obj
    SESSION.commit()
    return True

def delete(contact_id):
    """Deletes a contact"""
    contact = SESSION.query(Contacts).filter(Contacts.id == contact_id).first()
    if not contact:
        print "Invalid id"
    else:
        print 'Deleting...'
        deleted = SESSION.delete(contact)
        SESSION.commit()
        return True

