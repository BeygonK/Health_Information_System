from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

db = SQLAlchemy()

# models for Program
class Program(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# models for Client
class Client(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)  # Store encrypted
    date_of_birth = db.Column(db.String(100), nullable=False)  # Store encrypted
    gender = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrolled_programs = db.relationship('Program', secondary='enrollment')

enrollment = db.Table('enrollment',
    db.Column('client_id', db.String(36), db.ForeignKey('client.id')),
    db.Column('program_id', db.String(36), db.ForeignKey('program.id'))
)