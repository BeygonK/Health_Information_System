from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from flask_caching import Cache
import uuid
from datetime import datetime
from jsonschema import validate, ValidationError
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'SimpleCache'
db = SQLAlchemy(app)
cache = Cache(app)
Swagger(app)

executor = ThreadPoolExecutor()

# JSON Schemas
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

# Database Models
class Program(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Client(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrolled_programs = db.relationship('Program', secondary='enrollment')

enrollment = db.Table('enrollment',
    db.Column('client_id', db.String(36), db.ForeignKey('client.id')),
    db.Column('program_id', db.String(36), db.ForeignKey('program.id'))
)

# Create database
with app.app_context():
    db.create_all()

# 1. Create a health program
@app.route('/programs', methods=['POST'])
@swag_from({
    'tags': ['Programs'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'TB'},
                    'description': {'type': 'string', 'example': 'Tuberculosis Treatment'}
                },
                'required': ['name', 'description']
            }
        }
    ],
    'responses': {
        '201': {'description': 'Program created'},
        '400': {'description': 'Invalid input'}
    }
})
def create_program():
    try:
        data = request.get_json()
        validate(instance=data, schema=PROGRAM_SCHEMA)
        program = Program(name=data['name'], description=data['description'])
        db.session.add(program)
        db.session.commit()
        return jsonify({
            'id': program.id,
            'name': program.name,
            'description': program.description,
            'created_at': program.created_at.isoformat()
        }), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

# 2. Register a new client
@app.route('/clients', methods=['POST'])
@swag_from({
    'tags': ['Clients'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'John Doe'},
                    'date_of_birth': {'type': 'string', 'example': '1990-01-01'},
                    'gender': {'type': 'string', 'example': 'Male'}
                },
                'required': ['name', 'date_of_birth', 'gender']
            }
        }
    ],
    'responses': {
        '201': {'description': 'Client registered'},
        '400': {'description': 'Invalid input'}
    }
})
def register_client():
    try:
        data = request.get_json()
        validate(instance=data, schema=CLIENT_SCHEMA)
        client = Client(
            name=data['name'],
            date_of_birth=data['date_of_birth'],
            gender=data['gender']
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({
            'id': client.id,
            'name': client.name,
            'date_of_birth': client.date_of_birth,
            'gender': client.gender,
            'created_at': client.created_at.isoformat()
        }), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

# 3. Enroll client in a program
@app.route('/clients/<client_id>/enroll', methods=['POST'])
@swag_from({
    'tags': ['Clients'],
    'parameters': [
        {
            'name': 'client_id',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'program_id': {'type': 'string'}
                },
                'required': ['program_id']
            }
        }
    ],
    'responses': {
        '200': {'description': 'Client enrolled'},
        '400': {'description': 'Invalid input'},
        '404': {'description': 'Client or Program not found'}
    }
})
def enroll_client(client_id):
    try:
        data = request.get_json()
        validate(instance=data, schema=ENROLL_SCHEMA)
        client = Client.query.get(client_id)
        program = Program.query.get(data['program_id'])
        
        if not client or not program:
            return jsonify({'error': 'Client or Program not found'}), 404
        
        if program not in client.enrolled_programs:
            client.enrolled_programs.append(program)
            db.session.commit()
        
        return jsonify({
            'message': f'Client enrolled in {program.name}',
            'enrolled_programs': [p.name for p in client.enrolled_programs]
        })
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

# 4. Search for a client (async)
@app.route('/clients/search', methods=['GET'])
@swag_from({
    'tags': ['Clients'],
    'parameters': [
        {
            'name': 'name',
            'in': 'query',
            'type': 'string',
            'required': False
        }
    ],
    'responses': {
        '200': {'description': 'List of matching clients'}
    }
})
async def search_client():
    name = request.args.get('name', '').lower()
    
    async def search():
        with app.app_context():
            clients = Client.query.filter(Client.name.ilike(f'%{name}%')).all()
            return [
                {
                    'id': client.id,
                    'name': client.name,
                    'date_of_birth': client.date_of_birth,
                    'gender': client.gender
                }
                for client in clients
            ]
    
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(executor, search)
    return jsonify(results)

# 5 & 6. View client profile (cached)
@app.route('/clients/<client_id>', methods=['GET'])
@cache.cached(timeout=60)
@swag_from({
    'tags': ['Clients'],
    'parameters': [
        {
            'name': 'client_id',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ],
    'responses': {
        '200': {'description': 'Client profile'},
        '404': {'description': 'Client not found'}
    }
})
def get_client_profile(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    return jsonify({
        'id': client.id,
        'name': client.name,
        'date_of_birth': client.date_of_birth,
        'gender': client.gender,
        'enrolled_programs': [
            {
                'id': p.id,
                'name': p.name,
                'description': p.description
            }
            for p in client.enrolled_programs
        ],
        'created_at': client.created_at.isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)