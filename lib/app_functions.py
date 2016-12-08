"""Contains the main functions of the app"""
import re
from database import db_functions
from third_party.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

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

def send_text():
    """Sends a text message"""

    # Specify your login credentials
    username = "MyAfricasTalkingUsername"
    apikey = "MyAfricasTalkingAPIKey"
    # Specify the numbers that you want to send to in a comma-separated list
    # Please ensure you include the country code (+254 for Kenya)
    to = "+254711XXXYYY,+254733YYYZZZ"
    # And of course we want our recipients to know what we really do
    message = "I'm a lumberjack and it's ok, I sleep all night and I work all day"
    # Create a new instance of our awesome gateway class
    gateway = AfricasTalkingGateway(username, apikey)
    # Any gateway errors will be captured by our custom Exception class below
    # so wrap the call in a try-catch block
    try:
        # Thats it, hit send and we'll take care of the rest.

        results = gateway.sendMessage(to, message)

        for recipient in results:
            # status is either "Success" or "error message"
            print 'number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                                recipient['status'],
                                                                recipient['messageId'],
                                                                recipient['cost'])
    except AfricasTalkingGatewayException, e:
        print 'Encountered an error while sending: %s' % str(e)

def delete_contact(line):
    """Deletes a contact"""
    first_name = line['<first_name>']
    last_name = line['<last_name>']

    deleted = db_functions.delete(first_name, last_name)

    if deleted:
        return "Successfully deleted contact"
    else:
        return "No contacts found matching provided names"
