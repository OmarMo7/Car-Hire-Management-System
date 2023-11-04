from flask import Flask, request, jsonify, redirect, url_for
from flask import render_template
from flask_mysqldb import MySQL
from datetime import datetime

# from flask.cli import with_appcontext
# import click
# import os


app = Flask(__name__, template_folder='template')
app.config['EXPLAIN_TEMPLATE_LOADING'] = True


# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'omar'
app.config['MYSQL_PASSWORD'] = 'Ooooooo7'
app.config['MYSQL_DB'] = 'carhiredb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)


# Load SQL commands from file and execute them
def load_sql_commands_from_file(filename):
    with open(filename, 'r') as f:
        commands = f.read().split(';')  # split the commands by ';'
        with app.app_context():
            cur = mysql.connection.cursor()
            for command in commands:
                if command.strip():  # ensure the command is not empty
                    cur.execute(command)
                    cur.fetchall()  # Fetch all results before committing
            mysql.connection.commit()
            cur.close()


# Load and execute SQL commands from "table.sql" file
load_sql_commands_from_file('./tables.sql')

# print(result)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/vehicles', methods=['GET', 'POST'])
def vehicle():
    if request.method == 'POST':
        vehicle_model = request.form['vehicle_model']
        price = request.form['price']
        # Add the vehicle to the database
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO vehicles (model, price) VALUES (%s, %s)",
            (vehicle_model, price)
        )
        mysql.connection.commit()
        cur.close()
        # return jsonify(message='Customer added successfully')
    return render_template('vehicles.html')


@app.route('/customers', methods=['GET', 'POST'])
def customers():
    customers = []
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        # Add the customer to the database
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('customers'))

    # Get all customers
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()

    mysql.connection.commit()
    cur.close()
    return render_template('customers.html', customers=customers)


@app.route('/bookings', methods=['GET', 'POST'])
def booking():
    message = ''
    bookings_today = []
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        vehicle_id = request.form['vehicle_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        start_date_stripped = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_stripped = datetime.strptime(end_date, '%Y-%m-%d')

        # Check hire period
        hire_period = (end_date_stripped - start_date_stripped).days
        if hire_period > 7:
            return jsonify(message='Cannot hire a car for more than a week')
        print(hire_period)

        # Check vehicle availability
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM bookings WHERE vehicle_id = %s AND start_date < %s AND end_date > %s",
            (vehicle_id, end_date, start_date)
        )
        if cur.fetchone() is not None:
            return jsonify(message='Vehicle is not available for the requested period')

        cur.execute(
            "SELECT price FROM vehicles WHERE vehicle_id = %s",
            (vehicle_id,)
        )
        price = cur.fetchone()
        price = price['price']

        # Check if the booking is in advance
        today = datetime.today().date()
        if start_date_stripped.date() > today:
            message = 'You made a booking in advance.'

        # Get the current date as a string in the format 'YYYY-MM-DD'
        today = datetime.today().strftime('%Y-%m-%d')
        cur.execute(
            "SELECT * FROM bookings WHERE DATE(start_date) = %s", (today,))
        bookings_today = cur.fetchall()

        # Create booking
        cur.execute(
            "INSERT INTO bookings (customer_id, vehicle_id, booking_date, start_date, end_date, price) VALUES (%s, %s, NOW(), %s, %s, %s)",
            (customer_id, vehicle_id, start_date, end_date, price)
        )

        mysql.connection.commit()

        cur.close()

    return render_template('bookings.html', bookings_today=bookings_today, message=message)





if __name__ == '__main__':
    app.run()
