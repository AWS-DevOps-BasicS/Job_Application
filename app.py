from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# RDS database configuration
DB_HOST = 'jobapplication.c3wsqegimvwi.ap-northeast-3.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'naresh123456'
DB_NAME = 'jobapplication'

def connect_to_rds():
    """Establish a connection to the RDS database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            connection.commit()
    finally:
        connection.close()

def create_table_if_not_exists():
    """Create the table if it doesn't exist."""
    connection = connect_to_rds()
    try:
        with connection.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS applicants (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                phone VARCHAR(15),
                position VARCHAR(100),
                experience TEXT,
                skills TEXT,
                education TEXT
            )
            """
            cursor.execute(create_table_query)
            connection.commit()
    finally:
        connection.close()

@app.before_first_request
def setup():
    """Ensure database and table exist before processing any requests."""
    create_database_if_not_exists()
    create_table_if_not_exists()

@app.route('/')
def index():
    """Render the job application form."""
    return render_template('job_form.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission and save details to the database."""
    try:
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        position = request.form['position']
        experience = request.form['experience']
        skills = request.form['skills']
        education = request.form['education']
        
        # Connect to RDS and insert data
        connection = connect_to_rds()
        cursor = connection.cursor()
        query = """
        INSERT INTO applicants (name, email, phone, position, experience, skills, education)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, phone, position, experience, skills, education))
        connection.commit()
        
        message = "Application submitted successfully!"
    except Exception as e:
        message = f"Error: {e}"
    finally:
        cursor.close()
        connection.close()

    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
