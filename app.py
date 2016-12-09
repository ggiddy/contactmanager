"""
A CLI app to manage contacts and sends SMS.

Usage:
    app.py (-i | --interactive)
    app.py (-h | --help | -v | --version)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    -v, --version  Show the version number.
"""

import cmd
from docopt import docopt, DocoptExit
import lib.app_functions as app_functions
from lib.database import db_functions
from tabulate import tabulate

import sys
import os

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print 'Invalid Command!'
            print e
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

class ContactManager(cmd.Cmd):
    """Handler for the incoming commands."""

    @docopt_cmd
    def do_add(self, line):
        """Usage: add -f <first_name> -l <last_name> -p <phone_number>"""
        new = app_functions.new_contact(line)
        if new:
            print "Added %s %s %s" % (new.first_name, new.last_name, new.phone_number)

    @docopt_cmd
    def do_search(self, line):
        """Usage: search <first_name>"""
        os.system('clear')
        contacts = app_functions.search_contact(line)
        conts = []
        length = len(contacts)

        for c in contacts:
            contact = [c.first_name, c.last_name, c.phone_number]
            conts.append(contact)

        if length > 0:
            if length > 1:
                print str(length) + ' contacts found\n'
                print tabulate(conts, \
                    headers=['First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid')
            else:
                print str(length) + ' contact found\n'
                print tabulate(conts, \
                    headers=['First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid')
        else:
            print "No contacts found matching " + line['<first_name>']

    @docopt_cmd
    def do_contacts(self, line):
        """Usage: contacts"""
        all_contacts = db_functions.get()
        conts = []
        for c in all_contacts:
            contact = [c.first_name, c.last_name, c.phone_number]
            conts.append(contact)
        length = len(all_contacts)
        if length > 0:
            if length > 1:
                print str(length) + ' contacts found\n'
                print tabulate(conts, \
                    headers=['First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid')
            else:
                print str(length) + ' contact found\n'
                print tabulate(conts, \
                    headers=['First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid')
        else:
            print "You have no contacts"


    @docopt_cmd
    def do_text(self, line):
        """Usage: text <first_name> -m <message>"""
        app_functions.send_text(line)

    @docopt_cmd
    def do_delete(self, line):
        """Usage: delete <first_name>"""
        app_functions.delete_contact(line)

    @docopt_cmd
    def do_edit(self, line):
        """Usage: edit <first_name>"""
        app_functions.edit_contact(line)

    @docopt_cmd
    def do_history(self, name):
        """Usage: history <name>"""
        pass

    @docopt_cmd
    def do_sync(self, line):
        """Usage: sync"""
        app_functions.sync()

    @docopt_cmd
    def do_exit(self, line):
        """Exits the app"""
        pass

    def do_EOF(self, line):
        """Exit the app"""
        print "Good Bye"
        return True

OPT = docopt(__doc__, sys.argv[1:], version="ContactManager version: 1.0")

if OPT['--interactive']:
    try:
        print __doc__
        ContactManager().cmdloop()
    except KeyboardInterrupt:
        print "Exiting App..."
        