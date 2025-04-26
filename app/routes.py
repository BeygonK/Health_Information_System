from flask import jsonify, request
from flasgger import swag_from
from jsonschema import validate, ValidationError
import asyncio
from concurrent.futures import ThreadPoolExecutor
from flask_httpauth import HTTPTokenAuth
from models import db, Client, Program
from schemas import PROGRAM_SCHEMA, CLIENT_SCHEMA, ENROLL_SCHEMA
from utils import encrypt_data, decrypt_data

executor = ThreadPoolExecutor()
auth = HTTPTokenAuth(scheme='Bearer')

# Mock API keys (replace with database in production)
API_KEYS = {'doctor1': 'secret-token-123'}

@auth.verify_token
def verify_token(token):
    return token in API_KEYS.values()

def register_routes(app, cache):
    @app.route('/programs', methods=['POST'])
    @auth.login_required
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

    @app.route('/clients', methods=['POST'])
    @auth.login_required
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
                name=encrypt_data(data['name']),
                date_of_birth=encrypt_data(data['date_of_birth']),
                gender=data['gender']
            )
            db.session.add(client)
            db.session.commit()
            return jsonify({
                'id': client.id,
                'name': data['name'],
                'date_of_birth': data['date_of_birth'],
                'gender': client.gender,
                'created_at': client.created_at.isoformat()
            }), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/clients/<client_id>/enroll', methods=['POST'])
    @auth.login_required
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

    @app.route('/clients/search', methods=['GET'])
    @auth.login_required
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
                        'name': decrypt_data(client.name),
                        'date_of_birth': decrypt_data(client.date_of_birth),
                        'gender': client.gender
                    }
                    for client in clients
                ]
        
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(executor, search)
        return jsonify(results)

    @app.route('/clients/<client_id>', methods=['GET'])
    @auth.login_required
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
            'name': decrypt_data(client.name),
            'date_of_birth': decrypt_data(client.date_of_birth),
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