"""Functions that perform operations on DB"""
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from table_def import Contacts
from termcolor import colored

BASE = declarative_base()

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

def get(param=None, field=None):
    """Fetches contacts from the DB"""
    if not param:

        # Get all records if no params passed
        contacts = SESSION.query(Contacts).all()
        return contacts

    else:
        # Get specific records
        if field == 'f':
            # Query using the first name
            contacts = SESSION.query(Contacts).filter(Contacts.first_name.contains(param)).all()
            return contacts
        if field == 'l':
            # Query using the last name
            contacts = SESSION.query(Contacts).filter(Contacts.last_name.contains(param)).all()
            return contacts
        if field == 'p':
            # Query using the phone number
            contacts = SESSION.query(Contacts).filter(Contacts.phone_number.contains(param)).all()
            return contacts

def get_by_id(id):
    """Fetches a contact by id"""
    contact = SESSION.query(Contacts).filter(Contacts.id == id).first()
    if contact:
        return contact

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
        return False
    else:
        print colored("Deleting...", "blue", attrs=['bold'])
        deleted = SESSION.delete(contact)
        SESSION.commit()
        return True
