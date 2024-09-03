import struct
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import time
import numpy as np
def floats_to_bytestring(float_array):
    # Initialize an empty bytestring
    concatenated_bytes = b''

    # Iterate over each float in the array
    for number in float_array:
        # Convert the float to bytes using struct.pack with 'f' format (for 32-bit float)
        byte_repr = struct.pack('f', number)
        # Concatenate the byte string
        concatenated_bytes += byte_repr

    return concatenated_bytes


def get_encryption_key_bytes():
    """Retrieve the ENCRYPTION_KEY environment variable as a bytestring."""
    encryption_key_str = os.getenv('ENCRYPTION_KEY')
    if encryption_key_str is None:
        raise ValueError("ENCRYPTION_KEY environment variable is not set or accessible.")

    # Convert the string to a bytestring
    encryption_key_bytes = encryption_key_str.encode('utf-8')
    return encryption_key_bytes

def concatenate_with_encryption_key(concatenated_array_bytes):
    """Concatenate the bytestring from the array with the ENCRYPTION_KEY bytestring."""
    encryption_key_bytes = get_encryption_key_bytes()
    combined_bytes =encryption_key_bytes + concatenated_array_bytes
    return combined_bytes

def encrypt_password(password, encryption_key):
    # Se asigura dimensiune de 32 bytes pentru cheia de criptare
    key = encryption_key[:16] + encryption_key[-16:]

    # Se genereaza un Vector de initializare aleatoriu
    iv = get_random_bytes(16)

    # Se creaza cifrul AES
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Datele sunt paded astfel incat sa fie un multiplu de 16 bytes
    padded_password = pad(password.encode('utf-8'), AES.block_size)

    # Datele sunt encriptate
    encrypted_password = cipher.encrypt(padded_password)

    # Se concateneaza Vectorul de initializare cu parola criptate si sunt transformate in string
    encrypted_data = base64.b64encode(iv + encrypted_password).decode('utf-8')

    return encrypted_data

def decrypt_password(encrypted_data, encryption_key):
    # Ensure the key is 32 bytes long (AES-256)
    key = encryption_key[:16] + encryption_key[-16:]

    # Decode the base64 encoded data
    encrypted_data_bytes = base64.b64decode(encrypted_data)

    # Extract the IV from the data (first 16 bytes)
    iv = encrypted_data_bytes[:16]

    # Extract the encrypted password
    encrypted_password = encrypted_data_bytes[16:]

    # Create AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt and unpad the password
    decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size)

    return decrypted_password.decode('utf-8')

