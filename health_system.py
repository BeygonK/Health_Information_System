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



# 1. Route to get programs
@app.route('/programs', methods=['POST'])
def create_program():
    data = request.get_json()
    program = Program(data['name'], data['description'])
    programs[program.id] = program
    return jsonify({
        'id': program.id,
        'name': program.name,
        'description': program.description,
        'created_at': program.created_at.isoformat()
    }), 201
    

# 2. Register a new client
@app.route('/clients', methods=['POST'])
def register_client():
    data = request.get_json()
    client = Client(data['name'], data['date_of_birth'], data['gender'])
    clients[client.id] = client
    return jsonify({
        'id': client.id,
        'name': client.name,
        'date_of_birth': client.date_of_birth,
        'gender': client.gender,
        'created_at': client.created_at.isoformat()
    }), 201