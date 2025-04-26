class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../health_system.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'
    SECRET_KEY = 'mysecretkey'