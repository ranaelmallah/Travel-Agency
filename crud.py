from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime
from datetime import datetime, time
import os
import re

db=SQLAlchemy()

class MyTrips(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(1000),nullable=False)
    date=db.Column(db.Date,nullable=False)
    time = db.Column(db.Time, nullable=True) 
    location=db.Column(db.String(200),nullable=False)
    price=db.Column(db.String(20),nullable=False)
    img = db.Column(db.String(500), nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Trip {self.id}"
    def validate(self):
        # Image
        if not self.img:
            return "No image URL provided"
        if not re.match(r'^https?:\/\/.*\.(png|jpg|jpeg|gif)$', self.img, re.IGNORECASE):
            return "Invalid image URL format"
        # Title
        if not (3 <= len(self.title) <= 200):
            return "Title must be 3-200 characters"

        # Description
        if not (10 <= len(self.description) <= 1000):
            return "Description must be 10-1000 characters"

        # Location
        if not (3 <= len(self.location) <= 200):
            return "Location must be 3-200 characters"

        # Price
        if not re.match(r'^\d+(\.\d{1,2})?$', self.price):
            return "Invalid price format"

        # Passed all validations
        return None