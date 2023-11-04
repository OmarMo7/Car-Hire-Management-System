from flask import Flask
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
                    result = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            return result

# Load and execute SQL commands from "table.sql" file
result = load_sql_commands_from_file('./tables.sql')



if __name__ == '__main__':
    app.run()
