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
from lib.functions import create, get, update, delete

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
        """Usage: add -n <name> -p <phone_number>"""
        fname, phone = line['<name>'], line['<phone_number>']
        created = create(fname, phone)
        if created:
            print "Adding successful"

    @docopt_cmd
    def do_search(self, name):
        """Usage: search <name>"""
        pass

    @docopt_cmd
    def do_viewall(self, line):
        """Usage: viewall"""
        all_contacts = get()
        if all_contacts:
            for contact in all_contacts:
                print contact.first_name + " " + contact.phone_number

    @docopt_cmd
    def do_text(self, line):
        """Usage: text <name> -m <message>"""
        pass

    @docopt_cmd
    def do_delete(self, line):
        """Usage: del (<name> | <phone>)"""
        pass

    @docopt_cmd
    def do_edit(self, line):
        """Usage edit <name> -n <new_name> <new_phone>"""
        pass

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

    @docopt_cmd
    def do_EOF(self, line):
        """Exit the app"""
        print "Good Bye"
        return True

OPT = docopt(__doc__, sys.argv[1:], version="ContactManager version: 1.0")

if OPT['--interactive']:
    ContactManager().cmdloop()

print OPT