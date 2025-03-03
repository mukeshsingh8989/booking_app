from flask import Flask, request, jsonify, render_template
from models import db, Member, Inventory, Booking
import csv
from datetime import datetime
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

MAX_BOOKINGS = 2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'members' in request.files:
        members_file = request.files['members']
        members_file.save('uploads/members.csv')
        load_members_from_csv('uploads/members.csv')
    if 'inventory' in request.files:
        inventory_file = request.files['inventory']
        inventory_file.save('uploads/inventory.csv')
        load_inventory_from_csv('uploads/inventory.csv')
    return jsonify({"message": "Files uploaded and data loaded successfully"}), 200

def load_members_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            member = Member(
                name=row['name'],
                surname=row['surname'],
                booking_count=int(row['booking_count']),
                date_joined=datetime.strptime(row['date_joined'], '%Y-%m-%d %H:%M:%S')
            )
            db.session.add(member)
        db.session.commit()

def load_inventory_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            inventory = Inventory(
                title=row['title'],
                description=row['description'],
                remaining_count=int(row['remaining_count']),
                expiration_date=datetime.strptime(row['expiration_date'], '%d/%m/%Y')
            )
            db.session.add(inventory)
        db.session.commit()

@app.route('/book', methods=['POST'])
def book_item():
    data = request.get_json()
    member_id = data.get('member_id')
    inventory_id = data.get('inventory_id')

    member = Member.query.get(member_id)
    inventory = Inventory.query.get(inventory_id)

    if not member or not inventory:
        return jsonify({"error": "Member or Inventory not found"}), 404

    if member.booking_count >= MAX_BOOKINGS:
        return jsonify({"error": "Member has reached the maximum number of bookings"}), 400

    if inventory.remaining_count <= 0:
        return jsonify({"error": "No remaining inventory"}), 400

    booking = Booking(member_id=member_id, inventory_id=inventory_id)
    db.session.add(booking)
    member.booking_count += 1
    inventory.remaining_count -= 1

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Booking failed"}), 500

    return jsonify({"message": "Booking successful", "booking_id": booking.id}), 201

@app.route('/cancel', methods=['POST'])
def cancel_booking():
    data = request.get_json()
    booking_id = data.get('booking_id')

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    member = booking.member
    inventory = booking.inventory

    member.booking_count -= 1
    inventory.remaining_count += 1

    db.session.delete(booking)
    db.session.commit()

    return jsonify({"message": "Booking cancelled successfully"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)