#!/usr/bin/python3
"""Initialize the storage engine"""
import os

# Import models for registering with SQLAlchemy
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review

# Choose the storage type based on environment variable
storage_type = os.getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()

# Dictionary for class references (used in DBStorage)
classes = {
    "State": State,
    "City": City,
    "User": User,
    "Place": Place,
    "Amenity": Amenity,
    "Review": Review
}

