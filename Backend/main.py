from datetime import datetime
#import face_recognition
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import base64
import cv2
import os
import random
import numpy as np
import uuid
import json
from MTCNN_module import get_image_tensor

import tensorflow as tf
from tensorflow.keras.layers import Layer
from crypt import floats_to_bytestring, concatenate_with_encryption_key, encrypt_password, decrypt_password, get_encryption_key_bytes
from QR import generate_qr_for_2fa
import pyotp

cwd = os.getcwd()
print(cwd)

def form_encryption_key(id):
    user = User.query.filter_by(id=id).first()
    embedding_crypted = user.embedding
    embedding = decrypt_password(embedding_crypted, get_encryption_key_bytes())
    array_string = np.fromstring(embedding[1:-1], sep=',')
    byte_string = floats_to_bytestring(array_string)
    byte_string = concatenate_with_encryption_key(byte_string)
    return byte_string



def get_user_by_id(id):

        user = User.query.filter_by(id=id).first()

        # Check if the user exists
        if user:
            print(user)
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'image': user.image_name,
            }
        else:
            print("User not found.")


        return user_data

def get_user_passwords_by_user_id(id):

        passwords = Password.query.filter_by(user_id=id).all()
        if passwords:
            passwords_data = []
            #Pozitie nouă
            x = form_encryption_key(id)
            for password in passwords:
                #Pozitie veche
                #x = form_encryption_key(id)
                placeholder = decrypt_password(password.password, x)
                passwords_data.append({"id": password.id,
                                       'user_id': password.user_id,
                                       "password": placeholder,
                                       "name": password.name,
                                       "date_created": password.date_created,
                                       "date_modified": password.date_modified})
        else:
            return "Passwords not found"
        return passwords_data

def new_sid(id):

    try:
        with db.session() as session:
            sid = str(uuid.uuid4())
            new_sid = Sid(user_id=id, sid=sid, date_create=datetime.now())
            session.add(new_sid)
            session.commit()
            return sid
    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        print(f"Error adding sid: {e}")
        # Roll back the session to revert any changes
        session.rollback()
        # Return False to indicate failure
        return False

def add_password(user_id, password, password_name):
    try:
        with db.session() as session:
            # Create a new Password object
            x = form_encryption_key(user_id)
            x = encrypt_password(password, x)
            new_password = Password(user_id=user_id, password=x, password_name=password_name,)
            session.add(new_password)
            session.commit()

            # Return True to indicate success
            return True
    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        print(f"Error adding password: {e}")
        # Roll back the session to revert any changes
        session.rollback()
        # Return False to indicate failure
        return False


def preprocess(image):

    # resizing and scaling
    img = tf.image.resize(image, (105, 105))
    img = img / 255.0
    return img

def verify_sid(sid):
    x = Sid.query.filter_by(sid=sid).first()
    if x:
        if x.sid == sid:
            print(x.date_create)
            return x.user_id

    return 0

def get_embedding(json):
    start = time.time()
    embedding_login = get_image_tensor(json)
    if (type(embedding_login) == type(None)):
        return 0
    end = time.time()
    print("timp prelucrare imagine de login:", end - start)

    prediction = model.predict(embedding_login)
    print("timp creare embedding pentru imagine de login:", time.time() - end)
    end = time.time()
    return prediction

def authentificate(prediction):

    x = User.query.all()
    for i in x:
        embedding = decrypt_password(i.embedding, get_encryption_key_bytes())
        array_back = np.fromstring(embedding[1:-1], sep=',')
        array_back = np.expand_dims(array_back, axis=0)
        distance = np.linalg.norm(prediction - array_back)
        print("distanta:", distance)
        if distance < 1.4:
            print("User:", i.username)
            return i.id
    print("User not found.")
    return 0


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nopass:Horse#Cactus$nirVana2@localhost/nopassmanager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Action(db.Model):
    __tablename__ = 'ACTION'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.BigInteger, nullable=False)

class User(db.Model):
    __tablename__ = 'USER'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    embedding = db.Column(db.String(5000), nullable=False)
    last_logon = db.Column(db.DateTime, default=datetime, nullable=False)

class Password(db.Model):
    __tablename__ = 'PASSWORD'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('USER.id'), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime, nullable=False)
    date_modified = db.Column(db.DateTime, default=datetime, nullable=False)

    user = db.relationship('User', backref=db.backref('passwords', lazy=True))

