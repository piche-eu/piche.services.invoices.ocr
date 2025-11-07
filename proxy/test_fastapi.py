import base64
import requests

filepath = "/Users/leonid/Desktop/HotCode/piche.invoice.ocr/data/dataset/pdf/v2/inv/0057125VEUB2B/Faktura_VAT_0057125VEUB2B.pdf"
 
#data_to_send = "This is some data to be sent as base64."
#encoded_string = base64.b64encode(data_to_send.encode("utf-8")).decode("utf-8")

    # Example: Encoding a file
with open(filepath, "rb") as image_file:
    encoded_string = image_file.read()
    encoded_string = base64.b64encode(encoded_string).decode("utf-8")

url = "http://127.0.0.1:8000/upload-base64-file/"  # Replace with your FastAPI server address
payload = {"data": encoded_string, "filename":"test.pdf"}
headers={"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)


print(response.json())
