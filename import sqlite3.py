import sqlite3
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Database initialization
def initialize_database():
    conn = sqlite3.connect('medical_appointments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, time TEXT, 
                 duration INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

# User registration
def register(username, email, password):
    conn = sqlite3.connect('medical_appointments.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()
    print("User registered successfully")

# Schedule appointment
def schedule_appointment(user_id, date, time, duration):
    conn = sqlite3.connect('medical_appointments.db')
    c = conn.cursor()
    c.execute("INSERT INTO appointments (user_id, date, time, duration) VALUES (?, ?, ?, ?)", 
              (user_id, date, time, duration))
    conn.commit()
    conn.close()
    send_reminder(user_id, date, time)

# Send appointment reminder via email
def send_reminder(user_id, date, time):
    conn = sqlite3.connect('medical_appointments.db')
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE id=?", (user_id,))
    user_email = c.fetchone()[0]
    conn.close()

    reminder_message = f"Reminder: Your appointment is scheduled for {date} at {time}"

    sender_email = 'your_email@gmail.com'  # Update with your email
    sender_password = 'your_password'  # Update with your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = 'Appointment Reminder'
    msg.attach(MIMEText(reminder_message, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, msg.as_string())
        print("Reminder email sent successfully")
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Please check your email address and password.")
    except Exception as e:
        print(f"Error sending reminder email: {e}")

if __name__ == '_main_':
    initialize_database()
    register("John Doe", "john@example.com", "password123")
    schedule_appointment(1, "2024-04-04", "10:00", 60)