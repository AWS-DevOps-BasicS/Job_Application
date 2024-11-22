#!/bin/bash

# Bash script to set up and run the Job Application Flask app

# Variables
APP_DIR="/path/to/job_application" # Change this to your project directory
PYTHON_PATH=$(which python3)       # Path to Python 3
SERVICE_NAME="job_application.service"
DB_HOST="your-rds-endpoint"        # Change to your RDS endpoint
DB_USER="your-username"            # Change to your RDS username
DB_PASSWORD="your-password"        # Change to your RDS password
DB_NAME="your-database"            # Change to your RDS database name

# Functions
function install_dependencies() {
    echo "Installing Python dependencies..."
    pip install -r "$APP_DIR/requirements.txt"
}

function configure_app() {
    echo "Configuring the Flask app with RDS credentials..."
    sed -i "s|DB_HOST = '.*'|DB_HOST = '${DB_HOST}'|" "$APP_DIR/app.py"
    sed -i "s|DB_USER = '.*'|DB_USER = '${DB_USER}'|" "$APP_DIR/app.py"
    sed -i "s|DB_PASSWORD = '.*'|DB_PASSWORD = '${DB_PASSWORD}'|" "$APP_DIR/app.py"
    sed -i "s|DB_NAME = '.*'|DB_NAME = '${DB_NAME}'|" "$APP_DIR/app.py"
}

function setup_database() {
    echo "Setting up the database..."
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$APP_DIR/setup/create_table.sql"
}

function run_flask_app() {
    echo "Starting the Flask app..."
    cd "$APP_DIR"
    $PYTHON_PATH app.py
}

function setup_systemd_service() {
    echo "Setting up systemd service..."
    SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"
    sed "s|/path/to/job_application|$APP_DIR|" "$APP_DIR/setup/job_application.service" > "$SERVICE_PATH"
    sed -i "s|ExecStart=.*|ExecStart=${PYTHON_PATH} $APP_DIR/app.py|" "$SERVICE_PATH"
    systemctl daemon-reload
    systemctl start "$SERVICE_NAME"
    systemctl enable "$SERVICE_NAME"
    echo "Service $SERVICE_NAME has been started and enabled."
}

# Main Menu
echo "Job Application Flask App Setup Script"
echo "-------------------------------------"
echo "1. Install dependencies"
echo "2. Configure app with RDS credentials"
echo "3. Set up database"
echo "4. Run Flask app"
echo "5. Set up as systemd service"
echo "6. Exit"

read -p "Enter your choice [1-6]: " CHOICE

case $CHOICE in
1)
    install_dependencies
    ;;
2)
    configure_app
    ;;
3)
    setup_database
    ;;
4)
    run_flask_app
    ;;
5)
    setup_systemd_service
    ;;
6)
    echo "Exiting setup script."
    ;;
*)
    echo "Invalid option. Exiting."
    ;;
esac
