"""Create the DB tables we need"""

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Contacts(Base):
    """Define contacts table"""
    __tablename__ = 'contacts'
    # Define columns.
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=True)
    phone_number = Column(String(13), nullable=False)


class Messages(Base):
    """Define messages table"""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(String(250))
    sent_to = Column(Integer, ForeignKey('contacts.id'))

# Create engine.
ENGINE = create_engine('sqlite:///contacts.db')

# Create all tables
Base.metadata.create_all(ENGINE)
