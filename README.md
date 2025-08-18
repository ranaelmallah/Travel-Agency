**TravelMate–Project Summary**

TravelMate is a web application designed to manage a travel agency’s operations, 
providing functionalities for both admins and users. Admins can add and manage trips using SQLAlchemy,
including details like destination, price, and dates. Users can browse available trips and book them,
with each booking stored in a JSON file for record-keeping.
The application ensures a smooth user experience
with secure data handling and easy management of trips and bookings
----------------------------------------------------------------------------------------------------------------
**Key Features**
- **User and Admin Roles:** Admins can add and manage trips, while users can browse and book trips.
- **Booking Records in JSON:** All user bookings are securely stored and managed in a JSON file.
- **Trip Management with SQLAlchemy:** Admins can efficiently manage trip details such as destinations, dates, and prices.
- --------------------------------------------------------------------------------------------------------------------------------
**Prerequisites**

To run this project, you need to install the following Python modules:

-Flask: For the web framework.

-Flask-SQLAlchemy: For managing the database and trip models.

-Werkzeug: For secure password hashing (if you use authentication).

-json: For reading and writing booking data to a JSON file.

-os, re, datetime: Built-in Python modules used in the project.


You can install the required modules using pip: 

pip install Flask Flask-SQLAlchemy Werkzeug 

---------------------------------------------------------------------------------------------------------------------------------
Project Checklist
- It is available on GitHub.
- It uses the Flask web framework.
- It uses at least one module from the Python Standard Library other than the random module.
Module name: os , re, datetime
- It contains at least one class written by you that has both properties and methods.
File name for the class definition: crud.py
Line number(s) for the class definition: 9-46
Name of two properties: id,title,description,date, time ,location,price,img  
   
Name of two method: validate()
File name and line numbers where the methods are used: app.py, Name of two methods: validate() , update_user_data(),lines 137,200
- It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- It uses modern JavaScript (for example, let and const rather than var).
- It makes use of the reading and writing to the same file feature.
- It contains conditional statements.
File name: app.py,trips.html
Line number(s): (32,65,94)-(33)
- It contains loops.
File name: trips.html
Line number(s): 34 
- It lets the user enter a value in a text box at some point.
- It doesn't generate any error message even if the user enters a wrong input.
- It is styled using your own CSS.
- The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code.
- All exercises have been completed as per the requirements and pushed to the respective GitHub repository.


