from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    booking_count = db.Column(db.Integer, default=0)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='member', lazy=True)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    remaining_count = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)

    bookings = db.relationship('Booking', backref='inventory', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)