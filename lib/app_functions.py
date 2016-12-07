"""Contains the main functions of the app"""
import re
from database.db_functions import DbManipulator


DBM = DbManipulator()
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
        contact = DBM.get(first_name)
        print contact
        if phone_number == contact.phone_number:
            # Phone number already saved.
            return "That phone number already exists"
        else:
            # Save contact and return it
            new = DBM.create(first_name, phone_number, last_name)
            return new
    else:
        return "Not a valid phone number"
    # Query with validated phone if number exists, no. already added

    # Else add user
    return "Creating the new contact %s %s %s" \
            % (line['<first_name>'], line['<last_name>'], line['<phone_number>'])

def all_contacts():
    """Retrieve all contacts"""
    contacts = DBM.get()
    return contacts

def search_contact():
    """Search a contact using the given parameters"""
    return 1
