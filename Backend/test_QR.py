import pyotp
import qrcode
# Generate a secret key for a new user
secret = pyotp.random_base32()




# Generate TOTP URI
totp_uri = pyotp.totp.TOTP('NV4VG5LQMVZFGZLDOJSXIS3FPHGESJR7MNE6VPQ6ZOLD6NBGQQ7A====').provisioning_uri(name="LT", issuer_name="YourAppName")

# Generate QR code
qr = qrcode.make(totp_uri)
qr.save("qrcode.png")  # or qr.show() to display directly