class Log(db.Model):
    __tablename__ = 'LOG'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    action_id = db.Column(db.BigInteger, db.ForeignKey('ACTION.id'), nullable=False)
    sid_id = db.Column(db.BigInteger, db.ForeignKey('SID.sid'), nullable=False)
    freetext_1 = db.Column(db.String(255), nullable=True)
    freetext_2 = db.Column(db.String(255), nullable=True)
    freetext_3 = db.Column(db.String(255), nullable=True)
    date_create = db.Column(db.DateTime, default=datetime, nullable=False)

    action = db.relationship('Action', backref=db.backref('logs', lazy=True))
    sid = db.relationship('Sid', backref=db.backref('logs', lazy=True))

class Sid(db.Model):
    __tablename__ = 'SID'
    sid = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('USER.id'), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime, nullable=False)

    user = db.relationship('User', backref=db.backref('sids', lazy=True))

'''
@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        # Attempt to query the User table
        users = User.query.all()
        # If the query is successful, return a success message with user count
        return jsonify({"message": "Connection successful!", "user_count": len(users)}), 200
    except Exception as e:
        # If there's an error, return the error message
        return jsonify({"error": str(e)}), 500
'''

@app.route('/authentificate', methods=['POST'])
def handle_post_auth():
    # Check if the request contains JSON data
    if request.is_json:
        sid = 0
        data = request.get_json()
        prediction = get_embedding(data)
        valid = authentificate(prediction)
        if valid != 0:


        # Process the data (this is just an example)
            response = {
                "message": "Data received successfully!",
                "received_data": data,
                "id" : valid
            }
            return jsonify(response), 200
        return jsonify({"message": "USER NOT FOUND"}), 400
    else:
        return jsonify({"message": "Request must be JSON"}), 400


@app.route('/signup', methods=['POST'])
def handle_post_signup():
    # Step 1: Receive username, email, and image
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    image_base64 = data.get('image')

    if not username or not email or not image_base64:
        return jsonify({"error": "username, email, and image are required"}), 400

    prediction = get_embedding(data)
    valid = authentificate(prediction)
    #valid = 0 #placeholder
    if valid == 0:

        # Step 2: Generate a secret key for OTP (2FA)
        a = np.asarray(prediction)
        embedding_database = np.array2string(a, separator=',')

        prediction_bytestring = floats_to_bytestring(prediction[0])
        secret_key = concatenate_with_encryption_key(prediction_bytestring)
        base32_secret_key = base64.b32encode(secret_key[:16] + secret_key[-16:]).decode('utf-8')

        qr_base64 = generate_qr_for_2fa(username, base32_secret_key)
        prediction_string = np.array2string(prediction[0], separator=',')
        prediction_encrypted = encrypt_password(prediction_string, get_encryption_key_bytes())
        print(prediction_encrypted)
        temp_user_data[username] = {'email': email, 'secret_key': base32_secret_key, 'image': prediction_encrypted}
        print(temp_user_data[username])

        return jsonify({"qr_code": qr_base64,
                        "message": 'Successful',
                        "username": username}), 200
    else: return jsonify({"message": "User already registered"}), 400

@app.route('/check-otp', methods=['POST'])
def handle_post_check_otp():
    data = request.get_json()
    id = data.get('id')
    otp = data.get('otp')
    user = User.query.filter_by(id=id).first()

    encrypted_embedding = user.embedding
    decrypted_embedding = decrypt_password(encrypted_embedding, get_encryption_key_bytes())
    decrypted_embedding_array = np.fromstring(decrypted_embedding[1:-1], sep=',')
    byte_string = floats_to_bytestring(decrypted_embedding_array)

    byte_string = concatenate_with_encryption_key(byte_string)

    base32_secret_key = base64.b32encode(byte_string[:16] + byte_string[-16:]).decode('utf-8')

    totp = pyotp.TOTP(base32_secret_key)
    if not totp.verify(otp):
        return jsonify({"error": "Invalid OTP"}), 400

    sid = new_sid(id)

    response = {
        "message": "OTP code approved, sending SID!",
        "received_data": data,
        "sid": sid
    }
    return jsonify(response), 200


