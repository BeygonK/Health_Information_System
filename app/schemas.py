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