# Car Hire Management System

This is a simple Flask application for a car hire service. It uses MySQL for database operations.

## Features

1. **Home Page**: The home page of the application can be accessed by visiting the '/' route.

2. **Vehicle Management**: The '/vehicles' route allows you to add new vehicles to the database. The vehicle model and price are taken as input.

3. **Customer Management**: The '/customers' route allows you to add new customers to the database. The customer's name, email, and phone number are taken as input. It also displays all the customers in the database.

4. **Booking Management**: The '/bookings' route allows you to create new bookings. The customer ID, vehicle ID, start date, and end date are taken as input. It also checks the hire period, vehicle availability, and whether the booking is in advance. It displays all the bookings for the current date.

5. **Customer Details**: The '/customers/<int:customer_id>' route allows you to view and update the details of a specific customer. It displays the customer's details, their bookings, and the total price for all their bookings.

6. **Delete Customer**: The '/delete_customer/<int:customer_id>' route allows you to delete a specific customer. It deletes all bookings associated with the customer before deleting the customer.

## Database Configuration

The application uses Flask-MySQLdb for database operations. The database configuration is set in the application configuration. The application connects to a MySQL database named 'carhiredb' on 'localhost' with the user 'omar' and password 'Ooooooo7'.

## SQL Commands

The application loads and executes SQL commands from a file named 'tables.sql'. The commands are executed when the application starts.

## Running the Application

To run the application, simply execute the python file. Make sure you have Flask and Flask-MySQLdb installed and a MySQL server running on your machine. (COMMAND>> _python app.py_)
