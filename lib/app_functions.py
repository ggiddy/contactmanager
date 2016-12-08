"""Contains the main functions of the app"""
import os
import re
from database import db_functions
from tabulate import tabulate

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
        print "Contacts found"
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

def delete_contact(line):
    """Deletes a contact"""
    first_name = line['<first_name>']
    contacts = db_functions.get(first_name)

    if len(contacts) > 0:
        # There are contacts matching
        conts = []
        if len(contacts) > 1:
            for c in contacts:
                cts = [c.id, c.first_name, c.last_name]
                conts.append(cts)
            os.system('clear')

            print tabulate(conts, \
                    headers=['ID', 'First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid')
            try:
                contact_id = int(raw_input("Enter the ID of the contact to delete: "))
                deleted = db_functions.delete(contact_id)
                if deleted:
                    print "Deleted"
            except ValueError:
                print "Invalid entry"
        elif len(contacts) == 1:
            # only one contact, delete
            contact_id = contacts[0].id
            deleted = db_functions.delete(contact_id)
            if deleted:
                print "Deleted"
    else:
        return []
