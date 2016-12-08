"""Contains the main functions of the app"""
import re
from database import db_functions

def new_contact(line):
    """Validate and create a new contact"""

    # Validate phone_number
    num = re.compile(r'^(07)(\d{8})$')
    if num.match(line['<phone_number>']):
        # Phone number valid
        first_name = line['<first_name>']
        last_name = line['<last_name>']
        phone_number = line['<phone_number>']

        # Check if phone number has been saved
        contacts = db_functions.get(first_name)

        if contacts:
            for con in contacts:
                if phone_number == con.phone_number:
                    # Phone number already saved.
                    return "That phone number already exists"
            # Same name different phone number
            new = db_functions.create(first_name, phone_number, last_name)
            return new
        else:
            # Save contact and return it
            new = db_functions.create(first_name, phone_number, last_name)
            return new
    else: # Invalid phone
        return "Not a valid phone number"

def all_contacts():
    """Retrieve all contacts"""
    contacts = db_functions.get()
    if contacts:
        print "100 Contacts found"
        return contacts

def search_contact(line):
    """Search a contact using the given parameters"""
    first_name = line['<first_name>']
    contacts = db_functions.get(first_name)
    return contacts


def edit_contact(line):
    """Update a contact"""
    first_name = line['<first_name>']

    # Find the contact that matches the first name
    contact = db_functions.get(first_name)

    if len(contact) == 0:
        return 'No contacts matching %s were found' % first_name
    else:
        if len(contact) > 0:
            # More than 1 contact with the same firstname found
            return contact
