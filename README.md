Here’s the content formatted as a proper `README.md` file:

---

# **Job Application System**

## **Description**
A Flask-based web application for collecting job applications and storing applicant details in Amazon RDS without requiring resumes.

---

## **Project Structure**
```
job_application/
├── app.py               # Main Flask application
├── templates/
│   └── job_form.html    # HTML form template
├── setup/
│   ├── create_table.sql # SQL script to set up the RDS table
│   └── job_application.service # Systemd service file
├── requirements.txt     # Dependencies for the project
└── README.md            # Project instructions
```

---

## **Setup**

### **1. Prerequisites**
- Python 3.6 or later
- Pip package manager
- Amazon RDS instance
- A Linux environment to host the application

### **2. Clone the Repository**
```bash
git clone https://github.com/your-repo/job_application.git
cd job_application
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Your RDS Database**
Edit the `app.py` file and update the following placeholders:
```python
DB_HOST = 'your-rds-endpoint'
DB_USER = 'your-username'
DB_PASSWORD = 'your-password'
DB_NAME = 'your-database'
```

### **5. Create the Database Table**
Run the SQL script to set up the `applicants` table in your RDS instance:
```bash
mysql -h your-rds-endpoint -u your-username -p your-database < setup/create_table.sql
```

### **6. Run the Flask Application**
Start the application:
```bash
python app.py
```

The app will run at `http://<your-server-ip>:5000`.

---

## **Optional: Running as a Systemd Service**

### **1. Copy the Service File**
Modify the placeholders in `setup/job_application.service`:
- Replace `your_username` with your Linux user.
- Replace `your_group` with your user group.
- Replace `/path/to/job_application` with the absolute path to your project directory.
- Update the Python executable path (`/usr/bin/python3`).

Copy the service file to the systemd directory:
```bash
sudo cp setup/job_application.service /etc/systemd/system/
```

### **2. Enable the Service**
Reload systemd to recognize the service:
```bash
sudo systemctl daemon-reload
```

Start and enable the service:
```bash
sudo systemctl start job_application.service
sudo systemctl enable job_application.service
```

### **3. Verify the Service**
Check the service status:
```bash
sudo systemctl status job_application.service
```

---

## **Access the Application**
- Open your browser and navigate to: `http://<your-server-ip>:5000`
- Fill out the job application form, and the details will be saved in your RDS database.

---

## **Project Files**

### **1. Flask Application (`app.py`)**
Contains the backend logic for rendering the form and saving applicant details to the RDS database.

### **2. HTML Form (`templates/job_form.html`)**
Provides the user interface for applicants to submit their information.

### **3. Database Setup Script (`setup/create_table.sql`)**
SQL script to create the `applicants` table.

### **4. Systemd Service (`setup/job_application.service`)**
Configuration file for running the application as a Linux service.

### **5. Dependencies (`requirements.txt`)**
Lists Python dependencies required for the project:
```
flask
pymysql
```

Install them with:
```bash
pip install -r requirements.txt
```
