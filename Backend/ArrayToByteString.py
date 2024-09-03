import struct
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import time
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


# Example usage:
float_array = [-0.2838298 , -0.3080995 ,  0.035477  , -0.28573614,  0.7336259 ,
         0.3973074 ,  0.04761413, -0.32054025,  0.44421598,  0.11132391,
         0.25643766, -0.21591187,  0.37397936, -0.4368855 , -0.64613366,
         0.1690355 ,  0.4005965 ,  0.38201612,  0.9164581 , -0.6054882 ,
         0.20859823,  0.20324884, -0.57350284,  0.10675593,  0.01395878,
         0.55223215,  0.6539406 ,  0.07772115, -0.36922932, -0.48371834,
        -0.3063242 ,  0.46062854,  0.02200865, -0.2861081 ,  0.4699202 ,
         0.04030308,  0.19487861, -0.02503372,  0.10112329, -0.00858482,
         0.31499207,  0.02353511,  0.52731246,  0.17827892, -0.550956  ,
        -0.5846303 , -0.22581303, -0.17431739,  0.51342976,  0.1749169 ,
        -0.4576025 ,  0.88312393,  0.15936592, -0.10222222,  0.5201398 ,
         0.3870332 ,  0.05202313, -0.6963627 , -0.14555587, -0.49615723,
        -0.36857724, -0.03232872,  0.39624542,  0.9272887 , -0.1067998 ,
         1.0535853 ,  0.22083491,  0.46007213,  0.24656186,  0.0831952 ,
         0.08047834, -0.541955  ,  0.40174198, -0.54027957,  0.12332012,
        -0.02484034, -0.401708  ,  0.23519251, -0.5119965 , -0.39173827,
        -0.16595381,  0.06372456, -0.25030804,  0.41361916,  0.6370263 ,
         0.37801352, -0.13412097, -0.01332214, -0.2915726 ,  0.6945733 ,
         0.24637783,  0.29506734,  0.20645806, -0.27646995,  0.35081106,
         0.49273247, -0.2745526 , -0.2543452 , -0.6611102 , -0.02418789,
        -0.00540143,  0.5306119 ,  0.53008443, -0.8681118 , -0.20100586,
         0.08905891, -0.31863165,  0.29858488, -0.32042328, -0.8161375 ,
         0.15531483,  0.385621  ,  0.15298569,  0.7217248 ,  0.00635636,
         0.16268072, -0.34786952,  0.40322715,  0.6158768 ,  0.39011428,
        -0.3721456 , -0.32743403,  0.7642866 ,  0.06945989,  0.69248503,
        -0.48993954,  1.2605829 ,  0.34476212]

byte_string = floats_to_bytestring(float_array)

byte_string = concatenate_with_encryption_key(byte_string)

print(byte_string[:32])



# Retrieve the environment variable
encryption_key_str = os.getenv('ENCRYPTION_KEY')

# Convert the string to bytes
encryption_key_bytes = encryption_key_str.encode('utf-8')


print(encryption_key_bytes)

def encrypt_password(password, encryption_key):
    """Encrypt a password using AES encryption."""
    # Ensure the key is 32 bytes long (AES-256)
    key = encryption_key[:32]

    # Generate a random IV (Initialization Vector)
    iv = get_random_bytes(16)

    # Create AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the password to be a multiple of 16 bytes
    padded_password = pad(password.encode('utf-8'), AES.block_size)

    # Encrypt the password
    encrypted_password = cipher.encrypt(padded_password)

    # Encode the IV and the encrypted password to base64 to return as a string
    encrypted_data = base64.b64encode(iv + encrypted_password).decode('utf-8')

    return encrypted_data

def decrypt_password(encrypted_data, encryption_key):
    """Decrypt a password using AES encryption."""
    # Ensure the key is 32 bytes long (AES-256)
    key = encryption_key[:32]

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
start = time.time()
password = 'LeagueofLegends'

encrypted_password = encrypt_password(password, byte_string)
print("Encrypted Password:", encrypted_password)

decrypted_password = decrypt_password(encrypted_password, byte_string)
print("Decrypted Password:", decrypted_password)
