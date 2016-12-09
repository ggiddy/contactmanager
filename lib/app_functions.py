"""Contains the main functions of the app"""
import os
import re
from database import db_functions
from third_party.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from tabulate import tabulate
import requests
from firebase import firebase
import json
from termcolor import cprint, colored

def new_contact(line):
    """Validate and create a new contact"""

    # Validate phone_number
    num = re.compile(r'^(07)(\d{8})$')
    if num.match(line['<phone_number>']):
        # Phone number valid
        first_name = line['<first_name>']
        last_name = line['<last_name>']
        phone_number = '+254' + str(int(line['<phone_number>'])) # Format appropriately

        # Save contact and return it
        try:
            new = db_functions.create(first_name, phone_number, last_name)
            if new:
                print colored("Successfully added %s %s %s" %\
                    (new.first_name, new.last_name, new.phone_number), 'green')
        except Exception as e:
            print colored("The phone number already exists", 'red')
            return
    else: # Invalid phone
        print colored("The phone number is invalid", "red", attrs=['bold', 'blink'])

def all_contacts():
    """Retrieve all contacts"""
    contacts = db_functions.get()
    if contacts:
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
        print 'No contacts matching %s were found' % first_name
    elif len(contact) == 1:
        # Exactly 1 contact found
        contact_id = contact[0].id
        matching_contact = db_functions.get_by_id(contact_id)
        conts = []
        cts = [matching_contact.id, matching_contact.first_name,\
             matching_contact.last_name, matching_contact.phone_number]
        conts.append(cts)
        os.system('clear')
        print colored(tabulate(conts, \
                    headers=['ID', 'First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid'), 'cyan')
        do_update(matching_contact)
    elif len(contact) > 1:
        # More than 1 contact
        conts = []
        for con in contact:
            cts = [con.id, con.first_name, con.last_name, con.phone_number]
            conts.append(cts)
        os.system('clear')
        print colored(tabulate(conts, \
                    headers=['ID', 'First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid'), 'cyan')
        try:
            cont_id = int(raw_input('Enter the ID of the contact to edit:  '))
            in_results = False
            for con in contact:
                if cont_id == con.id:
                    in_results = True
            if in_results:
                matching_contact = db_functions.get_by_id(cont_id)
            else:
                print "Please select an ID from the above contacts"
                return
            if matching_contact:
                do_update(matching_contact)
            else:
                print "No contact matches the provided id"
        except Exception as e:
            print "Invalid ID"

def delete_contact(line):
    """Deletes a contact"""
    first_name = line['<first_name>']
    contacts = db_functions.get(first_name)

    if len(contacts) > 0:
        # There are contacts matching
        conts = []
        if len(contacts) > 1:
            for c in contacts:
                cts = [c.id, c.first_name, c.last_name, c.phone_number]
                conts.append(cts)
            os.system('clear')

            print colored(tabulate(conts, \
                    headers=['ID', 'First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid'), 'cyan')
            try:
                contact_id = int(raw_input("Enter the ID of the contact to delete: "))
                in_results = False
                for contact in contacts:
                    if contact.id == contact_id:
                        in_results = True
                if in_results:
                    deleted = db_functions.delete(contact_id)
                else:
                    print colored("Please select ID among the records above", "red")
                    return
                if deleted:
                    print "Deleted"
            except ValueError:
                print "Invalid entry"
        elif len(contacts) == 1:
            # only one contact, delete
            contact_id = contacts[0].id
            deleted = db_functions.delete(contact_id)
            if deleted:
                print colored("Deleted", 'green', attrs=['bold'])
    else:
        return []

def do_update(matching_contact):
    """Updates contact details"""
    # What to update?
    to_update = str(raw_input("What field do you want to update?\
                \n[F] First Name [L] Last Name [P] Phone Number  "))
    choice = re.compile(r'(f|F|l|L|p|P)')

    if choice.match(to_update):
        if to_update == 'f' or to_update == 'F':
            # Update firstname
            new_fname = raw_input('Enter the new First Name: ')
            if len(new_fname.split()) > 1 or len(new_fname.split()) == 0:
                print colored("Please enter one name", "red")
                return
            elif len(new_fname.split()) == 1:
                # Good input, update
                matching_contact.first_name = new_fname
                updated = db_functions.update(matching_contact)
                if updated:
                    print 'Changes saved successfully'
                else:
                    print 'Problem encountered with database connection'
        if to_update == 'l' or to_update == 'L':
            # Update lastname
            new_lname = raw_input('Enter the new Last Name: ')
            if len(new_lname.split()) > 1 or len(new_lname.split()) == 0:
                print "Please enter one name"
                return
            elif len(new_lname.split()) == 1:
                # Good input, update
                matching_contact.last_name = new_lname
                updated = db_functions.update(matching_contact)
                if updated:
                    print 'Changes saved successfully'
                else:
                    print 'Problem encountered with database connection'
        if to_update == 'p' or to_update == 'P':
            # Update phone
            new_phone = raw_input('Enter the new Phone Number: ')
            num = re.compile(r'^(07)(\d{8})$')
            if not num.match(new_phone):
                print "Invalid phone number"
                return
            new_phone = '+254' + str(int(new_phone))
            # Can't have phone duplicates
            all_conts = db_functions.get()
            for con in all_conts:
                if con.phone_number == new_phone:
                    print "Phone number already exists"
                    return
            # Phone must be correct format
            if len(new_phone.split()) > 1 or len(new_phone.split()) == 0:
                print "Please enter one phone number"
            elif len(new_phone.split()) == 1:
                # Good input, update
                matching_contact.phone_number = new_phone
                updated = db_functions.update(matching_contact)
                if updated:
                    print 'Changes saved successfully'
                else:
                    print 'Problem encountered with database connection'
    else:
        print 'Invalid choice'

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
        print colored(tabulate(conts, \
                headers=['ID', 'First Name', 'Last Name', 'Phone Number'], \
                tablefmt='fancy_grid'), 'cyan')
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
        print colored("Sending...", "blue")
        for recipient in results:
            # status is either "Success" or "error message"
            if recipient['status'] == 'Success':
                print colored("Message sent successfully", "green")
    except AfricasTalkingGatewayException, e:
        print 'Encountered an error while sending: %s' % str(e)
    return True

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
                "last_name": contact.last_name,
                "phone_number": contact.phone_number
            }
        })

    result = fb.post('/contacts', data)
    print colored("Syncing...", "blue")
    print colored("Synced", "green", attrs=['bold'])
