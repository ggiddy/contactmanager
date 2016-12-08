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

import sys

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
        print new

    @docopt_cmd
    def do_search(self, line):
        """Usage: search <first_name>"""
        contacts = app_functions.search_contact(line)
        print contacts

    @docopt_cmd
    def do_contacts(self, line):
        """Usage: contacts"""
        all_contacts = db_functions.get()
        for c in all_contacts:
            print c.first_name +' '+ c.last_name +' '+ c.phone_number

    @docopt_cmd
    def do_text(self, line):
        """Usage: text <name> -m <message>"""
        print "Enter the text message"
        msg = input('->')

    @docopt_cmd
    def do_delete(self, line):
        """Usage: del (<name> | <phone>)"""
        pass

    @docopt_cmd
    def do_edit(self, line):
        """Usage: edit <first_name>"""
        contact = app_functions.edit_contact(line)
        print contact

    @docopt_cmd
    def do_history(self, name):
        """Usage: history <name>"""
        pass

    @docopt_cmd
    def do_sync(self, line):
        """Usage: sync"""
        pass

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
        