from flask_sqlalchemy import SQLAlchemy
import uuid


def get_uuid() -> str:
    return str(uuid.uuid4())

db = SQLAlchemy()
