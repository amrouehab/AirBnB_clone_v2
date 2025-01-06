#!/usr/bin/python3
"""Amenity Module for HBNB project using SQLAlchemy"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity

class Amenity(BaseModel, Base):
    """Representation of an Amenity in the database."""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    # Establishing the Many-to-Many relationship with Place
    place_amenities = relationship("Place", secondary=place_amenity, back_populates="amenities")

