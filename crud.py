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
        if not re.match(r'^[A-Za-z\s,\-]+$', self.title):
             return "Title must contain only letters, spaces, commas, or hyphens"

        # Description
        if not (10 <= len(self.description) <= 1000):
            return "Description must be 10-1000 characters"
        if not re.match(r'^[A-Za-z0-9\s.,-]+$', self.description):
            return "Description must contain only letters, numbers, spaces, periods, commas, and hyphens"

        # Reject if it's only numbers
        if self.description.isdigit():
            return "Description cannot be numbers only"
        # Location
        if not (3 <= len(self.location) <= 200):
            return "Location must be 3-200 characters" 
        if not re.match(r'^[A-Za-z0-9\s]+$', self.location):
            return "location must contain only letters, numbers, and spaces"
        if self.location.isdigit():
            return "location cannot be numbers only"
        # Price
        if not re.match(r'^\d+(\.\d{1,2})?$', self.price):
            return "Invalid price format"
        if not (2<=len(self.price)<=6):
             return "Price must be between 2 and 6 characters long"
        # Time
        if not self.time:
            return "Time is required"
       
        # Passed all validations
        return None