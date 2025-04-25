from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
import uuid
from datetime import datetime
from jsonschema import validate, ValidationError

app = Flask(__name__)
Swagger(app)

# JSON Schemas for validation
PROGRAM_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "description": {"type": "string"}
    },
    "required": ["name", "description"]
}

CLIENT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "date_of_birth": {"type": "string", "format": "date"},
        "gender": {"type": "string", "enum": ["Male", "Female", "Other"]}
    },
    "required": ["name", "date_of_birth", "gender"]
}

ENROLL_SCHEMA = {
    "type": "object",
    "properties": {
        "program_id": {"type": "string"}
    },
    "required": ["program_id"]
}

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
    

# 3. Enroll client in a program
@app.route('/clients/<client_id>/enroll', methods=['POST'])
def enroll_client(client_id):
    data = request.get_json()
    program_id = data['program_id']
    
    if client_id not in clients or program_id not in programs:
        return jsonify({'error': 'Client or Program not found'}), 404
    
    client = clients[client_id]
    if program_id not in client.enrolled_programs:
        client.enrolled_programs.append(program_id)
    
    return jsonify({
        'message': f'Client enrolled in {programs[program_id].name}',
        'enrolled_programs': [programs[pid].name for pid in client.enrolled_programs]
    })

# 4. Search for a client
@app.route('/clients/search', methods=['GET'])
def search_client():
    name = request.args.get('name', '').lower()
    results = [
        {
            'id': client.id,
            'name': client.name,
            'date_of_birth': client.date_of_birth,
            'gender': client.gender
        }
        for client in clients.values()
        if name in client.name.lower()
    ]
    return jsonify(results)



# 5. View client profile
@app.route('/clients/<client_id>', methods=['GET'])
def get_client_profile(client_id):
    if client_id not in clients:
        return jsonify({'error': 'Client not found'}), 404
    
    client = clients[client_id]
    return jsonify({
        'id': client.id,
        'name': client.name,
        'date_of_birth': client.date_of_birth,
        'gender': client.gender,
        'enrolled_programs': [
            {
                'id': pid,
                'name': programs[pid].name,
                'description': programs[pid].description
            }
            for pid in client.enrolled_programs
        ],
        'created_at': client.created_at.isoformat()
    })
    

# Entry point for the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)