"""
start = time.time()
password = "[-0.2307377 ,-0.4660222 ,-0.06995983,-0.18325752, 0.7292609 , 0.32554156,  0.02091003,-0.23755743, 0.41929367, 0.17709339, 0.24358925,-0.29455507,  0.4087082 ,-0.4127251 ,-0.639276  , 0.19810684, 0.40786022, 0.1525115 ,  0.6914342 ,-0.58557886, 0.23110923, 0.31375375,-0.51068187, 0.22786243,  0.13952215, 0.5282963 , 0.8555364 , 0.23213883,-0.34643358,-0.503858  , -0.31352496, 0.5678036 , 0.0422053 ,-0.2473507 , 0.447639  , 0.05975984,  0.10030472,-0.19583154, 0.04530088, 0.03933842, 0.1601654 ,-0.04231195,  0.4279709 , 0.07976694,-0.56027836,-0.46891922,-0.25774208,-0.30035028,  0.4840098 , 0.10025689,-0.55831563, 0.7173816 , 0.08519188,-0.175013  ,  0.54805624, 0.43161654, 0.08528413,-0.610997  ,-0.24846393,-0.65098786, -0.5089052 , 0.07175206, 0.49330786, 0.98850095,-0.16162853, 1.0088998 ,  0.20600474, 0.44220212, 0.29321438,-0.05121751, 0.14592725,-0.48236102,  0.48595995,-0.45598215, 0.1500462 ,-0.05617182,-0.35488385, 0.320603  , -0.37812093,-0.28124747,-0.17624521,-0.00958811,-0.26138183, 0.42112675,  0.70414484, 0.30285412,-0.19729263,-0.03737684,-0.19406569, 0.61069465,  0.47845608, 0.27539536, 0.11485241,-0.15260541, 0.43062574, 0.6244058 , -0.25703648,-0.15702507,-0.64113706,-0.13427477,-0.06426565, 0.555857  ,  0.58198464,-0.89304096,-0.09938101,-0.02822279,-0.15396741, 0.18908969, -0.32148084,-0.89766675, 0.2437118 , 0.3589551 , 0.24273783, 0.74043673,  0.116278  , 0.27258563,-0.22989337, 0.5862399 , 0.6250827 , 0.4283789 , -0.32449406,-0.2599426 , 0.76048243, 0.0195674 , 0.64956355,-0.45759115,  1.1780736 , 0.25810397]"

encrypted_password = encrypt_password(password, get_encryption_key_bytes())
print("Encrypted Password:", encrypted_password)

decrypted_password = decrypt_password(encrypted_password, get_encryption_key_bytes())
print("Decrypted Password:", decrypted_password)

array_back = np.fromstring(decrypted_password[1:-1], sep=',')
array_back = np.expand_dims(array_back, axis=0)
print("Array:", array_back)
#get_encryption_key_bytes()

# Example usage:
float_array = [-0.2307377 , -0.4660222 , -0.06995983, -0.18325752,  0.7292609 ,
         0.32554156,  0.02091003, -0.23755743,  0.41929367,  0.17709339,
         0.24358925, -0.29455507,  0.4087082 , -0.4127251 , -0.639276  ,
         0.19810684,  0.40786022,  0.1525115 ,  0.6914342 , -0.58557886,
         0.23110923,  0.31375375, -0.51068187,  0.22786243,  0.13952215,
         0.5282963 ,  0.8555364 ,  0.23213883, -0.34643358, -0.503858  ,
        -0.31352496,  0.5678036 ,  0.0422053 , -0.2473507 ,  0.447639  ,
         0.05975984,  0.10030472, -0.19583154,  0.04530088,  0.03933842,
         0.1601654 , -0.04231195,  0.4279709 ,  0.07976694, -0.56027836,
        -0.46891922, -0.25774208, -0.30035028,  0.4840098 ,  0.10025689,
        -0.55831563,  0.7173816 ,  0.08519188, -0.175013  ,  0.54805624,
         0.43161654,  0.08528413, -0.610997  , -0.24846393, -0.65098786,
        -0.5089052 ,  0.07175206,  0.49330786,  0.98850095, -0.16162853,
         1.0088998 ,  0.20600474,  0.44220212,  0.29321438, -0.05121751,
         0.14592725, -0.48236102,  0.48595995, -0.45598215,  0.1500462 ,
        -0.05617182, -0.35488385,  0.320603  , -0.37812093, -0.28124747,
        -0.17624521, -0.00958811, -0.26138183,  0.42112675,  0.70414484,
         0.30285412, -0.19729263, -0.03737684, -0.19406569,  0.61069465,
         0.47845608,  0.27539536,  0.11485241, -0.15260541,  0.43062574,
         0.6244058 , -0.25703648, -0.15702507, -0.64113706, -0.13427477,
        -0.06426565,  0.555857  ,  0.58198464, -0.89304096, -0.09938101,
        -0.02822279, -0.15396741,  0.18908969, -0.32148084, -0.89766675,
         0.2437118 ,  0.3589551 ,  0.24273783,  0.74043673,  0.116278  ,
         0.27258563, -0.22989337,  0.5862399 ,  0.6250827 ,  0.4283789 ,
        -0.32449406, -0.2599426 ,  0.76048243,  0.0195674 ,  0.64956355,
        -0.45759115,  1.1780736 ,  0.25810397]

byte_string = floats_to_bytestring(float_array)

byte_string = concatenate_with_encryption_key(byte_string)

base32_secret_key = base64.b32encode(byte_string[:16] + byte_string[-16:]).decode('utf-8')

print(base32_secret_key)



# Retrieve the environment variable
encryption_key_str = os.getenv('ENCRYPTION_KEY')

# Convert the string to bytes
encryption_key_bytes = encryption_key_str.encode('utf-8')


print(encryption_key_bytes)
"""
