"""
A CLI app to manage contacts and sends SMS.

Usage:
    app.py (-i | --interactive)
    app.py (-h | --help )
    app.py (-v | --version)
    Contact-Manager$: add -f <first_name> -l <last_name> -p <phone_number>
    Contact-Manager$: view
    Contact-Manager$: search <first_name>
    Contact-Manager$: edit <first_name>
    Contact-Manager$: del <first_name>
    Contact-Manager$: text <first_name> -m <message>
    Contact-Manager$: sync
    Contact-Manager$: help

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
from pyfiglet import Figlet, figlet_format
from termcolor import cprint, colored
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
    fig = Figlet(font='doom')
    print cprint(figlet_format('Contact Manager'), 'yellow', attrs=['bold', 'blink'])
    intro = colored('-- Version -- 1.0\n', 'yellow', attrs=['bold'])
    prompt = colored('Contact-Manager$: ', 'yellow', attrs=['bold'])

    @docopt_cmd
    def do_add(self, line):
        """Usage: add -f <first_name> -l <last_name> -p <phone_number>"""
        app_functions.new_contact(line)

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
                print colored('\n\t   ' +str(length) + ' contacts found matching "%s" \n' \
                    % line['<first_name>'], 'green', attrs=['bold'])
                print colored(tabulate(conts, \
                    headers=['First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid'), 'cyan')
            else:
                print colored('\n\t   ' + str(length) + ' contact found matching "%s" \n' % \
                     line['<first_name>'], 'green', attrs=['bold'])
                print colored(tabulate(conts, \
                    headers=['First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid'), 'cyan')
        else:
            print colored("\n No contacts found matching \"" + line['<first_name>'] +"\"\n", \
                 "red", attrs=['bold'])

    @docopt_cmd
    def do_view(self, line):
        """Usage: view"""
        os .system('clear')
        all_contacts = db_functions.get()
        conts = []
        for c in all_contacts:
            contact = [c.first_name, c.last_name, c.phone_number]
            conts.append(contact)
        length = len(all_contacts)
        if length > 0:
            if length > 1:
                print colored('\n' + '\t   Total contacts('+str(length) +')', \
                        'green', attrs=['bold'])
                print colored(tabulate(conts, \
                    headers=['First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid'), 'cyan')
            else:
                print str(length) + ' contact found\n'
                print colored(tabulate(conts, \
                    headers=['First Name', 'Last Name', 'Phone Number'], \
                    tablefmt='fancy_grid'), 'cyan')
        else:
            print colored("You have no saved contacts", "red")


    @docopt_cmd
    def do_text(self, line):
        """Usage: text <first_name> -m <message>"""
        app_functions.send_text(line)

    @docopt_cmd
    def do_del(self, line):
        """Usage: delete <first_name>"""
        app_functions.delete_contact(line)

    @docopt_cmd
    def do_edit(self, line):
        """Usage: edit <first_name>"""
        app_functions.edit_contact(line)

    @docopt_cmd
    def do_sync(self, line):
        """Usage: sync"""
        app_functions.sync()

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
        