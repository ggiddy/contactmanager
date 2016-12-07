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
        contact = db_functions.get(first_name)

        if contact:
            if phone_number == contact.phone_number:
                # Phone number already saved.
                return "That phone number already exists"
        else:
            # Save contact and return it
            new = db_functions.create(first_name, phone_number, last_name)
            return new
    else: # Invalid phone
        return "Not a valid phone number"

    return "Creating the new contact %s %s %s" \
            % (line['<first_name>'], line['<last_name>'], line['<phone_number>'])

def all_contacts():
    """Retrieve all contacts"""
    contacts = db_functions.get()
    if contacts:
        print "Contacts found"
        return contacts

def search_contact():
    """Search a contact using the given parameters"""
    return 1
