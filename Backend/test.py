from main import db, User, app, Passwords, logs
import time
import numpy as np
from flask import jsonify
#with app.app_context():

# Create a new user object
start_time = time.time()


with app.app_context():
    log = logs.query.filter_by(sid="52ced965-c8e5-45a1-ac5f-4dea6968913b").first()

    # Check if the user exists
    if log:
        print(log)
        print("User found:")
        print(f"log: {log.user_id}")
    else:
        print("User not found.")
"""
with app.app_context():
    passwords = Passwords.query.filter_by(user_id=1).all()
    if passwords:
        password_data = np.array([])
        for password in passwords:
            password_data = np.append(password_data,
                                      {"id": password.id, 'user_id': password.user_id, "password": password.password})
            print(password_data)
    else:
        print("Passwords not found")
"""
"""
with app.app_context():
    new_password = Passwords(user_id=1, password="DoamneAjuta2")
    db.session.add(new_password)
    db.session.commit()
"""



end_time = time.time()
runtime = end_time - start_time
print("Runtime:", runtime, "seconds")