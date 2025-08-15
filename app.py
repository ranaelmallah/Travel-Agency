from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import json
import os, re
from crud import db, MyTrips
from datetime import datetime
from flask import abort
from flask_bcrypt import Bcrypt
# from user import  User
app = Flask(__name__)
app.secret_key="your_secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///trips.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "False"

db.init_app(app)
def load_admin_data():
    with open("admin.json", "r") as file:
        return json.load(file)

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
    if username == admin_data["username"] and password == admin_data["password"]:
        session["logged_in"] = True
        session["is_admin"] = True
        session["username"] = username
        return jsonify({
            "success": True, 
            "message": "Login successful",
            "redirect": url_for("dashboard")  # Add redirect URL
        })
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

        # try:
        #     # Force JSON parsing if Content-Type suggests JSON
        #     if request.content_type == 'application/json':
        #         data = request.get_json()
        #     else:
        #         data = request.form
                
        #     username = data.get('username')
        #     password = data.get('password')

        #     if not username or not password:
        #         return jsonify({
        #             "success": False, 
        #             "message": "Username and password are required"
        #         }), 400

        #     if username == Admin["username"] and password == Admin["password"]:
        #         session['logged_in'] = True
        #         session['is_admin'] = True
        #         session['username'] = username
        #         response = jsonify({
        #             "success": True, 
        #             "message": "Login successful",
        #             "redirect": url_for('dashboard')
        #         })
        #         return response
            
        #     return jsonify({
        #         "success": False, 
        #         "message": "Invalid credentials, only admin can access"
        #     }), 401
        # except Exception as e:
        #     return jsonify({
        #         "success": False,
        #         "message": f"Server error: {str(e)}"
        #     }), 500
@app.route('/dashboard', methods=["POST", "GET"])
# @login_required
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
# @app.route("/reset-password",methods=["POST","GET"])
# def reset_password():
#     if request.method=="POST":
#         old_password=request.form.get("old_password")
#         new_password=request.form.get("new_password")
#         admin_data=load_admin_data()

 


@app.route('/')
def index():
    trips=MyTrips.query.order_by(MyTrips.date).limit(3).all()
    return render_template('index.html',trips=trips)

@app.route('/trips')
def all_trips():
   trips=MyTrips.query.order_by(MyTrips.date).all()
   return render_template('trips.html', trips=trips)




@app.route('/about')
def about():
    return render_template("about.html")

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)