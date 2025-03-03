# Flask Booking System

This is a Flask-based booking system that allows users to upload CSV data, manage members and inventory, and book or cancel inventory items.

## Features
- Upload CSV files for members and inventory via a web form.
- Book an inventory item for a member, ensuring constraints (max 2 bookings per member, sufficient inventory count).
- Cancel a booking using a booking reference.
- Uses Flask, SQLAlchemy, and SQLite/PostgreSQL.

## Installation

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd flask-booking-system
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv  # or use `python3`
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```sh
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. Run the application:
   ```sh
   flask run
   ```

## Endpoints

- **Upload CSV Data**: `/upload`
- **Book an Item**: `/book`
- **Cancel a Booking**: `/cancel`

## Environment Variables

Create a `.env` file in the root directory and set:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///booking.db  # Or PostgreSQL URL
```

## License
This project is licensed under the MIT License.

