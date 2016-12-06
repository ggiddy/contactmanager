"""App module bootstraps starts the app"""

import cmd

class ContactManager(cmd.Cmd):
    """Handler for the incoming commands."""
    def do_add(self, name):
        """Creates a new contact."""
        pass

    def do_search(self, name):
        """Searches for a particular contact."""
        pass

    def do_viewall(self, line):
        """Shows all the saved contacts."""
        pass

    def do_text(self, line):
        """Sends a text message to a person with name *name"""
        pass

    def do_delete(self, line):
        """Deletes a contact"""
        pass

    def do_edit(self, line):
        """Edits a contact"""
        pass

    def do_history(self, name):
        """Shows the number of messages sent to *name and their content"""
        pass

    def do_exit(self, line):
        """Exits the app"""
        pass

    def do_sync(self, line):
        """Syncs contacts with Firebase"""

    def do_EOF(self, line):
        """Exit the app"""
        print "Good Bye"
        return True

if __name__ == '__main__':
    ContactManager().cmdloop()
