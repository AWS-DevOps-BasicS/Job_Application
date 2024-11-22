from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# RDS database configuration
DB_HOST = 'your-rds-endpoint'
DB_USER = 'your-username'
DB_PASSWORD = 'your-password'
DB_NAME = 'your-database'

def connect_to_rds():
    """Establish a connection to the RDS database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

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
