from flask import Flask,render_template,request,flash,redirect,url_for
import json
from crud import db, MyTrips
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key="your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///trips.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "False"

db.init_app(app)

def load_trips():
    with open('trips.json', 'r', encoding='utf-8') as f:  
        return json.load(f)['trips']

@app.route('/')
def index():
    trips = load_trips()
    featured_trips = trips[:3]  
    return render_template('index.html', featured_trips=featured_trips) 

@app.route('/trips')
def all_trips():
    trips = load_trips()
    return render_template('trips.html', trips=trips)


@app.route('/login')
def login():
    return render_template("login.html")
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import os, re

@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    if request.method == "POST":
        
        img = request.form.get('img', '').strip()
        if not img:
            flash('No image URL provided', 'danger')
            return redirect(request.url)
        
        if not re.match(r'^https?:\/\/.*\.(png|jpg|jpeg|gif)$', img, re.IGNORECASE):
            flash('Invalid image URL format', 'danger')
            return redirect(request.url)
        # Validate other fields
        title = request.form.get('title', '').strip()
        if not (3 <= len(title) <= 200):
            flash('Title must be 3-200 characters', 'danger')
            return redirect(request.url)

        description = request.form.get('description', '').strip()
        if not (10 <= len(description) <= 1000):
            flash('Description must be 10-1000 characters', 'danger')
            return redirect(request.url)

        try:
            date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(request.url)

        location = request.form.get('location', '').strip()
        if not (3 <= len(location) <= 200):
            flash('Location must be 3-200 characters', 'danger')
            return redirect(request.url)

        price = request.form.get('price', '').strip()
        if not re.match(r'^\d+(\.\d{1,2})?$', price):
            flash('Invalid price format', 'danger')
            return redirect(request.url)

        # Process time if provided
        time_str = request.form.get('time')
        time_obj = None
        if time_str:
            try:
                time_obj = datetime.strptime(time_str, '%H:%M').time()
            except ValueError:
                flash('Invalid time format', 'danger')
                return redirect(request.url)

        # If all validations pass, create the trip
        try:
            new_trip = MyTrips(
                title=title,
                description=description,
                date=date,
                time=time_obj,
                location=location,
                price=price,
                img=img
            )
            db.session.add(new_trip)
            db.session.commit()
            
            # Save the actual file
           
            flash('Trip added successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving trip: {str(e)}', 'danger')
            return redirect(request.url)

    trips = MyTrips.query.order_by(MyTrips.date).all()
    return render_template("dashboard.html", trips=trips)

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_trip=MyTrips.query.get_or_404(id)
    try:
       db.session.delete(delete_trip)
       db.session.commit()
       return redirect(url_for("dashboard"))
    except Exception as e :
        return f"Error:{e}"



    # if request.method=="POST":
    #     title=request.form['title']
    #     description=request.form['description']
    #     date_str=request.form['date']
    #     location=request.form['location']
    #     price=request.form['price']
    #     time_str = request.form.get['time']
    #     img= request.form.get['img']
        
    #     try:
    #         date=datetime.strptime(date_str,'%Y-%m-%d')
    #         time=datetime.strptime(time_str,'%H:%M').time()



    #         new_trip=MyTrips(title=title,
    #             description=description,
    #             date=date,
    #             time=trip_time,
    #             location=location,
    #             price=price,
    #             img=img)
    #         db.session.add(new_trip)
    #         db.session.commit()
    #         return redirect(url_for('dashboard'))

    #     except Exception as e:
    #         print(f"Error:{e}")
    #         return f"Error:{e}"

    # trips=MyTrips.query.order_by(MyTrips.date).all()
    # return render_template("dashboard.html",trips=trips)
# @app.route('/crud',methods=['POST','GET'])
# def crud():

    
    


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)