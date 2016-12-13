"""Create the DB tables we need"""

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

BASE = declarative_base()

class Contacts(BASE):
    """Define contacts table"""
    __tablename__ = 'contacts'
    # Define columns.
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=True)
    phone_number = Column(String(13), nullable=False, unique=True)

# Create engine.
ENGINE = create_engine('sqlite:///contacts.db')

# Create all tables
BASE.metadata.create_all(ENGINE)
