import pyotp
import qrcode
import PIL
import base64
from io import BytesIO

def generate_qr_for_2fa(username, secret):
    # Step 1: Generate a secret key

    # Step 2: Create a TOTP URI
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name='NoPassManager')

    # Step 3: Generate the QR code
    qr = qrcode.make(totp_uri)

    # Step 4: Convert the QR code to a Base64 encoded string
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')


    return qr_base64


#y = generate_qr_for_2fa('LT', 'Franta')
#print(y)
