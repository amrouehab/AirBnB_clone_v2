#!/usr/bin/python3
"""DBStorage Module for HBNB project"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os


class DBStorage:
    """Database storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}',
            pool_pre_ping=True
        )
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects by class or all objects"""
        results = {}
        if cls:
            objects = self.__session.query(cls).all()
        else:
            from models import classes
            objects = []
            for class_type in classes.values():
                objects.extend(self.__session.query(class_type).all())

        for obj in objects:
            key = f"{obj.__class__.__name__}.{obj.id}"
            results[key] = obj
        return results

    def new(self, obj):
        """Add a new object to the session"""
        self.__session.add(obj)

    def save(self):
        """Commit changes to the session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload the database session"""
        from models import classes
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

