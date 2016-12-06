#!/home/giddy/Desktop/bootcamp/project/contactmanager/.env/bin/python
"""Application Testcases"""

from unittest import TestCase
from contactmanager.app import ContactManager

class TestContactManager(TestCase):
    """Testcases for the methods in app.py file"""
    def test_creates_contact_with_254(self):
        """Test if new contact gets created"""
        pass

    def test_creates_contact_with_07(self):
        """Test if new contact gets created"""
        pass

    def test_rejects_wrong_number_format(self):
        """Test if new contact gets created"""
        pass

    def test_name_already_added(self):
        """Test if a person with the same name exists"""
        pass

    def test_person_with_same_number(self):
        """Test if the person has the same number"""
        pass

    def test_syncs_with_firebase(self):
        """Test if the contact gets synced upon saving"""
        pass

    def test_created_but_not_synced(self):
        """Save contact"""
        pass

    def test_gets_contacts_from_db(self):
        """Retrieves contacts"""
        pass

    def tests_searches_a_contact(self):
        """Searches a particular contact"""
        pass

    def test_edits_a_contact(self):
        """Edits a contact"""
        pass

    def test_deletes_contact(self):
        """Deletes a contact"""
        pass
    def test_sends_text_message(self):
        """Sends a text message"""
        pass

    def test_retrieves_message_history(self):
        """Test that the history gets shown"""
        pass

    def test_sync_contacts(self):
        """Test if the contacts get synced to firebase"""
        pass

