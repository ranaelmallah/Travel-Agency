from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import json
import os, re
from crud import db, MyTrips
from datetime import datetime
from flask import abort
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from user import  User
app = Flask(__name__)
app.secret_key="your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///trips.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "False"

db.init_app(app)


@app.route('/')
def index():
    trips=MyTrips.query.order_by(MyTrips.date).limit(3).all()
    return render_template('index.html',trips=trips)

@app.route('/trips')
def all_trips():
   trips=MyTrips.query.order_by(MyTrips.date).all()
   return render_template('trips.html', trips=trips)



@app.route('/login')
def login():
    return render_template("login.html")
    # if request.method=='POST':
    #     username=request.form['username']
    #     password=request.form['password']

@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/dashboard', methods=["POST", "GET"])
# @login_required
def dashboard():

    if request.method == "POST":
        try:
            date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(request.url)

        time_obj = None
        time_str = request.form.get('time')
        if time_str:
            try:
                time_obj = datetime.strptime(time_str, '%H:%M').time()
            except ValueError:
                flash('Invalid time format', 'danger')
                return redirect(request.url)

        # Create new trip object
        new_trip = MyTrips(
            title=request.form.get('title', '').strip(),
            description=request.form.get('description', '').strip(),
            date=date,
            time=time_obj,
            location=request.form.get('location', '').strip(),
            price=request.form.get('price', '').strip(),
            img=request.form.get('img', '').strip()
        )

        # Validate using class method
        error = new_trip.validate()
        if error:
            flash(error, 'danger')
            return redirect(request.url)

        try:
            db.session.add(new_trip)
            db.session.commit()
            flash('Trip added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving trip: {str(e)}', 'danger')
            return redirect(request.url)

    trips = MyTrips.query.order_by(MyTrips.date).all()
    return render_template("dashboard.html", trips=trips)

    # if request.method == "POST":
        
    #     img = request.form.get('img', '').strip()
    #     if not img:
    #         flash('No image URL provided', 'danger')
    #         return redirect(request.url)
        
    #     if not re.match(r'^https?:\/\/.*\.(png|jpg|jpeg|gif)$', img, re.IGNORECASE):
    #         flash('Invalid image URL format', 'danger')
    #         return redirect(request.url)
    #     # Validate other fields
    #     title = request.form.get('title', '').strip()
    #     if not (3 <= len(title) <= 200):
    #         flash('Title must be 3-200 characters', 'danger')
    #         return redirect(request.url)

    #     description = request.form.get('description', '').strip()
    #     if not (10 <= len(description) <= 1000):
    #         flash('Description must be 10-1000 characters', 'danger')
    #         return redirect(request.url)

    #     try:
    #         date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    #     except ValueError:
    #         flash('Invalid date format', 'danger')
    #         return redirect(request.url)

    #     location = request.form.get('location', '').strip()
    #     if not (3 <= len(location) <= 200):
    #         flash('Location must be 3-200 characters', 'danger')
    #         return redirect(request.url)

    #     price = request.form.get('price', '').strip()
    #     if not re.match(r'^\d+(\.\d{1,2})?$', price):
    #         flash('Invalid price format', 'danger')
    #         return redirect(request.url)

    #     # Process time if provided
    #     time_str = request.form.get('time')
    #     time_obj = None
    #     if time_str:
    #         try:
    #             time_obj = datetime.strptime(time_str, '%H:%M').time()
    #         except ValueError:
    #             flash('Invalid time format', 'danger')
    #             return redirect(request.url)

    #     # If all validations pass, create the trip
    #     try:
    #         new_trip = MyTrips(
    #             title=title,
    #             description=description,
    #             date=date,
    #             time=time_obj,
    #             location=location,
    #             price=price,
    #             img=img
    #         )
    #         db.session.add(new_trip)
    #         db.session.commit()
            
    #         # Save the actual file
           
    #         flash('Trip added successfully!', 'success')
    #         return redirect(url_for('dashboard'))
        
    #     except Exception as e:
    #         db.session.rollback()
    #         flash(f'Error saving trip: {str(e)}', 'danger')
    #         return redirect(request.url)

    # trips = MyTrips.query.order_by(MyTrips.date).all()
    # return render_template("dashboard.html", trips=trips)

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_trip=MyTrips.query.get_or_404(id)
    try:
       db.session.delete(delete_trip)
       db.session.commit()
       return redirect(url_for("dashboard"))
    except Exception as e :
        return f"Error:{e}"

@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    trip = MyTrips.query.get_or_404(id)

    if request.method == "POST":
        try:
            date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(request.url)

        time_obj = None
        time_str = request.form.get('time')
        if time_str:
            try:
                time_obj = datetime.strptime(time_str, '%H:%M').time()
            except ValueError:
                flash('Invalid time format', 'danger')
                return redirect(request.url)

        # Update trip fields from form
        trip.title = request.form.get('title', '').strip()
        trip.description = request.form.get('description', '').strip()
        trip.date = date
        trip.time = time_obj
        trip.location = request.form.get('location', '').strip()
        trip.price = request.form.get('price', '').strip()
        trip.img = request.form.get('img', '').strip()

        # Validate using the model's method
        error = trip.validate()
        if error:
            flash(error, 'danger')
            return redirect(request.url)

        try:
            db.session.commit()
            flash('Trip updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating trip: {str(e)}', 'danger')
            return redirect(request.url)

    # For GET request, show the current trip data
    return render_template("update_trip.html", trip=trip)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)