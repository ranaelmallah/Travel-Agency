from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime
from datetime import datetime, time
import os
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