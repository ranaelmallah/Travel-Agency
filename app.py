from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os, re
from crud import db, MyTrips
from datetime import datetime

hashed_pw = generate_password_hash("admin882000")

admin_data = {
    "username": "Rana Mousa",
    "password": hashed_pw
}
with open("admin.json", "w") as f:
    json.dump(admin_data, f, indent=4)
# from user import  User
app = Flask(__name__)
app.secret_key="your_secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///trips.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "False"

db.init_app(app)
# load admin data 
def load_admin_data():
    with open("admin.json", "r") as file:
        return json.load(file)
# read and write user data 
BOOKINGS_FILE = "bookings.json"

def load_bookings():
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "w") as f:
            json.dump([], f)
    with open(BOOKINGS_FILE, "r") as f:
        return json.load(f)

def save_bookings(bookings):
    with open(BOOKINGS_FILE, "w") as f:
        json.dump(bookings, f, indent=4)


@app.context_processor
def inject_role():
    return dict(is_admin=session.get('is_admin', False))

@app.route('/')
def index():
    trips=MyTrips.query.order_by(MyTrips.date).limit(3).all()  
    return render_template('index.html',trips=trips)
#  ============================trips route============================

@app.route('/trips')
def all_trips():
   trips=MyTrips.query.order_by(MyTrips.date).all()
   return render_template('trips.html', trips=trips)
#  ============================about route============================
@app.route('/about')
def about():
    return render_template("about.html")  
#  ============================login route============================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required"}), 400

    admin_data = load_admin_data()
    if (
        username == admin_data["username"] and 
        check_password_hash(admin_data["password"], password)):
        session["logged_in"] = True
        session["is_admin"] = True
        session["username"] = username
        return jsonify({
            "success": True, 
            "message": "Login successful",
            "redirect": url_for("dashboard")  
        })
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

#  ============================dashboard route============================

@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    if not session.get('logged_in')or not session.get('is_admin'):
        return redirect(url_for('login'))
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
#  validate the date must be in the future
        current_date = date.today().strftime('%Y-%m-%d')
        try:

            trip_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            if trip_date < date.today():
                flash('Trip date must be in the future', 'danger')
                trips = MyTrips.query.order_by(MyTrips.date).all()
                bookings = load_bookings()
                return render_template("dashboard.html", trips=trips, bookings=bookings, current_date=date.today().strftime('%Y-%m-%d'))
        except ValueError:

            flash('Invalid date format', 'danger')
            return redirect(request.url)
        # Validate using class method
        error = new_trip.validate()
        if error:
            flash(error, 'danger')
            trips = MyTrips.query.order_by(MyTrips.date).all()
            bookings = load_bookings()
            return render_template("dashboard.html", trips=trips, bookings=bookings)

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
    bookings = load_bookings()
    return render_template("dashboard.html", trips=trips,bookings=bookings)
#  ============================delete-trip route============================
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_trip=MyTrips.query.get_or_404(id)
    try:
       db.session.delete(delete_trip)
       db.session.commit()
       return redirect(url_for("dashboard"))
    except Exception as e :
        return f"Error:{e}"
#  ============================update-trip route============================
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
                try:
                    time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
                except ValueError:
                    flash('Invalid time format', 'danger')
                    return redirect(request.url)
                

        trip.title = request.form.get('title', '').strip()
        trip.description = request.form.get('description', '').strip()
        trip.date = date
        trip.time = time_obj
        trip.location = request.form.get('location', '').strip()
        trip.price = request.form.get('price', '').strip()
        trip.img = request.form.get('img', '').strip()

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

    
    return render_template("update_trip.html", trip=trip)
#  ============================user-book route============================

@app.route("/book", methods=["GET", "POST"])
def book():
    trip_id = request.args.get("trip_id", None)  

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
      
        if not re.match(r"^[A-Za-z\s]{3,}$", name):
            flash("Name must be at least 3 letters and contain only letters and spaces.", "danger")
            return redirect(request.url)

        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            flash("Invalid email address.", "danger")
            return redirect(request.url)

        if not re.match(r"^\d{7,}$", phone):
            flash("Phone number must be at least 7 digits and numbers only.", "danger")
            return redirect(request.url)

        if len(address) < 5:
            flash("Address must be at least 5 characters long.", "danger")
            return redirect(request.url)

        

        # Save booking including trip_id
        bookings = load_bookings()
        bookings.append({
            "trip_id": trip_id,   
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
           
        })
        save_bookings(bookings)

        flash("Booking successful!", "success")
        return redirect(url_for("index", trip_id=trip_id))

    return render_template("book.html", trip_id=trip_id)

#  ============================logout  route============================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)