#!/usr/bin/python3
"""Place Module for HBNB project"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models

# Association table for many-to-many relationship between Place and Amenity
place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"), primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"), primary_key=True, nullable=False)
)

class Place(BaseModel, Base):
    """A place to stay"""
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    # Relationship for DBStorage
    amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)

    if models.storage.__class__.__name__ != "DBStorage":
        @property
        def amenities(self):
            """Getter attribute for amenities in FileStorage"""
            amenity_list = []
            for amenity_id in self.amenity_ids:
                amenity = models.storage.get(Amenity, amenity_id)
                if amenity:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """Setter attribute for amenities in FileStorage"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
