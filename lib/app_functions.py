"""Contains the main functions of the app"""
import os
import re
from database import db_functions
from third_party.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from tabulate import tabulate
import requests
from firebase import firebase
import json

def new_contact(line):
    """Validate and create a new contact"""

    # Validate phone_number
    num = re.compile(r'^(07)(\d{8})$')
    if num.match(line['<phone_number>']):
        # Phone number valid
        first_name = line['<first_name>']
        last_name = line['<last_name>']
        phone_number = '+254' + str(int(line['<phone_number>'])) # Format appropriately

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


def send_text(line):
    """Sends a text message"""
    first_name = line['<first_name>']
    message = line['<message>']
    conts = []
    # Retrieve contact with given first_name
    contact = db_functions.get(first_name)
    if len(contact) == 0:
        print "There are no contacts matching %s" % first_name
    elif len(contact) == 1:
        # Just one contact, retrieve number
        phone_number = contact[0].phone_number
    elif len(contact) > 1:
        # Ask which contact to send to
        for c in contact:
            cts = [c.id, c.first_name, c.last_name]
            conts.append(cts)
        os.system('clear')
        print tabulate(conts, \
                headers=['ID', 'First Name', 'Last Name', 'Phone Number'], \
                tablefmt='fancy_grid')
        try:
            contact_id = int(raw_input("Enter the ID of the contact to send to: "))
            found_contact = db_functions.get_by_id(contact_id)
            if found_contact:
                # Now get phone_number
                phone_number = found_contact.phone_number
        except Exception as e:
            print "Invalid entry"
            return

    # Specify your login credentials
    username = "giddy254"
    apikey = "f0fd428f966c0caca7711a689bff6ebbd81edf8b28cbd4c6960a12c38a3d4655"
    # Specify the numbers that you want to send to in a comma-separated list
    # Please ensure you include the country code (+254 for Kenya)
    to = phone_number
    # And of course we want our recipients to know what we really do
    message = message
    # Create a new instance of our awesome gateway class
    gateway = AfricasTalkingGateway(username, apikey)
    # Any gateway errors will be captured by our custom Exception class below
    # so wrap the call in a try-catch block
    try:
        # Thats it, hit send and we'll take care of the rest.

        results = gateway.sendMessage(to, message)

        for recipient in results:
            # status is either "Success" or "error message"
            if recipient['status'] == 'Success':
                print "Message sent successfully"
    except AfricasTalkingGatewayException, e:
        print 'Encountered an error while sending: %s' % str(e)

def sync():
    """Sync contacts to firebase"""

    fb = firebase.FirebaseApplication('https://contactmanager-b338a.firebaseio.com/', None)
    data = {}
    all_contacts = db_functions.get()

    for contact in all_contacts:
        data.update({
            contact.id: {
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name
            }
        })

    result = fb.post('/contacts', data)

    print "Synced"
