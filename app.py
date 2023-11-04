from flask import Flask, request, jsonify
from flask_mysqldb import MySQL



app = Flask(__name__, template_folder='template')
app.config['EXPLAIN_TEMPLATE_LOADING'] = True


# Configure MySQL connection parameters
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
        commands = f.read().split(';') 
        with app.app_context():
            cur = mysql.connection.cursor()
            for command in commands:
                if command.strip():  
                    cur.execute(command)
                    cur.fetchall()
            mysql.connection.commit()
            cur.close()

# Load and execute SQL commands from "table.sql" file
load_sql_commands_from_file('./tables.sql')

@app.route('/customer', methods=['POST'])
def add_customer():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
        (name, email, phone)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify(message='Customer added successfully')


@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE customers SET name = %s, email = %s, phone = %s WHERE customer_id = %s",
        (name, email, phone, customer_id)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify(message='Customer updated successfully')


@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify(message='Customer deleted successfully')


@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers WHERE customer_id = %s",
                (customer_id,))
    customer = cur.fetchone()
    cur.close()

    if customer:
        return jsonify(customer)
    else:
        return jsonify(message='Customer not found'), 404

if __name__ == '__main__':
    app.run()
