import base64, uuid

url = "http://localhost:5500/templates/login.html"
# print(base64.urlsafe_b64encode(url.encode('utf-8')))

shortcode = "1"
encode = base64.urlsafe_b64encode(shortcode.encode('utf-8'))
print(encode)
# short = b'MTIzNDU='.decode("utf-8")
# print(short)
decoded_short = base64.urlsafe_b64decode('None')
print(decoded_short)
# print(base64.urlsafe_b64encode(str(uuid.uuid5).encode('utf-8')))