@app.route('/verify-otp', methods=['POST'])
def handle_post_verify_otp():
    data = request.get_json()
    username = data.get('username')
    otp = data.get('otp')

    if not username or not otp:
        return jsonify({"error": "username and otp are required"}), 400

    # Retrieve the temporary user data from the previous step
    user_data = temp_user_data.get(username)

    if not user_data:
        return jsonify({"error": "Invalid or expired signup session"}), 400

    # Step 1: Verify the OTP using the secret key
    totp = pyotp.TOTP(user_data['secret_key'])
    if not totp.verify(otp):
        return jsonify({"error": "Invalid OTP"}), 400

    # Step 2: Create the user in the database
    new_user = User(username=username, email=user_data['email'], embedding=user_data['image'], last_logon=datetime.now())
    db.session.add(new_user)
    db.session.commit()

    # Cleanup temporary data after successful signup
    del temp_user_data[username]
    print("user created")
    return jsonify({"message": "User created successfully", "user_id": new_user.id}), 200


@app.route('/getpasswords', methods=['POST'])
def handle_post_getpasswords():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()

        print(data['sid'])
        user_id = verify_sid(data['sid'])
        if user_id != 0:
            send_data = get_user_passwords_by_user_id(user_id)

        else:
            send_data = "e prost sidu fratemiu"

        #data = json.loads(data)

        # Process the data (this is just an example)
        response = {
            "message": "Data received successfully!",
            "passwords": send_data,
            "sid" : data['sid']
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/deletepassword', methods=['POST'])
def handle_post_deletepasswords():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()

        # Verify the SID
        user_id = verify_sid(data.get('sid'))
        if user_id != 0:
            # SID is valid, proceed to delete the passwords
            password_ids = data.get('password_ids', [])

            if not password_ids:
                return jsonify({"error": "No password IDs provided."}), 400

            deleted_ids = []
            for password_id in password_ids:
                password_entry = Password.query.filter_by(id=password_id, user_id=user_id).first()
                if password_entry:
                    db.session.delete(password_entry)
                    deleted_ids.append(password_id)

            if deleted_ids:
                db.session.commit()
                response = {
                    "message": "Passwords deleted successfully!",
                    "deleted_ids": deleted_ids
                }
                return jsonify(response), 200
            else:
                return jsonify({"error": "No passwords found to delete or you do not have permission to delete them."}), 404
        else:
            return jsonify({"error": "Invalid SID."}), 403
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/addpassword', methods=['POST'])
def handle_post_addpassword():
    if request.is_json:
        data = request.get_json()
        print('password')

        # Verify the SID
        user_id = verify_sid(data.get('sid'))
        print(user_id)
        if user_id != 0:
            # SID is valid, proceed to add the new password
            password = data.get('password')
            name = data.get('name')
            x = form_encryption_key(user_id)
            x = encrypt_password(password, x)

            if password and name:
                new_password = Password(
                    user_id=user_id,
                    password=x,
                    name=name,
                    date_created=datetime.now(),
                    date_modified=datetime.now()
                )

                db.session.add(new_password)
                print("added")
                db.session.commit()

                response = {
                    "message": "Password added successfully!",
                    "password_id": new_password.id
                }
                return jsonify(response), 200
            else:
                return jsonify({"error": "Missing password or name."}), 400
        else:
            return jsonify({"error": "Invalid SID."}), 403
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/modifypassword', methods=['POST'])
def handle_post_modifypassword():
    if request.is_json:
        data = request.get_json()

        # Verify the SID
        user_id = verify_sid(data.get('sid'))
        if user_id != 0:
            # SID is valid, proceed to modify the password
            password_id = data.get('password_id')
            password = data.get('password')
            name = data.get('name')
            x = form_encryption_key(user_id)
            modified_password = encrypt_password(password, x)

            if password and name:
                password_entry = Password.query.filter_by(id=password_id, user_id=user_id).first()
                if password_entry:
                    password_entry.password = modified_password
                    password_entry.name = name
                    password_entry.date_modified = datetime.now()

                    db.session.commit()

                    response = {
                        "message": "Password modified successfully!",
                        "password_id": password_id
                    }
                    return jsonify(response), 200
                else:
                    return jsonify({"error": "Password not found or you do not have permission to modify it."}), 404
            else:
                return jsonify({"error": "Missing password or name."}), 400
        else:
            return jsonify({"error": "Invalid SID."}), 403
    else:
        return jsonify({"error": "Request must be JSON"}), 400


if __name__ == '__main__':

    temp_user_data = {}
    model = tf.keras.models.load_model('finetuned_facenet_model.h5')
    model.load_weights('finetuned_facenet.h5')
    app.run(debug=True)