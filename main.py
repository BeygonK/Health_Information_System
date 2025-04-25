from flask import Flask, jsonify, request
import uuid
from datetime import datetime

app = Flask(__name__)

# In-memory storage for clients and programs
clients = {}
programs = {}

class Client:
    def __init__(self, name, date_of_birth, gender):
        """
        Initialize a new client with a unique ID, name, date of birth,gender, and an empty list of enrolled programs.
        The ID is generated using UUID to ensure uniqueness.

        Args:
            name (string): Holds the name of the client
            date_of_birth (string): Holds the date of birth of the client
            gender (string): Holds the gender of the client
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.enrolled_programs = []
        self.created_at = datetime.now()
        

class Program:
    def __init__(self, name, description):
        """
        Initialize a new program with a unique ID, name, description, and the date it was created.

        Args:
            name (string): Holds the name of the program
            description (string): Describes the program
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_at = datetime.now()