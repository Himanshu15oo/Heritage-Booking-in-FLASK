# Import QRCode from pyqrcode
import pyqrcode
import png
from pyqrcode import QRCode


# String which represents the QR code
s = "upi://pay?pa=himanshusangale@oksbi&pn=HimanshuSangale&am=1&tn=Trial"

# Generate QR code
url = pyqrcode.create(s)

# Create and save the svg file naming "myqr.svg"
url.svg("../static/img/h.svg", scale = 8)
# Create and save the png file naming "myqr.png"
# url.png('myqr.png', scale = 6)

# # Importing library
# import qrcode

# # Data to be encoded
# data = 'QR Code using make() function'

# # Encoding data using make() function
# img = qrcode.make(data)
# print(img)
# # Saving as an image file
# # img.save('MyQRCode1.png')
